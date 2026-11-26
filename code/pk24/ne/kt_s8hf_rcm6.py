#!/usr/bin/env python3
"""kt_s8hf_rcm6.py -- pk24: kt_s8hf_rcm5_pk24.py (6fce793b) with the N5ROW, N5ABSENT and C-REPRO-RC5 prints
(make_rcm6_v1.py). rcm5's docstring follows.
kt_s8hf_rcm5_pk24.py -- pk24: kt_s8hf_rcm4_pk24.py (d3d59ce2) with the two-sided rows from n = 5 on (make_rcm5_v1.py).
rcm4's docstring follows.
kt_s8hf_rcm4_pk24.py -- pk24: kt_s8hf_rcm3_pk24.py (8e0d47ae) with the first ten pieces in the grid and the M1CONS count
(make_rcm4_v1.py). rcm3's docstring follows.
kt_s8hf_rcm3_pk24.py -- pk24: kt_s8hf_rcm2_pk24.py (6d41b5f1) with the horizontal chains dropping the certified vertical
chain's dual run (make_rcm3_v1.py). rcm2's docstring follows.
kt_s8hf_rcm2_pk24.py -- pk24: kt_s8hf_rcm1_pk24.py (65ff267c) plus a zero-bar reading and first-piece diagnostics
(make_rcm2_v1.py). rcm1's docstring follows.
kt_s8hf_rcm1_pk24.py -- pk24: the fix to NE_RC_DESIGN_v1: the RC reading
on certified inputs (S8's certified chain with real bars from kt_s8_cert_v1_14_3_pk24.py in its cert chunk namespace, pk15's
certified t export, certified tau', a fixed rational c, |v_i| capped by R_w, bars on the float horizontal entries), made by
make_rcm1_v1.py from kt_s8hf_rc3_pk24.py (466795f4). rc3's docstring follows.
kt_s8hf_rc3_pk24.py -- pk24: kt_s8hf_rc2_pk24.py (30b3a99d) plus the RCC reading (make_rc3_v1.py). rc2's docstring follows.
kt_s8hf_rc2_pk24.py -- pk24: kt_s8hf_rc1_pk24.py (94abcdb7) plus C-HARM-RC and PLANT-RC at t = 0, RCXW, RCIN and the RCBAR
readings (make_rc2_v1.py). rc1's docstring follows.
kt_s8hf_rc1_pk24.py -- pk24: kt_s8hf_v2d_pk24.py plus three readings (FLOAT DATA): option (a') on every FLIP/SAME slot
(v2d scans slot 1 only); option (a') with the bb bulk vector mirrored (v2d's MB is BHa unmirrored); and RC, the R-centred
H-NORM (B~ = kappa S'^2 - R, 0 <= Q0 R Q0 <= tau', centred at tau'/2) with Euclidean W'-balls (pk24/STATE.md). The copy's
docstring follows.
kt_s8hf_v2d_pk24.py -- pk24 COPY of pk22/w1/s8hf_a/kt_s8hf_v2d_px22.py (sha256 1524a13c45dbfde3edaf507cab31c483ac8286659200713f721a6d017aa4c5af) made by pk24/ne/make_rc1_v1.py:
outputs in pk24/ne/out, the cert module copied into pk24/ne (59d4f3e5fe165333). pk22's docstring follows.
kt_s8hf_v2d_px22.py -- pk22 (from kt_s8hf_v2c_px22.py d823e75b), NE option (a'): p_H's W'-part pinned from slot 1's exact
hT within beta_perp R_w, in place of option (a)'s pn_SH4 ball. v2c's docstring follows.
kt_s8hf_v2c_px22.py -- pk22 (from kt_s8hf_v2b_px22.py 6f6ae805): the exact chain is evaluated on option (a)'s top-mode
thresholds (rows_h and rows_mixed take m0o), so every option (a) row has its true central value. v2b's docstring follows.
kt_s8hf_v2b_px22.py -- pk22 (from kt_s8hf_v2a_px22.py e385855f): option (a)'s headroom takes the true central value from the
exact chain and the lower end from option (a)'s chain (CM.head(v_true, lo_a)), merged by row key. v2a's docstring follows.
kt_s8hf_v2a_px22.py -- pk22 COPY of pk11/kt_s8hf_v2.py (sha256 c27e24b2b2dfb74281b91a4048103bda97ede99ab634a136acad20080273d3e0) made by make_s8hf_a_v1.py for NE's option (a): outputs in
pk22/w1/s8hf_a/out; inputs from pk11; the cert module copied (bbdfb48622e93903); the scan's reading P2 by opt_a_chain and setup_p2a
(no N2T or TT in it). FLOAT DATA. The original docstring follows.
kt_s8hf_v2.py -- pk11 (code/pk11/). P2-12's float engine, step 2 of DESIGN_P2_12_FLOAT_v1_2 (2b7795ab): the MIXED classes (the
horizontal t edge with a vertical partner a or b), and reading P2 (Option A with SH4's u-perp form at gaps >= 2, with v1_2's top-mode
terms, sects. 4.2-4.3) for FLIP, SAME and MIXED. REVISION of kt_s8hf_v1_2 (29f358d0): its engine and controls are unchanged, and its
docstring follows. FLOAT DATA, not a certificate.
Additions:
- jacobi_eig, bperp and setup_p from kt_s8hp_v1_1 (49ab72a5), unchanged. beta_perp per piece as there: kappa = (N-1)/2 - c_lo
  (pk15's MOCK c_t ball), rho_1 the largest |Ritz value| of S' on W', eps_H = c_N / J_lo, TRB_H the rule's J-uniform value, and
  alpha = (N-1)/2 - c(t = 0) (the chain's harmonic c).
- setup_p2, reading P2: setup_p's form plus the top-mode terms. Slot 1: rnX = l_u pc_H + pn R_w s' + sqrt((beta_perp R_w)^2 - wn'^2);
  slots i >= 2: rnX = l_u(i-2) pc_H + pn e[i-1] s' + beta_perp e[i-1]. wn' comes from the W'-components, each widened by s pn R_w;
  pn = hyp(|BH|, pc_H) >= |p_H|, s' = vac sp, s = vac s. C-P2-REG: with the top-mode terms off, setup_p2 reproduces setup_p ball for
  ball.
- The two-chain pair form (sect. 5.1): vecs2, cov2_2, sf_pair2 and dk_class2 are S8's vecs, cov2, sf_pair and dk_class with the left
  pair and its residuals from the left chain and the right pair from the right chain; the T-chain data (R; the lemma's sperp, eta, r, Rn,
  gform) are common. S8's k = 0 parity shortcut applies only when both sides are the same objects. dk_class2's far branch is S8's
  vertical one ('V', with the given first far slot) or the horizontal one ('H', dk_class_h's exponents).
- C-MIXED-REG, at the grid's first and last piece, over every S8 class (DNEAR, m <= MM), ball for ball (equal midpoints and
  radii): (a) sf_pair2 with the vertical chain and its prm as the same objects on both sides, parity on, against S8's sf_pair; (b) with
  copies of them on the right, parity off, against sf_pair(parity=False); (c) dk_class2 against S8's dk_class (near, inf, and far with
  S8's DFAR); (d) S8's far_lo2 on both bases. PLANT-MIXED-REG: the right chain's slot-0 insertion vector + 1e-9 must break (a).
- MIXED classes (P2-11's MIXED threshold T_M = 3 at N4 and 2 at N3, on the pair's smaller exponent), kinds 'same' (t with a) and 'flip'
  (t with b), the top-mode form from each class's m0 on:
  - HV: the horizontal edge near (slots 0..T_M, gaps 1..T_M + 1) at the left, the vertical partner at the right: two-sided (slots
    -1..T_M - 1, n >= 6), far (S8's vertical far bound from slot T_M; route B where its slots exist) or at infinity (S8's TM/MB bulk);
  - VH: the vertical edge near (slots -1..T_M - 1) at the left, the horizontal edge far (far_lo2_h from slot T_M + 1; route B where
    its slots exist) or at infinity (the bulk vector BH).
- Controls: C-HARM-H under P2 (FLIP and SAME at t = 0, containment); C-HARM-H-M (the mixed classes at t = 0: HV two-sided at n = 6..8,
  HV and VH at infinity on a 64-column strip; containment, under A and under P2) with PLANT-RES-M (every slot residual of both chains
  set to 0 must break it for some class); C-REPRO-M (the n = 5 mixed classes against P2-13's exact float values at the first piece,
  containment, under A and P2).
- Readings per piece: FLIP and SAME under P2 (slot-1 rows); MIXED under A+ (beta_H with kappa and wn) and under P2 (all rows). Class
  tables: every MIXED class (smallest headroom over m and the pieces, failing rows) under P2 and A+, and the FLIP and SAME classes that
  failed under A+, under P2. The rule (the): every row > 0 with headroom >= 2.
Items: ITEM n4|n3, PHASE smoke (the first piece) or scan (the grid). Writes pk11/out/s8hf_v1/out_kt_s8hf_v2_<item>_<phase>.out (new
file).
Run: D=/mnt/g2/release/root/code/pk11; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_s8hf_v2.py n4 120 scan > $D/out/s8hf_v1/kt_s8hf_v2_n4_scan.log 2>&1
kt_s8hf_v1_2.py -- pk11 (code/pk11/). REVISION of kt_s8hf_v1_1.py (e7dc3981), which stopped at the cert module's import (its
smoke n4 log: FileExistsError): the module opens its own chunk output on import, and v1's smoke had already made the stray with the fixed
tag r91. v1_2 takes the first free tag of r50..r99 for the stray (the name the module computes), printed. Nothing else changes; v1_1's
docstring follows.
kt_s8hf_v1_1.py -- pk11 (code/pk11/). REVISION of kt_s8hf_v1.py (a6058cfe). v1's smoke n4 (out below) read INVALID on
PLANT-RES-H alone: slot 1's residual x 0.1 broke no containment at t = 0, i.e. Option A's slot-1 bound is looser than 10x there; the
scan's first piece (N4 61, J_lo 349.4) had 35 of 68 slot-1 rows failing the rule, among them H1 rows at large m that S8 leaves to the
top-mode form (v1 computed no far top-mode). Changes:
- PLANT-RES-H removes slot 1's residual (x 0), which must break containment somewhere; x 0.1 and x 0.01 are INFO lines;
- PLANT-END-H is N/A when no class is span-exact (C-HARM-H then has no equality gate);
- dk_class_h: S8's top-mode form with the horizontal far exponents, so the H1 rows stop at the far class's m0 (as S8's S8-1 rows);
- reading A+ beside A: setup_h(kw=True) subtracts at slot 1 kappa and wn, the lower ends of the u-part and the W-part of
  B~_e eps = y - l_u p_H (S8's setup form for its d <= 2, with two orthogonal pieces, in place of the lemma's); a negative root argument is reported; the scan prints
  A+'s rows and the failing classes per kind.
Everything else is v1's. v1's docstring follows.
kt_s8hf_v1.py -- pk11 (code/pk11/). P2-12's float engine, its controls and the gap-2 scan (DESIGN_P2_12_FLOAT_v1_1 9df2dbaf,
step 4). FLOAT DATA: point evaluations at each piece's J_lo, no bars; not a certificate.
Inputs (pinned by full sha256): kt_s8_cert_v1_14_1 (9e990130), imported in its mock chunk namespace c<N>_0000_0001 r91 (a stray, not
counted), for its stage A (S8's records and laws, the P2 export rows, S4-U, the mains, the trial sets, route (b)'s sets and helpers) and
its core s8core_v1_11 (CM); the horizontal entries of kt_s8h_mk_v1 / v1_1 / v1_2 / v1_3 (fT, hT on E3T, H4T; N2T, TT on the 4-column
graphs; the 4-strip S4,x,0,HT and S4,xy,0,HT,2,HT); pk15's mock EXPORT_P2_T_v1 (Qvt_hi and the c_t ball per piece)
RULING_P3_BETAH_TRBH (beta_H's J-uniform values, parsed); P2-13's float outputs (C-REPRO-H) and its list (classes).
The chain (sects. 3-4), on S8's slots: slot i holds S8's pair (l(i), x(i)) and the horizontal pair (l(i), y_H(i)), the bond at gap i + 1
whose inner column i + 2 is S8's X column for that slot; a class (iL, iR, kind, m) is a strip of n = iL + iR + m + 3 columns (S8's rule).
- y_H(i) is the centred two-step vector y = B~_e l(i - 2) = x_H - c l(i): slot 0 from fT (E3T) with f, slot 1 from hT (H4T)
  with h, both exact, as S8's L[0] and L[1] with fX -> fT, hX -> hT and the place-2 allowance on every component (the bond is not
  parity-pure); slots >= 2 by Ritz steps with B~_e's matrix C (N2T2 - c TT2) C^T rhob / lambda_0^2 and its u -> W block BH; c = N2T00 /
  TT00 (any c is exact for A^L and det; the residual adds |t00 - c| s').
- The bulk vector at infinity: (0, BH) for t, (0, F BH) for bb; BH carries the top-mode allowance beta_H sp.
- Residuals: slot 0 exact (the 4-strip entries, centred); slot 1 Option A, T-1 form, kappa = wn = 0 (the first scan):
  rnX(1) = l_u pc_H + beta_H e[0]; slots i >= 2: l_u(i-2) pc_H + beta_H e[i-1]; component errors AHW cerr[i-2][0] + beta_H rn1[i-2];
  pc_H = Qvt_hi + (ce_hi - ce_lo) s' (pk15); beta_H the one full norm (rule (d)); no parity refinement (sf_pair parity=False).
- Rows (S8's families on the horizontal chain): H2 two-sided (both edges near; iL, iR in DN), H1 one edge far (the far-end bound with the
  horizontal deviation exponents e_R = R_w rho1^(i-1), e_R+1 = R_w rho1^(i+1)), Hinf the right edge at infinity; the top-mode form
  (S8's dk_class) gives each near and inf class its m0; H1 rows run to m = MM. DN = {flip: (0, 1, 2), same: (0, 1)}; far thresholds
  {flip: 3, same: 2}; n >= 6 (n <= 5 is P2-13). MIXED (a vertical partner) is not in v1.
Controls (gates unless INFO):
- C-HASH; C-UMAIN (INFO): TT00 rhob / (g00 lambda_0^2) (1 at t = 0 for consistent units) and c against pk15's c_t ball;
- C-HARM-H (t = 0, the harmonic limit: vacuum allowances 0, U at t = 0): every two-sided class at n = 6, 7, 8 and every inf class against
  (N - 1) T^2 / 2 (T the free strip's harmonic transfer current, strip_T as kt_s8f2_pilot_v1_2; inf on a strip of 64 columns):
  equality (relative 1e-8) for the classes whose slots are span-exact at t = 0 (slot 0's t = 0 residual below 1e-10 of its norm,
  fixed before the comparison), containment in [cov_lo, cov_hi] for the others and every class with slot 1;
- C-REPRO-H: the n = 5 two-sided classes (0, 0, m 2), (0, 1, m 1), (1, 0, m 1) for flip and same at the first piece's J_lo, inside
  [cov_lo, cov_hi] against P2-13's exact float value (kt_s8f1_v1_3 n5a, n5b PAIR lines);
- PLANT-RES-H: slot 1's residual x 0.1 must break C-HARM-H's containment for at least one class;
- PLANT-END-H: the bulk vector in slot 0's place must break C-HARM-H's equality for at least one exact class.
The scan (sect. 7): every row with an edge in slot 1 (gap 2) on the piece grid; reading: the smallest headroom and every row with
lo <= 0 or headroom < 2; rule: Option A holds if none. Pieces where route (b) gives no tau_B are listed (no T-chain bound there).
Items: ITEM n4|n3, PHASE smoke (the first S8 piece and the controls) or scan (the controls and the grid). LIM <= 120 (the cert module's
mock cap sets RLIMIT_CPU on import). Writes pk11/out/s8hf_v1/out_kt_s8hf_v1_<item>_<phase>.out (new file).
Run: D=/mnt/g2/release/root/code/pk11; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_s8hf_v1.py n4 120 smoke > $D/out/s8hf_v1/kt_s8hf_v1_n4_smoke.log 2>&1"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import sys, re, json, math, hashlib, resource, importlib.util, traceback
from fractions import Fraction

ITEMS = {'n4': 4, 'n3': 3}
if len(sys.argv) < 4 or sys.argv[1] not in ITEMS or sys.argv[3] not in ('smoke', 'scan'):
    print('usage: kt_s8hf_rcm1_pk24.py n4|n3 LIM smoke|scan   (LIM 10..570)')
    sys.exit(2)
ITEM, PHASE = sys.argv[1], sys.argv[3]
N = ITEMS[ITEM]
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (10 <= LIM <= 570):
    print('bad LIM %r' % sys.argv[2])
    sys.exit(2)
CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk11'
W4OUT = OWN + '/out'   # pk22 copy: pk11's outputs, read only
OUTD = CODEDIR + '/pk24/ne'   # pk24 copy: every output here
HFD = OUTD + '/out'
MKD = W4OUT + '/s8h_mk_v1'
OUT_PATH = os.path.join(HFD, 'out_kt_s8hf_rcm6_%s_%s.out' % (ITEM, PHASE))
if not (os.path.isdir(HFD) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(HFD)
        and os.path.realpath(HFD).startswith(os.path.realpath(OUTD) + os.sep)):
    print('output directory check failed')
    sys.exit(2)
FH = open(OUT_PATH, 'x')


def out(line):
    FH.write(line + '\n')
    FH.flush()


def cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def sha_file(p):
    try:
        with open(p, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


CERT = OUTD + '/kt_s8_cert_v1_14_3_pk24.py'   # pk24 copy of pk11's certified S8 engine v1_14_3
HJ = {(4, 'small'): MKD + '/s8h_float_v1.4.small.json', (3, 'small'): MKD + '/s8h_float_v1.3.small.json',
      (4, 'h4'): MKD + '/s8h_float_v1.4.h4.json', (3, 'h4'): MKD + '/s8h_float_v1.3.h4.json',
      (4, 'n2t'): MKD + '/s8h_float_v1_1.4.n2t.json', (3, 'n2t'): MKD + '/s8h_float_v1_1.3.n2t.json',
      (4, 'l'): MKD + '/s8h_float_v1_2.4.l.json', (3, 'l'): MKD + '/s8h_float_v1_2.3.l.json',
      (4, 's4h'): MKD + '/s8h_float_v1_3.4.s4h.json', (3, 's4h'): MKD + '/s8h_float_v1_3.3.s4h.json'}
HZX = CODEDIR + '/pk15/out/export_p2_t_cert_kt_p2_assembly_v1_37_1.kv'   # pk24: the CERTIFIED t export
RUL = CODEDIR + '/rv01/RULING_P3_BETAH_TRBH_rv01.md'
P13O = {4: [W4OUT + '/out_kt_s8f1_v1_3_n5a.4.out', W4OUT + '/out_kt_s8f1_v1_3_n5b.4.out'],
        3: [W4OUT + '/out_kt_s8f1_v1_3_n5a.3.out', W4OUT + '/out_kt_s8f1_v1_3_n5b.3.out']}
P13L = W4OUT + '/S8F2_ENTRY_LIST_v1.json'
PINS = {CERT: '4de02e4ce30900739b204d9d3ee9160e8aae55331cab804bfa609908a4773a49', HZX: 'ad7e863d44d48bd59946f48c1de261f51751cd064f6129fc56d85cad9c7ee844', RUL: '7147e76610b6c8ebc5aae056cb9fc88641924c98921b13d74d5ce0b75db476ba', P13L: 'adaf07438f867232310c5a9f521461a9447b148b6895ed278bba3f7ecd1b03ff'}
PINS.update({HJ[k]: v for k, v in {(4, 'small'): '562748035ce6e03031b86c0fae88d6773fc52f93d5a9bd9ca0f59c57a5c3641c', (3, 'small'): '2f1604d6693fa9eebcd3e27c236ec47f4cc29b862fa7e252ec731ccea24d9f4c', (4, 'h4'): '9eec7646eb9233754a1877cb3d4950c4c88b31a43b8140712ce19aef7e2a839a',
                                   (3, 'h4'): '32057a2fef03c7de3d799ce5f73806bc6f68a25ca35b05f4a5072679e10c06f1', (4, 'n2t'): '0b7c7c969032d4ae8fa763e1da7049846333b30745cf270c2f8d948f9adcc310', (3, 'n2t'): 'cdbd310b629a9279e223a2e4d20907af78dd5d511029e69edbb4e9af458fa5ba',
                                   (4, 'l'): '9e9cc80de83a683840edc2ec2877ca0dfda2b09089d5065f828ef65bf988e63e', (3, 'l'): 'd229b036cdda9391ac3cdf74d32e99aad8e2b6a405f78f160f45f7c42725d96e', (4, 's4h'): '260435f5cbfefa41ef7b30283ab2491e36f46d34910df01768615175a614e65e',
                                   (3, 's4h'): 'f1a9bd1c75ef92d526aa98bfc100a365b2144a0eb93195acefaf1045abe9da0c'}.items() if k[0] == N})
PINS.update({p: v for p, v in zip(P13O[N], {4: ('f89b307744fafefdf3978880afbbec633f5fc4918bcbf9f77886ecd7c8f866c7', 'ce8be6246184bfc34b84644ed5470f22be703ecfb55317a01b2483b777d86e7f'), 3: ('2b0633395e747093c88ce1caf8b9417d6f882d4e89633142ca06b34816f78e29', '3990ee22cb6e7f291cbad1be1f687b8534eda8dffea1696288e9780cd6283f0b')}[N])})
out('kt_s8hf_v2 sha256 %s ITEM=%s PHASE=%s LIM=%d' % (sha_file(os.path.abspath(__file__)), ITEM, PHASE, LIM))
_bad = ['%s %s' % (os.path.basename(p), sha_file(p)[:8]) for p in sorted(PINS) if sha_file(p) != PINS[p]]
out('C-HASH %s (%d files)%s' % ('PASS' if not _bad else 'FAIL', len(PINS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)

# ---- the cert module (stage A and its core), in its mock chunk namespace (it sets RLIMIT_CPU to LIM on import)
STRAY = OUTD + '/cert_out_v143/out_kt_s8_cert_v1_14_3_pk24_cert_c%d_0000_0001_r%d.out'   # v1_2: the cert module's own output name on import
_free = [k for k in range(50, 100) if not os.path.exists(STRAY % (N, k))]
if not _free:
    out('VERDICT INVALID (no free stray tag r50..r99 for the cert module\'s import)')
    sys.exit(2)
out('IMPORT: the certified S8 module (v1_14_3 copy) in its cert chunk namespace c%d_0000_0001 with tag r%d (the first free of r50..r99; a stray, not counted)'
    % (N, _free[0]))
sys.argv = [CERT, 'cert', 'chunk', str(LIM), str(N), '0', '1', 'r%d' % _free[0]]
_spec = importlib.util.spec_from_file_location('kt_s8_cert_v1_14_3', CERT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)
CM = mod.CM
arb = mod.arb
ZERO, ONE = CM.ZERO, CM.ONE
fails = []


def gate(name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


# ---- inputs
def load_json_entries():
    E = {}
    for (n_, blk), p in HJ.items():
        if n_ != N:
            continue
        d = json.load(open(p))
        if d.get('N') != N:
            raise ValueError('%s: N %r' % (os.path.basename(p), d.get('N')))
        for k, v in d['entries'].items():
            E[k] = [float(x) for x in v['ak']]
    return E


def beta_h():
    txt = open(RUL).read()
    m4 = re.search(r'N4: ([0-9.]+) \(T\) and ([0-9.]+) \(M\)', txt)
    m3 = re.search(r'N3: ([0-9.]+) \(T\) and ([0-9.]+) \(M\)', txt)
    if not (m4 and m3):
        raise ValueError('beta_H values not found in the rule')
    return {4: Fraction(m4.group(1)), 3: Fraction(m3.group(1))}[N]


def hz_rows():
    rows = {}
    fields = None
    for ln in open(HZX).read().split('\n'):
        if ln.startswith('FIELDS = '):
            fields = ln.split(' = ')[1].split()
        mm = re.match(r'^N(\d)_P(\d{4}) = (.*)$', ln)
        if mm and int(mm.group(1)) == N:
            rows[int(mm.group(2))] = mm.group(3).split()
    if fields is None or fields[10] != 'Qvt_hi' or fields[12] != 'ce_lo' or fields[13] != 'ce_hi':
        raise ValueError('pk15 export: FIELDS %r' % fields)
    return {i: {'jlo': float(r[0]), 'Qvt': Fraction(r[10]), 'ce_lo': Fraction(r[12]), 'ce_hi': Fraction(r[13])} for i, r in rows.items()}


def ser(a, t):
    s = ZERO
    p = ONE
    for c in a:
        s = s + arb(c) * p
        p = p * t
    return s


# ---- the horizontal chain (sect. 3)
def chain_h(V, H, t, chV, mains, vac, betaH):
    """the horizontal chain's dict in S8's format: L[i] = (l(i), y_H(i)) for slots i = 0..7 (L[-1] = S8's, unused), 'c' = 0 and 'B' the
    centred bulk vector for t ('TM') and bb ('MB') at infinity, the slot-0 norms, plus the two-step Ritz data."""
    rhoE, rmain, rho4, rhob, rhoH = mains
    K = chV['K']
    C, R, lam0, g00, pi = chV['C'], chV['R'], chV['lam0'], chV['g00'], chV['pi']
    sg = g00.sqrt()
    rng = range(K + 1)
    idx = list(range(1, K + 1))
    g = [[V[('g', min(a, b), max(a, b))] for b in rng] for a in rng]
    e = [V[('e', a)] for a in rng]
    fT = [ser(H['fT,%d' % a], t) for a in rng]
    hT = [ser(H['hT,%d' % a], t) for a in rng]
    N2T = [[ser(H['N2T,%d,%d' % (min(a, b), max(a, b))], t) for b in rng] for a in rng]
    TT = [[ser(H['TT,%d,%d' % (min(a, b), max(a, b))], t) for b in rng] for a in rng]

    def comps(vec, scale):
        return [scale * sum((C[k][i] * (vec[n] - g[n][0] / g00 * vec[0]) for i, n in enumerate(idx)), ZERO) for k in range(K)]

    def p2(M, a, b):
        return M[a][b] - g[a][0] / g00 * M[0][b] - g[b][0] / g00 * M[a][0] + g[a][0] * g[b][0] / (g00 * g00) * M[0][0]

    def p1(M, n):
        return M[n][0] - g[n][0] / g00 * M[0][0]
    c = N2T[0][0] / TT[0][0]
    s = vac['s']

    def allow(v):
        a_ = (s * abs(v[0]).upper()).upper()
        return (v[0], [x + CM.pm(a_) for x in v[1]])
    L = dict(chV['L'])
    raw = {0: allow((rhoE * fT[0] / (lam0 * e[0]), comps(fT, rhoE * sg / (lam0 * e[0])))),
           1: allow((rhoH * hT[0] / (lam0 * lam0 * e[0]), comps(hT, rhoH * sg / (lam0 * lam0 * e[0]))))}
    for i in (0, 1):
        l = chV['L'][i][0]
        x = raw[i]
        L[i] = (l, (x[0] - c * l[0], [x[1][k] - c * l[1][k] for k in range(K)]))
    N2 = [[p2(N2T, a, b) - c * p2(TT, a, b) for b in idx] for a in idx]
    BH = [sum((C[k][i] * (p1(N2T, n) - c * p1(TT, n)) for i, n in enumerate(idx)), ZERO) * rhob / (lam0 * lam0 * sg)
          + CM.pm(CM.fr(betaH) * vac['sp']) for k in range(K)]
    # place 2 for B~_e's W block, as S8's F-1 allowance a1 for B_X's (c = 0 after centring): 2 s |p_W| + 4 beta_H s^2
    a1H = (2 * s * CM.norm_up(BH) + 4 * CM.fr(betaH) * s * s).upper()
    AHm = [[x * rhob / (lam0 * lam0) + CM.pm(a1H) for x in row] for row in CM.mmul(CM.mmul(C, N2), CM.mT(C))]
    cu = (N2T[0][0] - c * TT[0][0]) / g00 * rhob / (lam0 * lam0)   # the centred u -> u part (0 up to rounding)
    for i in range(2, 8):
        u1, k1 = chV['L'][i - 2][0]
        y = (cu * u1 + CM.dot(BH, k1), [BH[k] * u1 + CM.dot(AHm[k], k1) for k in range(K)])
        L[i] = (chV['L'][i][0], y)
    ch = dict(chV)
    ch['L'] = L
    ch['c'] = ZERO
    ch['B'] = {'TM': BH, 'MB': [BH[k] if pi[k] > 0 else -BH[k] for k in range(K)]}
    # slot-0 norms (centred) from the 4-strip entries
    Z4 = V[('Z4',)]
    X1H, X12H = ser(H['S4,x,0,HT'], t), ser(H['S4,xy,0,HT,2,HT'], t)
    F4 = rho4 * g00 / (lam0 * lam0 * e[0] * e[0])
    n2y = F4 * (X12H - 2 * c * X1H + c * c * Z4)
    n21 = F4 * Z4
    crs = F4 * (X1H - c * Z4)
    l0, y0 = L[0]
    lu, yu = l0[0], y0[0]
    sq = lambda v: v[0] * v[0] + sum((x * x for x in v[1]), ZERO)
    ap2 = lu * lu * (n2y - yu * yu) - 2 * lu * yu * (crs - yu * lu) + yu * yu * (n21 - lu * lu) - \
        sum(((lu * y0[1][k] - yu * l0[1][k]) * (lu * y0[1][k] - yu * l0[1][k]) for k in range(K)), ZERO)
    ch['h'] = {'c': c, 'AHm': AHm, 'BH': BH, 'cu': cu, 'res2y0': n2y - sq(y0), 'ny0': n2y, 'Ap2y0': ap2,
               'umain': TT[0][0] * rhob / (g00 * lam0 * lam0)}
    return ch


def setup_h(chH, prmV, betaH, pcH, kw=False):
    """prm for the horizontal chain (sect. 4): T-1 residuals; the T-chain's own fields from S8's setup. kw=False: kappa = wn = 0 (reading
    A); kw=True (v1_1, reading A+): slot 1 subtracts kappa and wn, lower ends of the u-part and the W-part of B~_e eps = y - l_u p_H, as
    S8's setup does for its d <= 2 (two orthogonal pieces with the place-2 allowances in the balls; the u-part from the balls
    that carry the allowances; slot 1's components are exact, so no component error enters); a negative root argument is reported
    in 'rootneg', and the root is then 0 for the float reading."""
    L, K = chH['L'], chH['K']
    hh = chH['h']
    bH = CM.fr(betaH)
    rn1, e, cerrV = prmV['rn1'], prmV['e'], prmV['cerr']
    zc = (ZERO, ZERO, ZERO)
    rnX = {-1: prmV['rnX'][-1], 0: CM.sqrt_up(hh['res2y0'])}
    cerr = {-1: zc, 0: zc, 1: zc, 'inf': zc}
    AHW = CM.sqrt_up(sum((x * x for row in hh['AHm'] for x in row), ZERO))
    dmax = max(k for k in e if isinstance(k, int))
    kap, wn, rootneg = ZERO, ZERO, False
    if kw:
        y = L[1][1]
        lum = L[-1][0][0]
        kap = abs(y[0]).lower()
        kap = kap if kap > 0 else ZERO
        wn = CM.sqrt_lo(sum(((y[1][k] - lum * hh['BH'][k]) * (y[1][k] - lum * hh['BH'][k]) for k in range(K)), ZERO))
        wn = wn if wn > 0 else ZERO
    for i in range(1, dmax + 1):   # slots 1..DMAX (the rows use slots <= 5)
        lu2 = abs(L[i - 2][0][0]).upper()
        if i == 1 and kw:
            arg = bH * bH * e[0] * e[0] - kap * kap - wn * wn
            rootneg = bool(arg.upper() < 0)
            rnX[i] = (lu2 * pcH + CM.sqrt_up(arg)).upper()
        else:
            rnX[i] = (lu2 * pcH + bH * e[i - 1]).upper()
        if i >= 2:
            cerr[i] = (cerrV[i][0], (AHW * cerrV[i - 2][0] + bH * rn1[i - 2]).upper(), ZERO)
    Ap = {-1: prmV['Ap'][-1], 0: CM.sqrt_up(hh['Ap2y0'])}
    for i in range(1, dmax + 1):
        Ap[i] = (abs(L[i][0][0]) * rnX[i] + abs(L[i][1][0]) * rn1[i]).upper()
    rnX['inf'], Ap['inf'] = pcH, pcH
    prm = dict(prmV)
    pn = CM.hyp(CM.norm_up(hh['BH']), pcH)
    prm.update({'rnX': rnX, 'rnXo': dict(rnX), 'Ap': Ap, 'cerr': cerr, 'pc': pcH, 'pn': pn, 'BN': bH, 'Bm': bH, 'cc': ZERO,
                'dmaxH': dmax + 1, 'kap': kap, 'wn': wn, 'rootneg': rootneg, 'betaRw': (bH * e[0]).upper()})
    return prm


def dk_class_h(ch, prm, dk, dL, dR, kind, kmax=400):
    """v1_1: S8's dk_class (the top-mode form) for the horizontal chain; only its far branch differs: the far right edge at slot DF[kind]
    has B~_e acting on l(DF - 2), deviation R_w rho1^(DF - 1), paired with l(DF), deviation R_w rho1^(DF + 1) (far_lo2_h's exponents);
    one full norm beta_H; the centred right vector has no c term."""
    far = dR == 'far'
    dRr = 'inf' if far else dR
    L1, LX, R1, RY = CM.vecs(ch, dL, dRr, kind)
    K = ch['K']
    AL = [L1[0] * LX[1][k] - LX[0] * L1[1][k] for k in range(K)]
    AR = [R1[0] * RY[1][k] - RY[0] * R1[1][k] for k in range(K)]
    rn1, rnX, cerr = prm['rn1'], prm['rnX'], prm['cerr']
    ALp, ARp = prm['Ap'][dL], prm['Ap'][dRr]
    dAL, dAR = CM.dvec(prm, dL, L1, LX), CM.dvec(prm, dRr, R1, RY)
    dfar, Dc = ZERO, ZERO
    nl = CM.hyp(CM.norm_up(L1[1]) + cerr[dL][0], rn1[dL])
    nx = CM.hyp(CM.norm_up(LX[1]) + cerr[dL][1], rnX[dL])
    if far:
        dRf = DF[kind]
        eR = (prm['Rw'] * CM.ipow(prm['rho1'], dRf - 1)).upper()
        eR1 = (prm['Rw'] * CM.ipow(prm['rho1'], dRf + 1)).upper()
        pn = prm['pn']
        dfar = (prm['BN'] * eR + pn * eR * eR1).upper()
        Dc = (2 * nl * eR1 * nx * (pn + dfar)).upper()
    elif dR != 'inf':
        nlr = CM.hyp(CM.norm_up(R1[1]) + cerr[dR][0], rn1[dR])
        nyr = CM.hyp(CM.norm_up(RY[1]) + cerr[dR][1], rnX[dR])
        Dc = (2 * nl * nlr * nx * nyr).upper()
    nAL = CM.hyp(CM.norm_up(AL) + dAL, ALp)
    nAR = (CM.hyp(CM.norm_up(AR) + dAR, ARp) + dfar).upper()
    k1, ko = dk['k1'], dk['ko']
    ua = (CM.SQ2 * dk['s1'] * nAL + dAL).upper()
    ub = (CM.SQ2 * dk['s1'] * nAR + dAR + dfar).upper()
    a, b = AL[k1], AR[k1]
    same_sign = (a.lower() > 0 and b.lower() > 0) or (a.upper() < 0 and b.upper() < 0)
    if not dk['ok'] or not same_sign or not abs(a).lower() > ua or not abs(b).lower() > ub:
        return None, arb(-1)
    alo, blo = (abs(a).lower() - ua).lower(), (abs(b).lower() - ub).lower()
    P = (alo * blo).lower()
    O = ((abs(AL[ko]).upper() + CM.SQ2 * dk['so'] * nAL + dAL) * (abs(AR[ko]).upper() + CM.SQ2 * dk['so'] * nAR + dAR + dfar)).upper()
    Rr = (CM.sqrt_up(nAL * nAL - alo * alo) * CM.sqrt_up(nAR * nAR - blo * blo)).upper()
    Rk = lambda k: (P - CM.ipow(dk['qo'], k) * O - CM.ipow(dk['qr'], k) * Rr - CM.ipow(dk['qd'], k) * Dc).lower()
    k0 = next((k for k in range(kmax + 1) if Rk(k) > 0), None)
    return k0, P


def far_lo2_h(chH, prm, dL, kind, m, base, dR):
    """S8's far_lo2 with the horizontal deviation exponents: B~_e at slot dR acts on l(dR - 2), deviation R_w rho1^(dR - 1), paired with
    l(dR), deviation R_w rho1^(dR + 1); one full norm beta_H; the centred right vector has no c term."""
    v, cov_lo, num_lo, zhi, nAL, nl, nx = base[:7]
    k = m - 1
    eR = (prm['Rw'] * CM.ipow(prm['rho1'], dR - 1)).upper()
    eR1 = (prm['Rw'] * CM.ipow(prm['rho1'], dR + 1)).upper()
    pn = prm['pn']
    dfar = (prm['BN'] * eR + pn * eR * eR1).upper()
    rk = CM.ipow(prm['r'] + prm['eta'], k).upper()
    ny = (pn + dfar).upper()
    num2 = (num_lo - nAL * rk * dfar - 2 * rk * rk * nl * eR1 * nx * ny).lower()
    z2 = (zhi + rk * nl * eR1).upper()
    return v, ((num2 / (z2 * z2)).lower() if num2 >= 0 else CM.NEGINF)


DN = {'flip': (0, 1, 2), 'same': (0, 1)}
DF = {'flip': 3, 'same': 2}


def rows_h(chH, prm, only_slot1=False, m0o=None):
    """the horizontal rows (family, class, headroom, lo, v, hi) and the top-mode m0 per near and inf class."""
    RkC = {}
    dkf = CM.dk_setup(chH, prm)
    m0 = {}
    rows = []
    for kind in ('flip', 'same'):
        for dL in DN[kind]:
            r_ = CM.dk_class(chH, prm, dkf, dL, 'inf', kind)
            m0[(dL, 'inf', kind)] = (r_[0] + 1) if r_[0] is not None else None
            r_ = dk_class_h(chH, prm, dkf, dL, 'far', kind)   # v1_1: the far class's own top-mode threshold
            m0[(dL, 'far', kind)] = (r_[0] + 1) if r_[0] is not None else None
            for dR in DN[kind]:
                r_ = CM.dk_class(chH, prm, dkf, dL, dR, kind)
                m0[(dL, dR, kind)] = (r_[0] + 1) if r_[0] is not None else None
    if m0o is not None:   # pk22 option (a): use the given thresholds
        m0 = dict(m0o)
    for kind in ('flip', 'same'):
        for dL in DN[kind]:
            for dR in DN[kind]:
                if only_slot1 and 1 not in (dL, dR):
                    continue
                mm0 = m0[(dL, dR, kind)]
                for m in range(1, CM.MM + 1):
                    if dL + dR + m + 3 < 5 or (mm0 is not None and m >= mm0):   # rcm5: n >= 5
                        continue
                    b = CM.sf_pair(chH, prm, dL, dR, kind, m, RkC, parity=False)
                    rows.append(('H2', (dL, dR, kind, m), CM.head(b[0], b[1]), b[1], b[0], b[7]))
            if only_slot1 and dL != 1:
                continue
            mm0 = m0[(dL, 'inf', kind)]
            mf0 = m0[(dL, 'far', kind)]
            for m in range(1, CM.MM + 1):
                base = CM.sf_pair(chH, prm, dL, 'inf', kind, m, RkC, parity=False)
                if mm0 is None or m < mm0:
                    rows.append(('Hinf', (dL, 'inf', kind, m), CM.head(base[0], base[1]), base[1], base[0], base[7]))
                if mf0 is not None and m >= mf0:   # v1_1: the far class's top-mode form covers m >= its m0
                    continue
                # S8's s81_cert with the horizontal far bound: route A (far bound from DF on) or route B (DF..DF+2 explicit, far
                # bound from DF + 3 on), the larger lower end; each covers every far right edge
                fa = far_lo2_h(chH, prm, dL, kind, m, base, DF[kind])
                loA = fa[1]
                loB = far_lo2_h(chH, prm, dL, kind, m, base, DF[kind] + 3)[1]
                for j in (0, 1, 2):
                    b = CM.sf_pair(chH, prm, dL, DF[kind] + j, kind, m, RkC, parity=False)
                    loB = b[1] if b[1] < loB else loB
                lo1 = loA if loA > loB else loB
                rows.append(('H1', (dL, 'far', kind, m), CM.head(fa[0], lo1), lo1, fa[0], None))
    return rows, m0


# ---- the harmonic reference (kt_s8f2_pilot_v1_2's strip_T)
def vpair(e):
    c, b = e
    return {'TM': (3 * c, 3 * c + 1), 'MB': (3 * c + 1, 3 * c + 2), 'HT': (3 * c, 3 * c + 3), 'HM': (3 * c + 1, 3 * c + 4),
            'HB': (3 * c + 2, 3 * c + 5)}[b]


def strip_T(n, e, f):
    mus = [(0.0, [1 / math.sqrt(3)] * 3), (1.0, [1 / math.sqrt(2), 0.0, -1 / math.sqrt(2)]),
           (3.0, [1 / math.sqrt(6), -2 / math.sqrt(6), 1 / math.sqrt(6)])]
    lams = [(2 - 2 * math.cos(math.pi * m / n), [(math.sqrt(1.0 / n) if m == 0 else math.sqrt(2.0 / n)) * math.cos(math.pi * m * (j + 0.5) / n)
                                                  for j in range(n)]) for m in range(n)]

    def amp(b, k, m):
        u, v = vpair(b)
        ph, ps = mus[k][1], lams[m][1]
        return ph[u % 3] * ps[u // 3] - ph[v % 3] * ps[v // 3]
    return sum(amp(e, k, m) * amp(f, k, m) / (mus[k][0] + lams[m][0]) for k in range(3) for m in range(n) if (k, m) != (0, 0))


def harm(iL, iR, kind, m):
    """(N - 1) T^2 / 2 for the class: two-sided on its own strip, inf on a strip of 64 columns."""
    b2 = 'HB' if kind == 'flip' else 'HT'
    if iR == 'inf':
        n = 64
        cR = iL + m + 1
    else:
        n = iL + iR + m + 3
        cR = n - 2 - iR
    T_ = strip_T(n, (iL, 'HT'), (cR, b2))
    return (N - 1) * T_ * T_ / 2.0


# ---- one piece
def piece(A, i, t, vac, Uh, betaH, pcH, scale1=None, end_bulk=False, kw=False):
    """the vertical T-chain, route (b), S8's setup, the horizontal chain and its prm at the point t (v1_1: kw, reading A+; 'prmHk' then
    holds A+'s prm beside reading A's 'prmH')."""
    E = A['EP'][N]
    Ech = mod.w3_keys(E)
    V = mod.entry_thin(Ech, t, 0)
    C0 = mod.ritz_pure(V, A['odd'][N])
    chV = CM.chain(V, A['mains'][N], A['odd'][N], vac, C0, tt=False)
    leak = None
    for b in mod.RB_ORDER:
        SL = mod.RB_SETS[b]
        VB = mod.entry_thin(mod.b_entries(E, SL), t, 0)
        oddc = set(j for j, s_ in enumerate(SL) if s_ in A['odd'][N])
        c0b = mod.basis_RB(VB, C0, oddc, len(SL) - 1)
        chB = CM.chain_RB(VB, vac, c0b, oddc, len(SL) - 1)
        leak = CM.routeb_leak(chB, Uh)
        if leak is not None:
            break
    if leak is None:
        return None
    P2row = A['pieces'][N][i]
    P2r = {k: CM.fr(P2row[k]) for k in ('Bp_hi', 'Bm_hi', 'Rw_hi', 'rho1_hi')}
    chU = dict(chV, Gl=leak['Gl'])
    prmV = CM.setup(chU, P2r, Uh, vac, Gl=leak['Gl'], sblk=leak['sblk'])
    chH = chain_h(V, HENT, t, chU, A['mains'][N], vac, betaH)
    if end_bulk:   # PLANT-END-H: the bulk vector in slot 0's place
        l0 = chH['L'][0][0]
        chH['L'][0] = (l0, (ZERO, list(chH['B']['TM'])))
    prmH = setup_h(chH, prmV, betaH, pcH)
    prmHk = setup_h(chH, prmV, betaH, pcH, kw=True) if kw else None
    if scale1 is not None:   # PLANT-RES-H: slot 1's residual scaled
        prmH['rnX'][1] = (prmH['rnX'][1] * arb(scale1)).upper()
        prmH['Ap'][1] = (abs(chH['L'][1][0][0]) * prmH['rnX'][1] + abs(chH['L'][1][1][0]) * prmV['rn1'][1]).upper()
    return {'V': V, 'chV': chV, 'prmV': prmV, 'chH': chH, 'prmH': prmH, 'prmHk': prmHk, 'leak': leak}


def zero_vac(vac):
    return {k: (v if k == 'Bp' else ZERO) for k, v in vac.items()}


# ---- v2: beta_perp, reading P (kt_s8hp_v1_1, unchanged) and reading P2 (DESIGN_P2_12_FLOAT_v1_2 sects. 4.2-4.3)
CN = 2.0 + (N - 1) * (N - 3) / 8.0   # H-BESSEL's c_N (as kt_s8hp_v1_1's C-CN)


def jacobi_eig(A_, sweeps=60):
    """the eigenvalues (ascending) of a small symmetric float matrix (cyclic Jacobi; A_ is symmetrized first)."""
    n = len(A_)
    a = [[0.5 * (A_[i][j] + A_[j][i]) for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        if math.fsum([a[i][j] ** 2 for i in range(n) for j in range(n) if i != j]) < 1e-300:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                th = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                tt = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
                cs = 1.0 / math.sqrt(tt * tt + 1.0)
                sn = tt * cs
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = cs * akp - sn * akq, sn * akp + cs * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = cs * apk - sn * aqk, sn * apk + cs * aqk
    return sorted(a[i][i] for i in range(n))


def bperp(kap, rho1, epsH, trb, alpha):
    """beta_perp = max(kappa rho_1^2, eps_H rho_1^2 + TRB_H - alpha) and its two arguments (floats)."""
    up = kap * rho1 * rho1
    lo = epsH * rho1 * rho1 + trb - alpha
    return (up if up > lo else lo), up, lo


def setup_p(chH, prmV, betaH, betaP, pcH, wnsub=True):
    """reading P: setup_h(kw=True) with SH4's u-perp form: slot 1 rnX = l_u pc_H + sqrt((beta_perp e[0])^2 - wn^2) (the
    wn subtraction kept, no kappa), slots i >= 2 rnX = l_u(i-2) pc_H + beta_perp e[i-1]; beta_H stays in the component errors, the far
    ends and the bulk allowance. betaP: a Fraction. v1_1: wnsub=False is reading P0, the plain form (slot 1 without the wn
    subtraction)."""
    prm = setup_h(chH, prmV, betaH, pcH, kw=True)
    L = chH['L']
    bP = CM.fr(betaP)
    e, rn1 = prmV['e'], prmV['rn1']
    wn = prm['wn']
    rnX, Ap = prm['rnX'], prm['Ap']
    dmax = max(k for k in e if isinstance(k, int))
    rootneg = False
    for i in range(1, dmax + 1):
        lu2 = abs(L[i - 2][0][0]).upper()
        if i == 1:
            arg = bP * bP * e[0] * e[0] - (wn * wn if wnsub else ZERO)
            rootneg = bool(arg.upper() < 0)
            rnX[i] = (lu2 * pcH + CM.sqrt_up(arg)).upper()
        else:
            rnX[i] = (lu2 * pcH + bP * e[i - 1]).upper()
    for i in range(1, dmax + 1):
        Ap[i] = (abs(L[i][0][0]) * rnX[i] + abs(L[i][1][0]) * rn1[i]).upper()
    prm.update({'rnX': rnX, 'rnXo': dict(rnX), 'Ap': Ap, 'rootnegP': rootneg, 'bpRw': (bP * e[0]).upper()})
    return prm


def setup_p2(chH, prmV, betaH, betaP, pcH, vac):
    """v2, reading P2 (DESIGN v1_2 sects. 4.2-4.3): reading P (wn subtracted) plus the top-mode terms. Slot 1: rnX = l_u pc_H + pn e[0] s'
    + sqrt((beta_perp e[0])^2 - wn'^2), wn' the lower end of the norm of the W'-components y_k - l_u BH_k, each widened by +- s pn e[0]
   ; slots i >= 2: rnX = l_u(i-2) pc_H + pn e[i-1] s' + beta_perp e[i-1]. pn = hyp(|BH|, pc_H) (setup_h's), s' = vac['sp'],
    s = vac['s']. With s = s' = 0 every added term is an exact zero, so the result equals setup_p's ball for ball (C-P2-REG)."""
    prm = setup_h(chH, prmV, betaH, pcH, kw=True)
    L, K = chH['L'], chH['K']
    hh = chH['h']
    bP = CM.fr(betaP)
    e, rn1 = prmV['e'], prmV['rn1']
    pn = prm['pn']
    y = L[1][1]
    lum = L[-1][0][0]
    a_ = CM.pm((vac['s'] * pn * e[0]).upper())
    wn = CM.sqrt_lo(sum(((y[1][k] - lum * hh['BH'][k] + a_) * (y[1][k] - lum * hh['BH'][k] + a_) for k in range(K)), ZERO))
    wn = wn if wn > 0 else ZERO
    rnX, Ap = prm['rnX'], prm['Ap']
    dmax = max(k for k in e if isinstance(k, int))
    rootneg = False
    for i in range(1, dmax + 1):
        lu2 = abs(L[i - 2][0][0]).upper()
        tm = (pn * e[i - 1] * vac['sp']).upper()
        if i == 1:
            arg = bP * bP * e[0] * e[0] - wn * wn
            rootneg = bool(arg.upper() < 0)
            rnX[i] = (lu2 * pcH + tm + CM.sqrt_up(arg)).upper()
        else:
            rnX[i] = (lu2 * pcH + tm + bP * e[i - 1]).upper()
    for i in range(1, dmax + 1):
        Ap[i] = (abs(L[i][0][0]) * rnX[i] + abs(L[i][1][0]) * rn1[i]).upper()
    prm.update({'rnX': rnX, 'rnXo': dict(rnX), 'Ap': Ap, 'rootnegP': rootneg, 'bpRw': (bP * e[0]).upper(), 'wnP2': wn,
                'tm1': (pn * e[0] * vac['sp']).upper()})
    return prm


def opt_a_chain(chH, prmV, bp, pnA, wA, vac, betaH):
    """pk22, NE option (a) (NE_OPTION_A_FORM_v1 0afeffa1, F1-F4, F6): chH with every quantity taken from N2T and TT replaced by
    certified balls: BH -> ball pn_SH4 + beta_H s'; y_H(i), i >= 2: u-part +-(w |l_u(i-2)| + pn_SH4 e[i-1]), W'-parts
    +-(pn |l_u(i-2)| + beta_perp e[i-1]) (e[k] bounds |eps(k-1)|; past dmax the last e, which is larger); AHm -> 0; cu -> +-w."""
    K = chH['K']
    e = prmV['e']
    dmax = max(k for k in e if isinstance(k, int))
    ch = dict(chH)
    L = dict(chH['L'])
    hh = dict(chH['h'])
    # option (a'): p_H's W'-part from slot 1's exact y(1) = B~_e l(-1), within beta_perp R_w (e[0] = R_w), plus the top-mode allowance
    y1 = chH['L'][1][1]
    rp = (CM.fr(Fraction(bp)) * e[0] + CM.fr(betaH) * vac['sp']).upper()
    BHa = [y1[1][_k] + CM.pm(rp) for _k in range(K)]
    for i in range(2, 8):
        ee = e[min(i - 1, dmax)]
        u1 = chH['L'][i - 2][0][0]
        au = abs(u1).upper()
        r_u = (CM.fr(Fraction(wA)) * au + CM.fr(Fraction(pnA)) * ee).upper()
        r_w = (CM.fr(Fraction(bp)) * ee).upper()
        L[i] = (chH['L'][i][0], (CM.pm(r_u), [BHa[_k] * u1 + CM.pm(r_w) for _k in range(K)]))
    ch['L'] = L
    ch['B'] = {'TM': BHa, 'MB': list(BHa)}
    hh.update({'BH': BHa, 'AHm': [[ZERO] * K for _k in range(K)], 'cu': CM.pm(CM.fr(Fraction(wA)).upper())})
    ch['h'] = hh
    return ch


def setup_p2a(chH, prmV, betaH, betaP, pcH, vac, pnA):
    """pk22, NE option (a) (F5, F7): reading P2 on opt_a_chain's chain with kappa = wn = 0, pn = hyp(pn_SH4 + beta_H s', pc_H), slot 1
    rnX = l_u pc_H + pn e[0] s' + beta_perp e[0], slots i >= 2 as P2, and no component error at slots i >= 2 beyond the balls."""
    prm = setup_h(chH, prmV, betaH, pcH, kw=False)
    L = chH['L']
    bP = CM.fr(betaP)
    e, rn1 = prmV['e'], prmV['rn1']
    y1n = CM.norm_up(chH['L'][1][1][1])   # option (a'): |p_H,W| <= |y(1)_W| + beta_perp R_w, or pn_SH4
    pq = (y1n + CM.fr(betaP) * e[0]).upper()
    pq = pq if pq < CM.fr(Fraction(pnA)).upper() else CM.fr(Fraction(pnA)).upper()
    pn = CM.hyp((pq + CM.fr(betaH) * vac['sp']).upper(), pcH)
    rnX, Ap, cerr = prm['rnX'], prm['Ap'], prm['cerr']
    dmax = max(k for k in e if isinstance(k, int))
    for i in range(1, dmax + 1):
        lu2 = abs(L[i - 2][0][0]).upper()
        tm = (pn * e[i - 1] * vac['sp']).upper()
        rnX[i] = (lu2 * pcH + tm + bP * e[i - 1]).upper()
        if i >= 2:
            cerr[i] = (cerr[i][0], ZERO, ZERO)
    for i in range(1, dmax + 1):
        Ap[i] = (abs(L[i][0][0]) * rnX[i] + abs(L[i][1][0]) * rn1[i]).upper()
    prm.update({'rnX': rnX, 'rnXo': dict(rnX), 'Ap': Ap, 'cerr': cerr, 'pn': pn, 'rootnegP': False, 'bpRw': (bP * e[0]).upper(),
                'wnP2': ZERO, 'tm1': (pn * e[0] * vac['sp']).upper()})
    return prm


def merge_rows(rowsA, rowsT):
    """pk22 option (a): rows with lo from option (a)'s chain and the central value from the exact chain; head = CM.head(v_true, lo_a).
    Returns (merged rows, keys only in A, keys only in T)."""
    vt = {(r[0], tuple(r[1])): r[4] for r in rowsT}
    outr, onlyA = [], []
    for r in rowsA:
        k_ = (r[0], tuple(r[1]))
        if k_ not in vt:
            onlyA.append(k_)
            continue
        outr.append((r[0], r[1], CM.head(vt[k_], r[3]), r[3], vt[k_], r[5]))
    ka = set((r[0], tuple(r[1])) for r in rowsA)
    onlyT = [k_ for k_ in vt if k_ not in ka]
    return outr, onlyA, onlyT


def bp_piece(chV, jlo, ce_lo, alpha, trb):
    """beta_perp(float) at a piece (kt_s8hp_v1_1's inputs): rho_1 the largest |Ritz value| of S' on W', kappa = (N-1)/2 - c_lo, eps_H =
    c_N / J_lo; returns (beta_perp, kappa rho_1^2, eps_H rho_1^2 + TRB_H - alpha, rho_1, kappa, eps_H)."""
    rho1 = max(abs(x) for x in jacobi_eig([[float(x.mid()) for x in row] for row in chV['R']]))
    kap = (N - 1) / 2.0 - float(ce_lo)
    epsH = CN / float(jlo)
    return bperp(kap, rho1, epsH, trb, alpha) + (rho1, kap, epsH)


# ---- v2: the two-chain pair form (DESIGN v1_2 sect. 5.1)
T_M = {4: 3, 3: 2}[N]                  # P2-11's MIXED threshold (EXPORT_KT_S9H_v1 FLOAT-PASS)
NEAR_H = tuple(range(0, T_M + 1))      # horizontal slots i (gap i + 1, exponent i - 1 < T_M)
NEAR_V = tuple(range(-1, T_M))         # vertical slots d (exponent d < T_M)
DF_V, DF_H = T_M, T_M + 1              # the first far slot of each edge type


def vecs2(chL, chR, dL, dR, kind):
    """S8's vecs with the left pair from chL and the right pair from chR (mirrored by kind with chR's parities)."""
    K, pi = chR['K'], chR['pi']
    L1, LX = chL['L'][dL]
    if dR == 'inf':
        R1, RY = (ONE, [ZERO] * K), (chR['c'], list(chR['B']['TM' if kind == 'same' else 'MB']))
    else:
        R1, RY = chR['L'][dR][0], CM.mirror(chR['L'][dR][1], kind, pi)
    return L1, LX, R1, RY


def cov2_2(chL, chR, dL, dR, kind, Rk):
    """S8's cov2 on vecs2."""
    L1, LX, R1, RY = vecs2(chL, chR, dL, dR, kind)
    K = chL['K']
    q = lambda a, b: CM.dot(a, CM.mv(Rk, b))
    z, xy, x1, y1 = q(L1[1], R1[1]), q(LX[1], RY[1]), q(LX[1], R1[1]), q(L1[1], RY[1])
    AL = [L1[0] * LX[1][k] - LX[0] * L1[1][k] for k in range(K)]
    AR = [R1[0] * RY[1][k] - RY[0] * R1[1][k] for k in range(K)]
    num = q(AL, AR) + (z * xy - x1 * y1)
    Zz = L1[0] * R1[0] + z
    return num, Zz, AL, AR, (z, xy, x1, y1), (L1, LX, R1, RY)


def sf_pair2(chL, prmL, chR, prmR, dL, dR, kind, m, RkC, parity=True):
    """S8's sf_pair (float chains: no dual branch, no info record, zero off) with the left pair and its residuals from (chL, prmL) and the
    right pair and its residuals from (chR, prmR); R and the lemma's fields from the left (the T-chain's, common). The k = 0 parity
    shortcut needs the same objects on both sides (S8's single chain); otherwise it is off. Same operations in the same order as
    sf_pair, so (chV, prmV) on both sides gives sf_pair's balls exactly (C-MIXED-REG)."""
    k = m - 1
    if k not in RkC:
        RkC[k] = CM.mpow(chL['R'], k)
    num, Zz, AL, AR, (z, xy, x1, y1), (L1, LX, R1, RY) = cov2_2(chL, chR, dL, dR, kind, RkC[k])
    R = chL['R']
    rn1L, rnXL, rnXoL = prmL['rn1'], prmL['rnX'], prmL['rnXo']
    rn1R, rnXR = prmR['rn1'], prmR['rnX']
    ALp, ARp = prmL['Ap'][dL], prmR['Ap'][dR]
    ALW, ARW = CM.norm_up(AL), CM.norm_up(AR)
    dAL, dAR = CM.dvec(prmL, dL, L1, LX), CM.dvec(prmR, dR, R1, RY)
    r1k = CM.ipow(prmL['Rn'], k)
    e1L, eXL = prmL['cerr'][dL][0], prmL['cerr'][dL][1]
    e1R, eXR = prmR['cerr'][dR][0], prmR['cerr'][dR][1]
    lbv = lambda aW, da, aP, bW, db, bP: CM.lemma(k, prmL, R, aW, da, aP, bW, db, bP)
    ce = lambda aWn, da, bWn, db: (r1k * (da * bWn + aWn * db + da * db)).upper()
    t1s = lbv(AL, dAL, ALp, AR, dAR, ARp) + ce(ALW, dAL, ARW, dAR)
    if k == 0 and parity and chL is chR and prmL is prmR and dR != 'inf' and dL == dR:
        mo = (abs(L1[0]) * rnXoL[dL]).upper()
        mo = mo if mo < ALp else ALp
        t1 = ZERO if kind == 'same' else mo * mo
    else:
        t1 = lbv(AL, dAL, ALp, AR, dAR, ARp)
    t1 = t1 + ce(ALW, dAL, ARW, dAR)
    nL1, nLX, nR1, nRY = CM.norm_up(L1[1]), CM.norm_up(LX[1]), CM.norm_up(R1[1]), CM.norm_up(RY[1])
    dz = lbv(L1[1], e1L, rn1L[dL], R1[1], e1R, rn1R[dR]) + ce(nL1, e1L, nR1, e1R)
    dxy = lbv(LX[1], eXL, rnXL[dL], RY[1], eXR, rnXR[dR]) + ce(nLX, eXL, nRY, eXR)
    dx1 = lbv(LX[1], eXL, rnXL[dL], R1[1], e1R, rn1R[dR]) + ce(nLX, eXL, nR1, e1R)
    dy1 = lbv(L1[1], e1L, rn1L[dL], RY[1], eXR, rnXR[dR]) + ce(nL1, e1L, nRY, eXR)
    az, axy, ax1, ay1 = abs(z).upper(), abs(xy).upper(), abs(x1).upper(), abs(y1).upper()
    ddet = (az * dxy + axy * dz + dz * dxy + ax1 * dy1 + ay1 * dx1 + dx1 * dy1).upper()
    num_lo = (num.lower() - t1 - ddet).lower()
    num_hi = (num.upper() + t1s + ddet).upper()
    zhi = (abs(Zz).upper() + dz).upper()
    zlo = (abs(Zz).lower() - dz).lower()
    if num_lo >= 0:
        cov_lo = (num_lo / (zhi * zhi)).lower()
    else:
        cov_lo = (num_lo / (zlo * zlo)).lower() if zlo > 0 else CM.NEGINF
    if num_hi >= 0:
        cov_hi = (num_hi / (zlo * zlo)).upper() if zlo > 0 else CM.POSINF
    else:
        cov_hi = (num_hi / (zhi * zhi)).upper()
    v = float((num / (Zz * Zz)).mid())
    nAL = CM.hyp(ALW + dAL, ALp)
    nl = CM.hyp(nL1 + e1L, rn1L[dL])
    nx = CM.hyp(nLX + eXL, rnXL[dL])
    return v, cov_lo, num_lo, zhi, nAL, nl, nx, cov_hi


def dk_class2(chL, prmL, chR, prmR, dk, dL, dR, kind, far_spec=None, kmax=400):
    """S8's dk_class with the left pair from (chL, prmL) and the right pair from (chR, prmR). far_spec for dR = 'far': ('V', first far
    slot) is S8's vertical far branch (S8's dk_class with that slot in DFAR's place), ('H', first far slot) dk_class_h's horizontal one
    (exponents d - 1 and d + 1, no c term)."""
    far = dR == 'far'
    dRr = 'inf' if far else dR
    L1, LX, R1, RY = vecs2(chL, chR, dL, dRr, kind)
    K = chL['K']
    AL = [L1[0] * LX[1][k] - LX[0] * L1[1][k] for k in range(K)]
    AR = [R1[0] * RY[1][k] - RY[0] * R1[1][k] for k in range(K)]
    rn1L, rnXL, cerrL = prmL['rn1'], prmL['rnX'], prmL['cerr']
    rn1R, rnXR, cerrR = prmR['rn1'], prmR['rnX'], prmR['cerr']
    ALp, ARp = prmL['Ap'][dL], prmR['Ap'][dRr]
    dAL, dAR = CM.dvec(prmL, dL, L1, LX), CM.dvec(prmR, dRr, R1, RY)
    dfar, Dc = ZERO, ZERO
    nl = CM.hyp(CM.norm_up(L1[1]) + cerrL[dL][0], rn1L[dL])
    nx = CM.hyp(CM.norm_up(LX[1]) + cerrL[dL][1], rnXL[dL])
    if far:
        ftyp, dRf = far_spec
        if ftyp == 'V':
            eR = (prmR['Rw'] * CM.ipow(prmR['rho1'], dRf)).upper()
            eR1 = (prmR['Rw'] * CM.ipow(prmR['rho1'], dRf + 1)).upper()
            pn = prmR['pn']
            dfar = (prmR['BN'] * eR + pn * eR * eR1).upper()
            Dc = (2 * nl * eR1 * nx * (pn + dfar + prmR['cc'] * eR1)).upper()
        else:
            eR = (prmR['Rw'] * CM.ipow(prmR['rho1'], dRf - 1)).upper()
            eR1 = (prmR['Rw'] * CM.ipow(prmR['rho1'], dRf + 1)).upper()
            pn = prmR['pn']
            dfar = (prmR['BN'] * eR + pn * eR * eR1).upper()
            Dc = (2 * nl * eR1 * nx * (pn + dfar)).upper()
    elif dR != 'inf':
        nlr = CM.hyp(CM.norm_up(R1[1]) + cerrR[dR][0], rn1R[dR])
        nyr = CM.hyp(CM.norm_up(RY[1]) + cerrR[dR][1], rnXR[dR])
        Dc = (2 * nl * nlr * nx * nyr).upper()
    nAL = CM.hyp(CM.norm_up(AL) + dAL, ALp)
    nAR = (CM.hyp(CM.norm_up(AR) + dAR, ARp) + dfar).upper()
    k1, ko = dk['k1'], dk['ko']
    ua = (CM.SQ2 * dk['s1'] * nAL + dAL).upper()
    ub = (CM.SQ2 * dk['s1'] * nAR + dAR + dfar).upper()
    a, b = AL[k1], AR[k1]
    same_sign = (a.lower() > 0 and b.lower() > 0) or (a.upper() < 0 and b.upper() < 0)
    if not dk['ok'] or not same_sign or not abs(a).lower() > ua or not abs(b).lower() > ub:
        return None, arb(-1), arb(-1), arb(-1), a, b, ua, ub
    alo, blo = (abs(a).lower() - ua).lower(), (abs(b).lower() - ub).lower()
    P = (alo * blo).lower()
    O = ((abs(AL[ko]).upper() + CM.SQ2 * dk['so'] * nAL + dAL) * (abs(AR[ko]).upper() + CM.SQ2 * dk['so'] * nAR + dAR + dfar)).upper()
    Rr = (CM.sqrt_up(nAL * nAL - alo * alo) * CM.sqrt_up(nAR * nAR - blo * blo)).upper()
    Rk = lambda k: (P - CM.ipow(dk['qo'], k) * O - CM.ipow(dk['qr'], k) * Rr - CM.ipow(dk['qd'], k) * Dc).lower()
    k0 = next((k for k in range(kmax + 1) if Rk(k) > 0), None)
    return k0, P, Rk(CM.MM), Rk(CM.M1), a, b, ua, ub


def s1_rows(chL, prmL, chR, prmR, dL, kind, RkC, ftyp, DFx, mi0, mf0, tag):
    """the inf rows and the one-end-far rows of a mixed class with the near edge (chL, prmL) at the left: the right edge at infinity
    (its chain's bulk vector) and far from DFx on (S8's far_lo2 for a vertical far edge, far_lo2_h for a horizontal one; route A, and
    route B where the slots DFx..DFx + 2 exist in the right prm, the larger lower end kept), each up to its own top-mode m0."""
    rows = []
    for m in range(1, CM.MM + 1):
        need_inf, need_far = (mi0 is None or m < mi0), (mf0 is None or m < mf0)
        if not (need_inf or need_far):
            continue
        base = sf_pair2(chL, prmL, chR, prmR, dL, 'inf', kind, m, RkC, parity=False)
        if need_inf:
            rows.append(('Minf', (tag, dL, 'inf', kind, m), CM.head(base[0], base[1]), base[1], base[0], base[7]))
        if not need_far:
            continue
        if ftyp == 'V':
            far = lambda dRx: CM.far_lo2(None, prmR, dL, kind, m, base, dRx)
        else:
            far = lambda dRx: far_lo2_h(chR, prmR, dL, kind, m, base, dRx)
        fa = far(DFx)
        lo1 = fa[1]
        if all((DFx + j) in prmR['rnX'] for j in (0, 1, 2)):
            loB = far(DFx + 3)[1]
            for j in (0, 1, 2):
                b = sf_pair2(chL, prmL, chR, prmR, dL, DFx + j, kind, m, RkC, parity=False)
                loB = b[1] if b[1] < loB else loB
            lo1 = lo1 if lo1 > loB else loB
        rows.append(('M1', (tag, dL, 'far', kind, m), CM.head(fa[0], lo1), lo1, fa[0], None))
    return rows


def rows_mixed(chH, prmH_, chV, prmV, m0o=None):
    """the MIXED rows (family, class, headroom, lo, v, hi) and the top-mode m0 per class. HV: the horizontal edge near at the left, the
    vertical at the right, two-sided (M2, n >= 6), far (M1) or at infinity (Minf); VH: the vertical edge near at the left, the horizontal
    far (M1) or at infinity (Minf). Kinds 'same' (t with a) and 'flip' (t with b)."""
    RkC = {}
    dk = CM.dk_setup(chV, prmV)
    m0 = {}
    rows = []
    mz = lambda r_: (r_[0] + 1) if r_[0] is not None else None
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            for dV in NEAR_V:
                m0[('HV', iH, dV, kind)] = mz(dk_class2(chH, prmH_, chV, prmV, dk, iH, dV, kind))
            m0[('HV', iH, 'inf', kind)] = mz(dk_class2(chH, prmH_, chV, prmV, dk, iH, 'inf', kind))
            m0[('HV', iH, 'far', kind)] = mz(dk_class2(chH, prmH_, chV, prmV, dk, iH, 'far', kind, ('V', DF_V)))
        for dV in NEAR_V:
            m0[('VH', dV, 'inf', kind)] = mz(dk_class2(chV, prmV, chH, prmH_, dk, dV, 'inf', kind))
            m0[('VH', dV, 'far', kind)] = mz(dk_class2(chV, prmV, chH, prmH_, dk, dV, 'far', kind, ('H', DF_H)))
    if m0o is not None:   # pk22 option (a): use the given thresholds
        m0 = dict(m0o)
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            for dV in NEAR_V:
                mm0 = m0[('HV', iH, dV, kind)]
                for m in range(1, CM.MM + 1):
                    if iH + dV + m + 3 < 5 or (mm0 is not None and m >= mm0):   # rcm5: n >= 5
                        continue
                    b = sf_pair2(chH, prmH_, chV, prmV, iH, dV, kind, m, RkC, parity=False)
                    rows.append(('M2', ('HV', iH, dV, kind, m), CM.head(b[0], b[1]), b[1], b[0], b[7]))
            rows += s1_rows(chH, prmH_, chV, prmV, iH, kind, RkC, 'V', DF_V, m0[('HV', iH, 'inf', kind)], m0[('HV', iH, 'far', kind)],
                            'HV')
        for dV in NEAR_V:
            rows += s1_rows(chV, prmV, chH, prmH_, dV, kind, RkC, 'H', DF_H, m0[('VH', dV, 'inf', kind)], m0[('VH', dV, 'far', kind)],
                            'VH')
    return rows, m0


# ---- pk24 RC reading (R-centred H-NORM; pk24/STATE.md, KEY IDEA RC). FLOAT DATA: a reading, not a certificate.
# B~ = S'(M_e - c)S' = kappa S'^2 - R exactly, kappa = (N-1)/2 - c, R = S'((N-1)/2 - M_e)S' >= 0 (Lemma R1: m(l) < (N-1)/2); SH4's
# H-NORM gives 0 <= Q0 R Q0 <= tau' with tau' = eps_H rho_1^2 + tr P' - alpha (the branch blp of beta_perp). Centred at tau'/2: for eps
# perpendicular to u, Q0 B~ eps = kappa S'^2 eps - (tau'/2) eps - Y eps with ||Y|| <= tau'/2; on the chain S'^2 eps(d) = eps(d + 2).
def opt_a_chain_mb(chH, prmV, bp, pnA, wA, vac, betaH):
    """pk24: opt_a_chain with the bb bulk vector mirrored, MB = F BH as in chain_h (v2d's MB is BHa unmirrored)."""
    ch = opt_a_chain(chH, prmV, bp, pnA, wA, vac, betaH)
    pi, K = ch['pi'], ch['K']
    tm_ = ch['B']['TM']
    ch['B'] = {'TM': tm_, 'MB': [tm_[k] if pi[k] > 0 else -tm_[k] for k in range(K)]}
    return ch


def rc_chain(chH, prmV, tauP, betaH, vac, wA, pnA, barh=0.0):
    """pk24 RC: the horizontal chain at slots i >= 2 and the bulk vector, with W'-parts
    y(i)_W = y(1)_W - kappa eps(1)_W + (tau'/2) eps(-1)_W + kappa eps(i)_W - (tau'/2) eps(i-2)_W + P_W' Y (eps(-1) - eps(i-2)),
    p_H,W = (y(1)_W - kappa eps(1)_W + (tau'/2) eps(-1)_W + P_W' Y eps(-1)) / l_u (l_u = <u, w-hat> at every level). The u-parts stay
    option (a')'s balls. Returns (chB: boxes, centre +- rho on every W'-component; chC: centres; rho: the Euclidean radius per slot and
    'inf')."""
    K = chH['K']
    e, rn1, cerrV = prmV['e'], prmV['rn1'], prmV['cerr']
    dmax = max(k for k in e if isinstance(k, int))
    L = chH['L']
    hh = chH['h']
    kap = arb(N - 1) / 2 - hh['c']
    half = CM.fr(Fraction(tauP)) / 2
    sp, s_ = vac['sp'], vac['s']
    lu = L[-1][0][0]
    lW = {d: L[d][0][1] for d in range(-1, 8)}
    y1 = L[1][1]
    base = [y1[1][k] - kap * lW[1][k] + half * lW[-1][k] for k in range(K)]
    cer = lambda d: cerrV[min(d, dmax)][0]
    rp1 = lambda d: (rn1[min(d, dmax)] + abs(lu).upper() * sp).upper()   # |(1 - P_W) eps(d)|; past dmax the last (larger) bound
    sK = CM.sqrt_up(arb(K))
    Lb, Lc, rho = dict(L), dict(L), {}
    fn = lambda v: CM.hyp(abs(v[0]).upper(), CM.norm_up(v[1]))
    bH_ = CM.fr(Fraction(barh))
    by1 = (bH_ * (fn(y1) + 2 * abs(hh['c']).upper() * fn(L[1][0]))).upper()   # rc2: a relative bar on hT and l(1)
    if barh > 0:
        rho[1] = by1
    for i in range(2, 8):
        cen = [base[k] + kap * lW[i][k] - half * lW[i - 2][k] for k in range(K)]
        dv = [lW[-1][k] - lW[i - 2][k] for k in range(K)]
        vW = (CM.norm_up(dv) + cer(-1) + cer(i - 2)).upper()
        vP = (rp1(-1) + rp1(i - 2)).upper()
        ee = e[min(i - 1, dmax)]
        au = abs(L[i - 2][0][0]).upper()
        r_u = (CM.fr(Fraction(wA)) * au + CM.fr(Fraction(pnA)) * ee).upper()
        alw = (sK * s_ * (r_u + abs(y1[0]).upper())).upper()   # place 2: the u-multiples' components along e_k
        r_ = (half * CM.hyp(vW, vP) + abs(kap).upper() * cer(i) + half * cer(i - 2) + alw).upper()
        r_ = (r_ + by1 + bH_ * (abs(kap).upper() * (fn(L[1][0]) + fn(L[i][0])) + half * (fn(L[-1][0]) + fn(L[i - 2][0])))).upper()
        rho[i] = r_
        Lc[i] = (L[i][0], (CM.pm(r_u), cen))
        Lb[i] = (L[i][0], (CM.pm(r_u), [x + CM.pm(r_) for x in cen]))
    pc = [x / lu for x in base]
    rinf = ((half * e[0] + sK * s_ * abs(y1[0]).upper()) / abs(lu).lower() + CM.fr(betaH) * sp).upper()
    rinf = (rinf + (by1 + bH_ * (abs(kap).upper() * fn(L[1][0]) + half * fn(L[-1][0]))) / abs(lu).lower()).upper()
    rho['inf'] = rinf
    pi = chH['pi']
    mir = lambda v: [v[k] if pi[k] > 0 else -v[k] for k in range(K)]
    BHb = [x + CM.pm(rinf) for x in pc]
    chB, chC = dict(chH), dict(chH)
    chB['L'], chC['L'] = Lb, Lc
    chB['B'], chC['B'] = {'TM': BHb, 'MB': mir(BHb)}, {'TM': list(pc), 'MB': mir(pc)}
    hb = dict(hh)
    hb.update({'BH': BHb, 'AHm': [[ZERO] * K for _k in range(K)], 'cu': CM.pm(CM.fr(Fraction(wA)).upper())})
    chB['h'] = hb
    chC['h'] = dict(hb, BH=list(pc))
    return chB, chC, rho


def rc_setup(chB, chH, prmV, betaH, tauP, pcH, vac, pnA, betaP):
    """pk24 RC: the residuals outside W, (1 - P_W) y(i) <= l_u pc_H + tm + kappa |(1-P_W) eps(i)| + (tau'/2)(|(1-P_W) eps(i-2)| +
    e[i-1]) at every slot i >= 1 (slot 1's W'-part stays exact from hT); otherwise as setup_p2a (kappa = wn = 0, no component error at
    slots i >= 2 beyond rho)."""
    prm = setup_h(chB, prmV, betaH, pcH, kw=False)
    L = chB['L']
    kap = abs(arb(N - 1) / 2 - chH['h']['c']).upper()
    half = CM.fr(Fraction(tauP)) / 2
    e, rn1 = prmV['e'], prmV['rn1']
    dmax = max(k for k in e if isinstance(k, int))
    lu = L[-1][0][0]
    sp = vac['sp']
    rp1 = lambda d: (rn1[min(d, dmax)] + abs(lu).upper() * sp).upper()
    y1n = CM.norm_up(chH['L'][1][1][1])
    pq = (y1n + CM.fr(betaP) * e[0]).upper()
    pq = pq if pq < CM.fr(Fraction(pnA)).upper() else CM.fr(Fraction(pnA)).upper()
    pn = CM.hyp((pq + CM.fr(betaH) * sp).upper(), pcH)
    rnX, Ap, cerr = prm['rnX'], prm['Ap'], prm['cerr']
    for i in range(1, dmax + 1):
        lu2 = abs(L[i - 2][0][0]).upper()
        tm = (pn * e[i - 1] * sp).upper()
        rnX[i] = (lu2 * pcH + tm + kap * rp1(i) + half * (rp1(i - 2) + e[i - 1])).upper()
        if i >= 2:
            cerr[i] = (cerr[i][0], ZERO, ZERO)
    for i in range(1, dmax + 1):
        Ap[i] = (abs(L[i][0][0]) * rnX[i] + abs(L[i][1][0]) * rn1[i]).upper()
    prm.update({'rnX': rnX, 'rnXo': dict(rnX), 'Ap': Ap, 'cerr': cerr, 'pn': pn, 'rootnegP': False, 'bpRw': (half * e[0]).upper(),
                'wnP2': ZERO, 'tm1': (pn * e[0] * sp).upper()})
    return prm


def frob_up(M):
    return CM.sqrt_up(sum((x * x for row in M for x in row), ZERO))


def sf_pair2_rc(chLb, chLc, rhoL, prmL, chRb, chRc, rhoR, prmR, dL, dR, kind, m, RkC, info=None):
    """pk24 RC: sf_pair2 (parity off) with Euclidean W'-balls on the insertion vectors. chXb carry boxes (centre +- rho per component)
    and give every residual term as sf_pair2 does; chXc carry the centres and give the main term, num = num_c + dL.gL + dR.gR + the
    bilinear term, with |dL| <= rhoL[dL], |dR| <= rhoR[dR] (a missing key: no W'-ball), gL = R^k (L1u AR + z RY - y1 R1) and
    gR = (R^k)^T (R1u AL + z LX - x1 L1) at the centres. Returns sf_pair2's tuple and the box reading's lower end."""
    k = m - 1
    if k not in RkC:
        RkC[k] = CM.mpow(chLb['R'], k)
    Rk = RkC[k]
    numb, Zz, ALb, ARb, (zb, xyb, x1b, y1b), (L1, LXb, R1, RYb) = cov2_2(chLb, chRb, dL, dR, kind, Rk)
    numc, Zc, AL, AR, (z, xy, x1, y1), (L1c, LX, R1c, RY) = cov2_2(chLc, chRc, dL, dR, kind, Rk)
    K = chLb['K']
    rL = rhoL.get(dL, ZERO)
    rR = rhoR.get(dR, ZERO)
    RkT = CM.mT(Rk)
    gL = CM.mv(Rk, [L1[0] * AR[j] + z * RY[1][j] - y1 * R1[1][j] for j in range(K)])
    gR = CM.mv(RkT, [R1[0] * AL[j] + z * LX[1][j] - x1 * L1[1][j] for j in range(K)])
    nRk = CM.ipow(prmL['Rn'], k).upper()
    fRk = frob_up(Rk)
    nRk = nRk if nRk < fRk else fRk
    bil = (rL * rR * (abs(L1[0] * R1[0] + z).upper() * nRk + CM.norm_up(CM.mv(Rk, R1[1])) * CM.norm_up(CM.mv(RkT, L1[1])))).upper()
    lin = (rL * CM.norm_up(gL) + rR * CM.norm_up(gR) + bil).upper()
    R = chLb['R']
    rn1L, rnXL, rn1R, rnXR = prmL['rn1'], prmL['rnX'], prmR['rn1'], prmR['rnX']
    ALp, ARp = prmL['Ap'][dL], prmR['Ap'][dR]
    ALW, ARW = CM.norm_up(ALb), CM.norm_up(ARb)
    dAL, dAR = CM.dvec(prmL, dL, L1, LXb), CM.dvec(prmR, dR, R1, RYb)
    r1k = CM.ipow(prmL['Rn'], k)
    e1L, eXL = prmL['cerr'][dL][0], prmL['cerr'][dL][1]
    e1R, eXR = prmR['cerr'][dR][0], prmR['cerr'][dR][1]
    lbv = lambda aW, da, aP, bW, db, bP: CM.lemma(k, prmL, R, aW, da, aP, bW, db, bP)
    ce = lambda aWn, da, bWn, db: (r1k * (da * bWn + aWn * db + da * db)).upper()
    t1 = lbv(ALb, dAL, ALp, ARb, dAR, ARp) + ce(ALW, dAL, ARW, dAR)
    nL1, nLX, nR1, nRY = CM.norm_up(L1[1]), CM.norm_up(LXb[1]), CM.norm_up(R1[1]), CM.norm_up(RYb[1])
    dz = lbv(L1[1], e1L, rn1L[dL], R1[1], e1R, rn1R[dR]) + ce(nL1, e1L, nR1, e1R)
    dxy = lbv(LXb[1], eXL, rnXL[dL], RYb[1], eXR, rnXR[dR]) + ce(nLX, eXL, nRY, eXR)
    dx1 = lbv(LXb[1], eXL, rnXL[dL], R1[1], e1R, rn1R[dR]) + ce(nLX, eXL, nR1, e1R)
    dy1 = lbv(L1[1], e1L, rn1L[dL], RYb[1], eXR, rnXR[dR]) + ce(nL1, e1L, nRY, eXR)
    az, axy, ax1, ay1 = abs(zb).upper(), abs(xyb).upper(), abs(x1b).upper(), abs(y1b).upper()
    ddet = (az * dxy + axy * dz + dz * dxy + ax1 * dy1 + ay1 * dx1 + dx1 * dy1).upper()
    num_lo = (numc.lower() - lin - t1 - ddet).lower()
    num_hi = (numc.upper() + lin + t1 + ddet).upper()
    numb_lo = (numb.lower() - t1 - ddet).lower()
    zhi = (abs(Zz).upper() + dz).upper()
    zlo = (abs(Zz).lower() - dz).lower()

    def clo(nl_):
        if nl_ >= 0:
            return (nl_ / (zhi * zhi)).lower()
        return (nl_ / (zlo * zlo)).lower() if zlo > 0 else CM.NEGINF
    cov_lo, covb_lo = clo(num_lo), clo(numb_lo)
    if num_hi >= 0:
        cov_hi = (num_hi / (zlo * zlo)).upper() if zlo > 0 else CM.POSINF
    else:
        cov_hi = (num_hi / (zhi * zhi)).upper()
    v = float((numc / (Zz * Zz)).mid())
    nAL = CM.hyp(ALW + dAL, ALp)
    nl = CM.hyp(nL1 + e1L, rn1L[dL])
    nx = CM.hyp(nLX + eXL, rnXL[dL])
    if info is not None:
        info.update({'numc': float(numc.mid()), 'lin': float(lin.mid()), 'linL': float((rL * CM.norm_up(gL)).mid()),
                     'linR': float((rR * CM.norm_up(gR)).mid()), 'boxerr': float((numb.mid() - numb.lower()).mid()),
                     't1': float(t1.mid()), 'ddet': float(ddet.mid()), 'zhi': float(zhi.mid()), 'ALp': float(ALp.mid()),
                     'ARp': float(ARp.mid())})
    return v, cov_lo, num_lo, zhi, nAL, nl, nx, cov_hi, covb_lo


def s1_rows_rc(cL, prmL, cR, prmR, dL, kind, RkC, ftyp, DFx, mi0, mf0, tag):
    """s1_rows on sf_pair2_rc; cL and cR are (chain with boxes, chain with centres, rho). Rows carry the box lower end as a 7th entry."""
    rows = []
    for m in range(1, CM.MM + 1):
        need_inf, need_far = (mi0 is None or m < mi0), (mf0 is None or m < mf0)
        if not (need_inf or need_far):
            continue
        base = sf_pair2_rc(cL[0], cL[1], cL[2], prmL, cR[0], cR[1], cR[2], prmR, dL, 'inf', kind, m, RkC)
        if need_inf:
            rows.append(('Minf', (tag, dL, 'inf', kind, m), CM.head(base[0], base[1]), base[1], base[0], base[7], base[8]))
        if not need_far:
            continue
        if ftyp == 'V':
            far = lambda dRx: CM.far_lo2(None, prmR, dL, kind, m, base, dRx)
        else:
            far = lambda dRx: far_lo2_h(cR[0], prmR, dL, kind, m, base, dRx)
        fa = far(DFx)
        lo1 = fa[1]
        if all((DFx + j) in prmR['rnX'] for j in (0, 1, 2)):
            loB = far(DFx + 3)[1]
            for j in (0, 1, 2):
                b = sf_pair2_rc(cL[0], cL[1], cL[2], prmL, cR[0], cR[1], cR[2], prmR, dL, DFx + j, kind, m, RkC)
                loB = b[1] if b[1] < loB else loB
            lo1 = lo1 if lo1 > loB else loB
        rows.append(('M1', (tag, dL, 'far', kind, m), CM.head(fa[0], lo1), lo1, fa[0], None, None))
    return rows


def rows_mixed_rc(cH, prmH_, chV, prmV, boxlo):
    """rows_mixed on the RC chain, cH = (chB, chC, rho); the top-mode m0 from dk_class2 on the boxes (each box contains its ball)."""
    chB = cH[0]
    cV = (chV, chV, {})
    RkC = {}
    dk = CM.dk_setup(chV, prmV)
    m0 = {}
    rows = []
    mz = lambda r_: (r_[0] + 1) if r_[0] is not None else None
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            for dV in NEAR_V:
                m0[('HV', iH, dV, kind)] = mz(dk_class2(chB, prmH_, chV, prmV, dk, iH, dV, kind))
            m0[('HV', iH, 'inf', kind)] = mz(dk_class2(chB, prmH_, chV, prmV, dk, iH, 'inf', kind))
            m0[('HV', iH, 'far', kind)] = mz(dk_class2(chB, prmH_, chV, prmV, dk, iH, 'far', kind, ('V', DF_V)))
        for dV in NEAR_V:
            m0[('VH', dV, 'inf', kind)] = mz(dk_class2(chV, prmV, chB, prmH_, dk, dV, 'inf', kind))
            m0[('VH', dV, 'far', kind)] = mz(dk_class2(chV, prmV, chB, prmH_, dk, dV, 'far', kind, ('H', DF_H)))
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            for dV in NEAR_V:
                mm0 = m0[('HV', iH, dV, kind)]
                for m in range(1, CM.MM + 1):
                    if iH + dV + m + 3 < 5 or (mm0 is not None and m >= mm0):   # rcm5: n >= 5
                        continue
                    b = sf_pair2_rc(cH[0], cH[1], cH[2], prmH_, chV, chV, {}, prmV, iH, dV, kind, m, RkC)
                    key = ('HV', iH, dV, kind, m)
                    boxlo[('M2', key)] = b[8]
                    rows.append(('M2', key, CM.head(b[0], b[1]), b[1], b[0], b[7]))
            for r in s1_rows_rc(cH, prmH_, cV, prmV, iH, kind, RkC, 'V', DF_V, m0[('HV', iH, 'inf', kind)],
                                m0[('HV', iH, 'far', kind)], 'HV'):
                boxlo[(r[0], r[1])] = r[6]
                rows.append(r[:6])
        for dV in NEAR_V:
            for r in s1_rows_rc(cV, prmV, cH, prmH_, dV, kind, RkC, 'H', DF_H, m0[('VH', dV, 'inf', kind)],
                                m0[('VH', dV, 'far', kind)], 'VH'):
                boxlo[(r[0], r[1])] = r[6]
                rows.append(r[:6])
    return rows, m0


def rows_h_rc(cH, prm, boxlo):
    """rows_h (every slot of DN) on the RC chain, cH = (chB, chC, rho); m0 from dk_class on the boxes."""
    chB = cH[0]
    RkC = {}
    dkf = CM.dk_setup(chB, prm)
    m0 = {}
    rows = []
    for kind in ('flip', 'same'):
        for dL in DN[kind]:
            r_ = CM.dk_class(chB, prm, dkf, dL, 'inf', kind)
            m0[(dL, 'inf', kind)] = (r_[0] + 1) if r_[0] is not None else None
            r_ = dk_class_h(chB, prm, dkf, dL, 'far', kind)
            m0[(dL, 'far', kind)] = (r_[0] + 1) if r_[0] is not None else None
            for dR in DN[kind]:
                r_ = CM.dk_class(chB, prm, dkf, dL, dR, kind)
                m0[(dL, dR, kind)] = (r_[0] + 1) if r_[0] is not None else None
    for kind in ('flip', 'same'):
        for dL in DN[kind]:
            for dR in DN[kind]:
                mm0 = m0[(dL, dR, kind)]
                for m in range(1, CM.MM + 1):
                    if dL + dR + m + 3 < 5 or (mm0 is not None and m >= mm0):   # rcm5: n >= 5
                        continue
                    b = sf_pair2_rc(cH[0], cH[1], cH[2], prm, cH[0], cH[1], cH[2], prm, dL, dR, kind, m, RkC)
                    boxlo[('H2', (dL, dR, kind, m))] = b[8]
                    rows.append(('H2', (dL, dR, kind, m), CM.head(b[0], b[1]), b[1], b[0], b[7]))
            mm0 = m0[(dL, 'inf', kind)]
            mf0 = m0[(dL, 'far', kind)]
            for m in range(1, CM.MM + 1):
                base = sf_pair2_rc(cH[0], cH[1], cH[2], prm, cH[0], cH[1], cH[2], prm, dL, 'inf', kind, m, RkC)
                if mm0 is None or m < mm0:
                    boxlo[('Hinf', (dL, 'inf', kind, m))] = base[8]
                    rows.append(('Hinf', (dL, 'inf', kind, m), CM.head(base[0], base[1]), base[1], base[0], base[7]))
                if mf0 is not None and m >= mf0:
                    continue
                fa = far_lo2_h(cH[0], prm, dL, kind, m, base, DF[kind])
                loA = fa[1]
                loB = far_lo2_h(cH[0], prm, dL, kind, m, base, DF[kind] + 3)[1]
                for j in (0, 1, 2):
                    b = sf_pair2_rc(cH[0], cH[1], cH[2], prm, cH[0], cH[1], cH[2], prm, dL, DF[kind] + j, kind, m, RkC)
                    loB = b[1] if b[1] < loB else loB
                lo1 = loA if loA > loB else loB
                rows.append(('H1', (dL, 'far', kind, m), CM.head(fa[0], lo1), lo1, fa[0], None))
    return rows, m0


# ---- rcm6: the n = 5 two-sided keys and their P2-13 keys (the maps of pk22's C-REPRO-H and C-REPRO-M)
N5HV = ((0, 1, 1), (1, 0, 1), (2, -1, 1), (0, 0, 2), (1, -1, 2), (0, -1, 3))
N5H2 = ((0, 0, 2), (0, 1, 1), (1, 0, 1))
N5KEYS = ([('M2', ('HV', a_, b_, k_, m_)) for k_ in ('same', 'flip') for (a_, b_, m_) in N5HV]
          + [('H2', (a_, b_, k_, m_)) for k_ in ('flip', 'same') for (a_, b_, m_) in N5H2])


def n5key(fam, key):
    """rcm6: the P2-13 key of an n = 5 two-sided row (H2 (dL, dR, kind, m): t at column dL, the other edge at column 3 - dR;
    HV (iH, dV, kind, m): t at column iH, the vertical edge at column 3 - dV), else None."""
    if fam == 'M2' and key[0] == 'HV' and key[1] + key[2] + key[4] + 3 == 5:
        return 'S5,xy,%d,HT,%d,%s' % (key[1], 3 - key[2], 'TM' if key[3] == 'same' else 'MB')
    if fam == 'H2' and key[0] + key[1] + key[3] + 3 == 5:
        return 'S5,xy,%d,HT,%d,%s' % (key[0], 3 - key[1], 'HB' if key[2] == 'flip' else 'HT')
    return None


def rcsum(i, rA2, rM2, mrMB, mrP, mrRC, rRC, boxlo, cRC, prmRC, ev, blp, bpp, onA, onT):
    """pk24: the per-piece lines of the extra readings."""
    ok = lambda r: float(r[3].mid()) > 0 and r[2] >= 2.0
    rho = cRC[2]
    out('  RC piece %d: tau\'/2 %.6e (beta_perp %.6e); Euclidean rho slot 2 %.4e, slot 3 %.4e, inf %.4e; rnX slot 1 %.4e, slot 2 %.4e, '
        'slot 3 %.4e%s' % (i, 0.5 * float(blp), float(bpp), float(rho[2].mid()), float(rho[3].mid()), float(rho['inf'].mid()),
                            float(prmRC['rnX'][1].mid()), float(prmRC['rnX'][2].mid()), float(prmRC['rnX'][3].mid()),
                            ('; rows on one side only: RC %s, exact %s' % (onA[:4], onT[:4])) if (onA or onT) else ''))
    res = {}
    for tag, rows in (('A2-HH', rA2), ('MB-HH', rM2), ('MB-MIX', mrMB), ('RC-HH', rRC), ('RC-MIX', mrRC)):
        bad = [r for r in rows if not ok(r)]
        w = min(rows, key=lambda r: r[2]) if rows else None
        out('  %s piece %d: %d rows, failing %d, smallest headroom %s' % (tag, i, len(rows), len(bad),
                                                                         ('%.4g at %s %s' % (w[2], w[0], w[1])) if w else 'n/a'))
        res[tag] = bad
    for r in res['A2-HH'][:6]:
        out('  ROWA2 %s %s: lo %.6e, Cov %.6e, headroom %.4g' % (r[0], r[1], float(r[3].mid()), r[4], r[2]))
    for r in res['RC-HH'][:6] + res['RC-MIX'][:10]:
        bl = boxlo.get((r[0], r[1]))
        out('  ROWRC %s %s: lo %.6e (RC box %s), Cov %.6e, headroom %.4g' % (
            r[0], r[1], float(r[3].mid()), ('%.6e' % float(bl.mid())) if bl is not None else '-', r[4], r[2]))
    dA = {(r[0], r[1]): r for r in mrP}
    for r in mrRC:
        c_ = r[1]
        if c_[0] == 'HV' and c_[1] in (2, 3) and c_[3] == 'flip' and c_[4] <= 2:
            a = dA.get((r[0], c_))
            bl = boxlo.get((r[0], c_))
            out('  CMP %s %s: Cov %.6e; lo (a\') %s; RC box %s; RC %.6e; headroom (a\') %s -> RC %.4g' % (
                r[0], c_, r[4], ('%.6e' % float(a[3].mid())) if a else '-', ('%.6e' % float(bl.mid())) if bl is not None else '-',
                float(r[3].mid()), ('%.4g' % a[2]) if a else '-', r[2]))
    inf_ = {}
    sf_pair2_rc(cRC[0], cRC[1], cRC[2], prmRC, ev['chV'], ev['chV'], {}, ev['prmV'], 2, 'inf', 'flip', 1, {}, info=inf_)
    out('  DECOMP RC HV (2, inf, flip, 1): num_c %.6e; Euclidean W\' term %.4e (box reading: num ball half-width %.4e); residual term '
        't1 %.4e (ALp %.4e, ARp %.4e); ddet %.4e; zhi %.6f' % (inf_['numc'], inf_['lin'], inf_['boxerr'], inf_['t1'], inf_['ALp'],
                                                              inf_['ARp'], inf_['ddet'], inf_['zhi']))


def harm_check_rc(cH, prmH_, chV, prmV):
    """pk24: C-HARM-RC at t = 0 on sf_pair2_rc, for the MIXED classes of harm_check_m and the FLIP/SAME classes of harm_check (every
    slot of DN); the harmonic value must lie in [cov_lo, cov_hi] (slack 1e-12 relative). Returns (classes, failing, the largest
    lo / harmonic with its class)."""
    RkC = {}
    rows = []
    for kind in ('same', 'flip'):
        cls = []
        for iH in NEAR_H:
            cls += [('HV', iH, dV, kind, m) for dV in NEAR_V for m in range(1, 9) if iH + dV + m + 3 in (6, 7, 8)]
            cls += [('HV', iH, 'inf', kind, m) for m in range(1, 9)]
        for dV in NEAR_V:
            cls += [('VH', dV, 'inf', kind, m) for m in range(1, 9)]
        for (tg, a_, b_, k_, m_) in cls:
            if tg == 'HV':
                bb = sf_pair2_rc(cH[0], cH[1], cH[2], prmH_, chV, chV, {}, prmV, a_, b_, k_, m_, RkC)
            else:
                bb = sf_pair2_rc(chV, chV, {}, prmV, cH[0], cH[1], cH[2], prmH_, a_, b_, k_, m_, RkC)
            rows.append(((tg, a_, b_, k_, m_), bb, harm_m(tg, a_, b_, k_, m_)))
    for kind in ('flip', 'same'):
        for iL in DN[kind]:
            cls = [(iL, iR, kind, m) for iR in DN[kind] for m in range(1, 9) if iL + iR + m + 3 in (6, 7, 8)] + \
                  [(iL, 'inf', kind, m) for m in range(1, 9)]
            for (a_, b_, k_, m_) in cls:
                bb = sf_pair2_rc(cH[0], cH[1], cH[2], prmH_, cH[0], cH[1], cH[2], prmH_, a_, b_, k_, m_, RkC)
                rows.append((('H', a_, b_, k_, m_), bb, harm(a_, b_, k_, m_)))
    bad, worst = [], None
    for cl, bb, hv in rows:
        lo_, hi_ = float(bb[1].mid()), float(bb[7].mid())
        tol = 1e-12 * max(abs(hv), 1e-300)
        if not (lo_ - tol <= hv <= hi_ + tol):
            bad.append(cl)
        rr = lo_ / hv if hv != 0 else 0.0
        if worst is None or rr > worst[0]:
            worst = (rr, cl, lo_, hv, hi_)
    return len(rows), bad, worst


def rc_xw(V, H, t, chV, mains):
    """pk24 INFO: the W'-block of R = kappa S'^2 - B~ from the float two-vac entries, C ((N-1)/2 TT2 - N2T2) C^T rhob / lambda_0^2
    (CBP-2's matrix; c cancels); its eigenvalues against tau' (RC's premise is 0 <= Q0 R Q0 <= tau')."""
    rhoE, rmain, rho4, rhob, rhoH = mains
    K = chV['K']
    C, lam0, g00 = chV['C'], chV['lam0'], chV['g00']
    rng = range(K + 1)
    idx = list(range(1, K + 1))
    g = [[V[('g', min(a, b), max(a, b))] for b in rng] for a in rng]
    N2T = [[ser(H['N2T,%d,%d' % (min(a, b), max(a, b))], t) for b in rng] for a in rng]
    TT = [[ser(H['TT,%d,%d' % (min(a, b), max(a, b))], t) for b in rng] for a in rng]
    p2 = lambda M, a, b: M[a][b] - g[a][0] / g00 * M[0][b] - g[b][0] / g00 * M[a][0] + g[a][0] * g[b][0] / (g00 * g00) * M[0][0]
    X2 = [[arb(N - 1) / 2 * p2(TT, a, b) - p2(N2T, a, b) for b in idx] for a in idx]
    XW = [[x * rhob / (lam0 * lam0) for x in row] for row in CM.mmul(CM.mmul(C, X2), CM.mT(C))]
    return sorted(jacobi_eig([[float(x.mid()) for x in row] for row in XW]))


def rc_contain(chHex, cRC, prmEx):
    """pk24 INFO: |y_ex(i)_W - centre(i)| against rho(i) at slots 2..5 and for the bulk vector; y_ex from the exact float chain (two-vac
    entries), whose own W'-error bound at slot i (its cerr[i][1], the residual action it neglects) is printed beside."""
    res = []
    for i in (2, 3, 4, 5):
        ye = [float(x.mid()) for x in chHex['L'][i][1][1]]
        cc = [float(x.mid()) for x in cRC[1]['L'][i][1][1]]
        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(ye, cc)))
        res.append((i, d, float(cRC[2][i].mid()), float(prmEx['cerr'][i][1].mid())))
    be = [float(x.mid()) for x in chHex['h']['BH']]
    bc = [float(x.mid()) for x in cRC[1]['B']['TM']]
    d = math.sqrt(sum((a - b) ** 2 for a, b in zip(be, bc)))
    res.append(('inf', d, float(cRC[2]['inf'].mid()), 0.0))
    return res


# ---- pk24: the RC reading on certified inputs, per piece at its
# J_lo (the binding end, as the float scans): S8's certified chain and setup with real bars (piece_eval_RB of the certified engine
# v1_14_3, over the piece box), certified tau' (Jensen's alpha_lo at the certified c-box's upper end, TRB_H / (1 - eps_r)^2,
# eps_H = c_N t_max, rho_1 from the certified P2 row), pc_H from the certified Qvt_hi and box, c a fixed rational in the certified box,
# |v_i| capped by R_w, and absolute bars on the float horizontal entries (fT, hT; the 4-strip HT entries). FLOAT DATA: a reading.
def tau_cert(P2row, q, law, trb):
    """certified tau' (H-NORM's trace branch, 70e91b6e sect. 2.3 with B-1 and Jensen): eps_H rho_1^2 + TRB_H / (1 - eps_r)^2 - alpha_lo
    with eps_H = c_N t_max and alpha_lo = (N-1)/2 - c_hi (1 + (N-1) t_max / 2) + c_hi^2 t_max / 2 at the certified box's upper end c_hi.
    Gates: Jensen (c_hi < N - 1, c_hi < 1/t_max + (N-1)/2), B-3 (c_hi <= (N-1)/2 - c_N/300), the trace guard (TRB_H/(1-eps_r)^2 >=
    alpha_lo) and tau' > 0. Returns (tau' upper end, alpha_lo, gates)."""
    tmax = CM.fr(1 / Fraction(P2row['jlo']))
    chi = CM.fr(q['ce_hi'])
    A_ = arb(N - 1) / 2
    cN = CM.fr(Fraction(CN))
    rho1 = CM.fr(P2row['rho1_hi'])
    epsH = (cN * tmax).upper()
    alo = (A_ - chi * (1 + (N - 1) * tmax / 2) + chi * chi * tmax / 2).lower()
    er = CM.fr(Fraction(law['eps_r']))
    trp = (trb / ((1 - er) * (1 - er))).upper()
    tau = (epsH * rho1 * rho1 + trp - alo).upper()
    gates = {'J1': bool(chi.upper() < N - 1), 'J2': bool(chi.upper() < (1 / tmax + A_).lower()),
             'B3': bool(chi.upper() < (A_ - cN / 300).lower()), 'TR': bool(trp.lower() > alo.upper()), 'T0': bool(tau.lower() > 0)}
    return tau, alo, gates


def chain_h_fix(V, H, t, chV, mains, vac, betaH, cfix, barF, barS):
    """chain_h's slots 0 and 1, slot-0 norms and fields with c the fixed rational cfix (kappa = (N-1)/2 - cfix exactly) and no two-vac
    entry: slots >= 2 and BH are placeholders that rc_chain_m replaces. Absolute bars: barF on every fT and hT entry, barS on the
    4-strip HT entries (the float tables carry none; the certified M3 entries will)."""
    rhoE, rmain, rho4, rhob, rhoH = mains
    K = chV['K']
    C, lam0, g00 = chV['C'], chV['lam0'], chV['g00']
    sg = g00.sqrt()
    rng = range(K + 1)
    idx = list(range(1, K + 1))
    g = [[V[('g', min(a, b), max(a, b))] for b in rng] for a in rng]
    e = [V[('e', a)] for a in rng]
    bF, bS = CM.pm(CM.fr(Fraction(barF))), CM.pm(CM.fr(Fraction(barS)))
    fT = [ser(H['fT,%d' % a], t) + bF for a in rng]
    hT = [ser(H['hT,%d' % a], t) + bF for a in rng]

    def comps(vec, scale):
        return [scale * sum((C[k][i] * (vec[n] - g[n][0] / g00 * vec[0]) for i, n in enumerate(idx)), ZERO) for k in range(K)]
    c = CM.fr(cfix)
    s = vac['s']

    def allow(v):
        a_ = (s * abs(v[0]).upper()).upper()
        return (v[0], [x + CM.pm(a_) for x in v[1]])
    L = dict(chV['L'])
    raw = {0: allow((rhoE * fT[0] / (lam0 * e[0]), comps(fT, rhoE * sg / (lam0 * e[0])))),
           1: allow((rhoH * hT[0] / (lam0 * lam0 * e[0]), comps(hT, rhoH * sg / (lam0 * lam0 * e[0]))))}
    for i in (0, 1):
        l = chV['L'][i][0]
        x = raw[i]
        L[i] = (l, (x[0] - c * l[0], [x[1][k] - c * l[1][k] for k in range(K)]))
    for i in range(2, 8):
        L[i] = (chV['L'][i][0], (ZERO, [ZERO] * K))
    ch = dict(chV)
    ch['L'] = L
    ch['c'] = ZERO
    ch['B'] = {'TM': [ZERO] * K, 'MB': [ZERO] * K}
    ch.pop('dual', None)   # rcm3: the vertical chain's dual run must not reach a horizontal row
    Z4 = V[('Z4',)]
    X1H, X12H = ser(H['S4,x,0,HT'], t) + bS, ser(H['S4,xy,0,HT,2,HT'], t) + bS
    F4 = rho4 * g00 / (lam0 * lam0 * e[0] * e[0])
    n2y = F4 * (X12H - 2 * c * X1H + c * c * Z4)
    n21 = F4 * Z4
    crs = F4 * (X1H - c * Z4)
    l0, y0 = L[0]
    lu, yu = l0[0], y0[0]
    sq = lambda v: v[0] * v[0] + sum((x * x for x in v[1]), ZERO)
    ap2 = lu * lu * (n2y - yu * yu) - 2 * lu * yu * (crs - yu * lu) + yu * yu * (n21 - lu * lu) - \
        sum(((lu * y0[1][k] - yu * l0[1][k]) * (lu * y0[1][k] - yu * l0[1][k]) for k in range(K)), ZERO)
    ch['h'] = {'c': c, 'AHm': [[ZERO] * K for _k in range(K)], 'BH': [ZERO] * K, 'cu': ZERO, 'res2y0': n2y - sq(y0), 'ny0': n2y,
               'Ap2y0': ap2, 'umain': ZERO}
    return ch


def rc_chain_m(chH, prmV, tau_b, betaH, vac, w_b, pn_b):
    """rc_chain with certified balls for tau', the c-box width w and pn_SH4, and |v_i| capped by R_w (its upper end e[0])."""
    K = chH['K']
    e, rn1, cerrV = prmV['e'], prmV['rn1'], prmV['cerr']
    dmax = max(k for k in e if isinstance(k, int))
    L = chH['L']
    hh = chH['h']
    kap = arb(N - 1) / 2 - hh['c']
    half = tau_b / 2
    sp, s_ = vac['sp'], vac['s']
    lu = L[-1][0][0]
    lW = {d: L[d][0][1] for d in range(-1, 8)}
    y1 = L[1][1]
    base = [y1[1][k] - kap * lW[1][k] + half * lW[-1][k] for k in range(K)]
    cer = lambda d: cerrV[min(d, dmax)][0]
    rp1 = lambda d: (rn1[min(d, dmax)] + abs(lu).upper() * sp).upper()
    sK = CM.sqrt_up(arb(K))
    Lb, Lc, rho = dict(L), dict(L), {}
    for i in range(2, 8):
        cen = [base[k] + kap * lW[i][k] - half * lW[i - 2][k] for k in range(K)]
        dv = [lW[-1][k] - lW[i - 2][k] for k in range(K)]
        vW = (CM.norm_up(dv) + cer(-1) + cer(i - 2)).upper()
        vP = (rp1(-1) + rp1(i - 2)).upper()
        vn = CM.hyp(vW, vP)
        vn = vn if vn.upper() < e[0].upper() else e[0]
        ee = e[min(i - 1, dmax)]
        au = abs(L[i - 2][0][0]).upper()
        r_u = (w_b * au + pn_b * ee).upper()
        alw = (sK * s_ * (r_u + abs(y1[0]).upper())).upper()
        r_ = (half * vn + abs(kap).upper() * cer(i) + half * cer(i - 2) + alw).upper()
        rho[i] = r_
        Lc[i] = (L[i][0], (CM.pm(r_u), cen))
        Lb[i] = (L[i][0], (CM.pm(r_u), [x + CM.pm(r_) for x in cen]))
    pc = [x / lu for x in base]
    rinf = ((half * e[0] + sK * s_ * abs(y1[0]).upper()) / abs(lu).lower() + CM.fr(betaH) * sp).upper()
    rho['inf'] = rinf
    pi = chH['pi']
    mir = lambda v: [v[k] if pi[k] > 0 else -v[k] for k in range(K)]
    BHb = [x + CM.pm(rinf) for x in pc]
    chB, chC = dict(chH), dict(chH)
    chB['L'], chC['L'] = Lb, Lc
    chB['B'], chC['B'] = {'TM': BHb, 'MB': mir(BHb)}, {'TM': list(pc), 'MB': mir(pc)}
    hb = dict(hh)
    hb.update({'BH': BHb, 'AHm': [[ZERO] * K for _k in range(K)], 'cu': CM.pm(w_b)})
    chB['h'] = hb
    chC['h'] = dict(hb, BH=list(pc))
    return chB, chC, rho


def rc_setup_m(chB, chH, prmV, betaH, tau_b, pcH, vac, pn_b):
    """rc_setup with certified tau' and pn_SH4 (the top-mode factor pn = hyp(pn_SH4 + beta_H s', pc_H))."""
    prm = setup_h(chB, prmV, betaH, pcH, kw=False)
    L = chB['L']
    kap = abs(arb(N - 1) / 2 - chH['h']['c']).upper()
    half = tau_b / 2
    e, rn1 = prmV['e'], prmV['rn1']
    dmax = max(k for k in e if isinstance(k, int))
    lu = L[-1][0][0]
    sp = vac['sp']
    rp1 = lambda d: (rn1[min(d, dmax)] + abs(lu).upper() * sp).upper()
    pn = CM.hyp((pn_b + CM.fr(betaH) * sp).upper(), pcH)
    rnX, Ap, cerr = prm['rnX'], prm['Ap'], prm['cerr']
    for i in range(1, dmax + 1):
        lu2 = abs(L[i - 2][0][0]).upper()
        tm = (pn * e[i - 1] * sp).upper()
        rnX[i] = (lu2 * pcH + tm + kap * rp1(i) + half * (rp1(i - 2) + e[i - 1])).upper()
        if i >= 2:
            cerr[i] = (cerr[i][0], ZERO, ZERO)
    for i in range(1, dmax + 1):
        Ap[i] = (abs(L[i][0][0]) * rnX[i] + abs(L[i][1][0]) * rn1[i]).upper()
    prm.update({'rnX': rnX, 'rnXo': dict(rnX), 'Ap': Ap, 'cerr': cerr, 'pn': pn, 'rootnegP': False, 'bpRw': (half * e[0]).upper(),
                'wnP2': ZERO, 'tm1': (pn * e[0] * sp).upper()})
    return prm


def same_val(a, b):
    """exact equality of two returned values: None, ints, floats (nan equal to nan) or balls (equal midpoints and radii; non-finite balls
    by their printed form)."""
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, (int, float)) or isinstance(b, (int, float)):
        return bool(a == b) or (a != a and b != b)
    fa = math.isfinite(float(a.mid())) and math.isfinite(float(a.rad()))
    fb = math.isfinite(float(b.mid())) and math.isfinite(float(b.rad()))
    if fa and fb:
        return bool(a.mid() == b.mid() and a.rad() == b.rad())
    return str(a) == str(b)


def mixed_reg(chV, prmV):
    """C-MIXED-REG (a)-(d) on one piece's vertical chain; returns (comparisons, mismatches)."""
    dk = CM.dk_setup(chV, prmV)
    chC, prmC = dict(chV), dict(prmV)
    R1, R2, R3 = {}, {}, {}
    ncmp, bad = 0, []
    eq = lambda x, y: len(x) == len(y) and all(same_val(p_, q_) for p_, q_ in zip(x, y))
    for kind in ('flip', 'same'):
        for dL in CM.DNEAR[kind]:
            for dR in list(CM.DNEAR[kind]) + ['inf']:
                for m in range(1, CM.MM + 1):
                    s8a = CM.sf_pair(chV, prmV, dL, dR, kind, m, R1)
                    v2a = sf_pair2(chV, prmV, chV, prmV, dL, dR, kind, m, R2, parity=True)
                    s8b = CM.sf_pair(chV, prmV, dL, dR, kind, m, R1, parity=False)
                    v2b = sf_pair2(chV, prmV, chC, prmC, dL, dR, kind, m, R3, parity=False)
                    for lab, x, y in (('a', s8a, v2a), ('b', s8b, v2b)):
                        ncmp += 1
                        if not eq(x, y):
                            bad.append((lab, dL, dR, kind, m))
                    if dR == 'inf':
                        ncmp += 1
                        if not eq(CM.far_lo2(chV, prmV, dL, kind, m, s8a, CM.DFAR[kind]),
                                  CM.far_lo2(None, prmV, dL, kind, m, v2a, CM.DFAR[kind])):
                            bad.append(('d', dL, dR, kind, m))
            for dR in list(CM.DNEAR[kind]) + ['inf', 'far']:
                ncmp += 1
                if not eq(CM.dk_class(chV, prmV, dk, dL, dR, kind), dk_class2(chV, prmV, chV, prmV, dk, dL, dR, kind, ('V', CM.DFAR[kind]))):
                    bad.append(('c', dL, dR, kind))
    return ncmp, bad


def harm_m(tag, dL, dR, kind, m):
    """(N - 1) T^2 / 2 for a mixed class: HV two-sided on its own strip (the vertical at column n - dR - 2), HV or VH at infinity on a
    64-column strip (inner columns dL + 1 and dL + 1 + m)."""
    vb = 'TM' if kind == 'same' else 'MB'
    hb = 'HT' if kind == 'same' else 'HB'
    if tag == 'HV':
        if dR == 'inf':
            T_ = strip_T(64, (dL, 'HT'), (dL + 1 + m, vb))
        else:
            n = dL + dR + m + 3
            T_ = strip_T(n, (dL, 'HT'), (n - dR - 2, vb))
    else:
        T_ = strip_T(64, (dL + 1, 'TM'), (dL + 1 + m, hb))
    return (N - 1) * T_ * T_ / 2.0


def harm_check_m(chH, prmH_, chV, prmV, record=None):
    """C-HARM-H-M at t = 0: HV two-sided classes at n = 6..8, HV and VH at infinity (m = 1..8), both kinds; the harmonic value must lie
    in [cov_lo, cov_hi] (float rounding slack 1e-12 relative). Returns (classes, failing)."""
    RkC = {}
    cls = []
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            cls += [('HV', iH, dV, kind, m) for dV in NEAR_V for m in range(1, 9) if iH + dV + m + 3 in (6, 7, 8)]
            cls += [('HV', iH, 'inf', kind, m) for m in range(1, 9)]
        for dV in NEAR_V:
            cls += [('VH', dV, 'inf', kind, m) for m in range(1, 9)]
    bad = []
    for (tg, a_, b_, k_, m_) in cls:
        if tg == 'HV':
            bb = sf_pair2(chH, prmH_, chV, prmV, a_, b_, k_, m_, RkC, parity=False)
        else:
            bb = sf_pair2(chV, prmV, chH, prmH_, a_, b_, k_, m_, RkC, parity=False)
        hv = harm_m(tg, a_, b_, k_, m_)
        lo_, hi_ = float(bb[1].mid()), float(bb[7].mid())
        tol = 1e-12 * max(abs(hv), 1e-300)
        if not (lo_ - tol <= hv <= hi_ + tol):
            bad.append((tg, a_, b_, k_, m_))
        if record is not None:
            record.append(((tg, a_, b_, k_, m_), bb[0], hv, lo_, hi_))
    return len(cls), bad


def zero_res(prm):
    """PLANT-RES-M: a copy of prm with every slot residual (rnX, rnXo, rn1, Ap at integer slots) set to 0."""
    q = dict(prm)
    for key in ('rnX', 'rnXo', 'rn1', 'Ap'):
        q[key] = {k: (ZERO if isinstance(k, int) else v) for k, v in prm[key].items()}
    return q


try:
    A = mod.run_A([], [], plants=False)
    HENT = load_json_entries()
    BETA = beta_h()
    HZ = hz_rows()
    out('INPUTS: beta_H = %s (J-uniform, row T, N%d); %d horizontal entries; pk15 Qvt rows %d (CERTIFIED export b05b09ad)' % (
        float(BETA), N, len(HENT), len(HZ)))
    i0 = A['RSTART'][N]
    grid = [i0] if PHASE == 'smoke' else sorted(set([i0, i0 + 1, i0 + 10, i0 + 40, 150, 250, 400, 600, 800, 903]))
    badg = [i for i in range(mod.NPIECES) if abs(HZ[i]['jlo'] - float(A['pieces'][N][i]['jlo'])) > 1e-9 * max(1.0, HZ[i]['jlo'])]
    out('C-GRID: pk15\'s export and S8\'s pieces share every J_lo (%d pieces): differing %s -> %s' % (
        mod.NPIECES, badg[:5] or 'none', gate('C-GRID', not badg)))
    # ---- controls at t = 0 (the harmonic limit)
    P0 = A['pieces'][N][mod.NPIECES - 1]
    vac0 = zero_vac(mod.vac_from_law(mod.law_at(A, N, P0['jlo']), P0['Bp_hi']))
    t0 = ZERO
    U0 = mod.u_poly(A['s4u'], N, t0).upper()
    pc0 = CM.fr(HZ[mod.NPIECES - 1]['Qvt'])
    ev0 = piece(A, mod.NPIECES - 1, t0, vac0, U0, BETA, pc0)
    if ev0 is None:
        raise ValueError('no route (b) tau_B at t = 0')
    hh0 = ev0['chH']['h']
    out('C-UMAIN t=0 (INFO): TT00 rhob / (g00 lambda_0^2) = %.15f; c = N2T00/TT00 = %.12f' % (float(hh0['umain'].mid()), float(hh0['c'].mid())))
    exact0 = float(CM.sqrt_up(hh0['res2y0']).mid()) <= 1e-10 * float(CM.sqrt_up(hh0['ny0']).mid())
    out('SPAN t=0: slot 0 residual %.3e of its norm %.6f -> slot 0 %s (fixed before C-HARM-H); slot 1 is Option A (containment)' % (
        float(CM.sqrt_up(hh0['res2y0']).mid()), float(CM.sqrt_up(hh0['ny0']).mid()), 'span-exact' if exact0 else 'not exact'))

    def harm_check(ev, tag, record):
        chH, prmH = ev['chH'], ev['prmH']
        RkC = {}
        n_eq, n_ct, bad_eq, bad_ct, worst = 0, 0, [], [], 0.0
        for kind in ('flip', 'same'):
            for iL in DN[kind]:
                cls = [(iL, iR, kind, m) for iR in DN[kind] for m in range(1, 9) if iL + iR + m + 3 in (6, 7, 8)] + \
                      [(iL, 'inf', kind, m) for m in range(1, 9)]
                for (a_, b_, k_, m_) in cls:
                    bb = CM.sf_pair(chH, prmH, a_, b_, k_, m_, RkC, parity=False)
                    hv = harm(a_, b_, k_, m_)
                    lo_, hi_ = float(bb[1].mid()), float(bb[7].mid())
                    exact_cls = exact0 and 1 not in (a_, b_) and b_ != 'inf' and max(a_, b_) == 0
                    if exact_cls:
                        n_eq += 1
                        rel = abs(bb[0] - hv) / max(abs(hv), 1e-300)
                        worst = max(worst, rel)
                        if rel > 1e-8:
                            bad_eq.append((a_, b_, k_, m_))
                    else:
                        n_ct += 1
                        tol = 1e-12 * max(abs(hv), 1e-300)
                        if not (lo_ - tol <= hv <= hi_ + tol):
                            bad_ct.append((a_, b_, k_, m_))
                    if record is not None:
                        record.append(((a_, b_, k_, m_), bb[0], hv, lo_, hi_))
        return n_eq, n_ct, bad_eq, bad_ct, worst
    rec0 = []
    ne, nc, be, bc, wq = harm_check(ev0, 't0', rec0)
    out('C-HARM-H t=0: %d equality classes (largest relative difference %.2e, tolerance 1e-8): failing %s -> %s; %d containment classes '
        '(the harmonic value in [cov_lo, cov_hi]): failing %s -> %s' % (ne, wq, be[:6] or 'none', gate('C-HARM-H', not be), nc,
                                                                      bc[:6] or 'none', gate('C-HARM-H', not bc)))
    for (cl, v_, hv, lo_, hi_) in rec0[:12]:
        out('HARM %s: chain %.9e, harmonic %.9e, [%.6e, %.6e]' % (cl, v_, hv, lo_, hi_))
    # v1_1: PLANT-RES-H with slot 1's residual removed (x 0) is the gate; x 0.1 and x 0.01 are INFO (how loose Option A is at t = 0)
    for sc in (0.1, 0.01):
        evq = piece(A, mod.NPIECES - 1, t0, vac0, U0, BETA, pc0, scale1=sc)
        _, _, _, bcq, _ = harm_check(evq, 'plant', None)
        out('INFO PLANT-RES-H x %g: containment fails for %d classes (%s)' % (sc, len(bcq), bcq[:4]))
    evp = piece(A, mod.NPIECES - 1, t0, vac0, U0, BETA, pc0, scale1=0.0)
    _, _, _, bcp, _ = harm_check(evp, 'plant', None)
    out('PLANT-RES-H: slot 1 residual x 0 at t = 0: containment fails for %d classes (%s) -> %s' % (
        len(bcp), bcp[:4], 'FIRES' if bcp else 'DOES NOT FIRE'))
    if not bcp:
        fails.append('PLANT-RES-H')
    if exact0:
        eve = piece(A, mod.NPIECES - 1, t0, vac0, U0, BETA, pc0, end_bulk=True)
        nee, _, bee, _, _ = harm_check(eve, 'plant', None)
        out('PLANT-END-H: the bulk vector in slot 0 at t = 0: equality fails for %d of %d exact classes -> %s' % (
            len(bee), nee, 'FIRES' if bee else 'DOES NOT FIRE'))
        if not bee:
            fails.append('PLANT-END-H')
    else:
        out('PLANT-END-H: N/A (no span-exact class at t = 0, so C-HARM-H has no equality gate to plant)')
    # ---- C-REPRO-H at the first piece: n = 5 classes against P2-13's exact float values
    P1 = A['pieces'][N][i0]
    t1 = arb(1) / CM.fr(Fraction(P1['jlo']))
    vac1 = mod.vac_from_law(mod.law_at(A, N, P1['jlo']), P1['Bp_hi'])
    U1 = mod.u_poly(A['s4u'], N, t1).upper()
    q1 = HZ[i0]
    pc1 = (CM.fr(q1['Qvt']) + (CM.fr(q1['ce_hi']) - CM.fr(q1['ce_lo'])) * vac1['sp']).upper()
    ev1 = piece(A, i0, t1, vac1, U1, BETA, pc1)
    L13 = json.load(open(P13L))
    img = {}
    for en in L13['entries']:
        for k_ in [en['key']] + list(en.get('images', [])):
            img[k_.split(' ')[0]] = en['key']
    pv = {}
    for p in P13O[N]:
        for ln in open(p).read().split('\n'):
            mm = re.match(r'^PAIR (\S+) N=%d .*Cov\*J\^2 a_k \[([^\]]*)\]' % N, ln)
            if mm:
                pv[mm.group(1)] = [float(x) for x in mm.group(2).split(',')]
    tf = float(t1.mid())
    nrep, badrep = 0, []
    if ev1 is not None:
        RkC = {}
        for kind in ('flip', 'same'):
            for (a_, b_, m_) in ((0, 0, 2), (0, 1, 1), (1, 0, 1)):
                if a_ not in DN[kind] or b_ not in DN[kind]:
                    continue
                cR = 5 - 2 - b_
                key = 'S5,xy,%d,HT,%d,%s' % (a_, cR, 'HB' if kind == 'flip' else 'HT')
                ck = img.get(key)
                if ck is None or ck not in pv:
                    badrep.append('%s: no P2-13 value' % key)
                    continue
                exact = sum(c_ * tf ** j for j, c_ in enumerate(pv[ck]))
                bb = CM.sf_pair(ev1['chH'], ev1['prmH'], a_, b_, kind, m_, RkC, parity=False)
                lo_, hi_ = float(bb[1].mid()), float(bb[7].mid())
                nrep += 1
                ok = lo_ <= exact <= hi_
                out('REPRO %s (class %s, %s): exact %.9e, chain %.9e, [%.6e, %.6e] -> %s' % (key, ck, kind, exact, bb[0], lo_, hi_,
                                                                                         'inside' if ok else 'OUTSIDE'))
                if not ok:
                    badrep.append(key)
    out('C-REPRO-H piece %d (J_lo %.6g): %d n = 5 classes inside [cov_lo, cov_hi] of P2-13\'s exact value: failing %s -> %s' % (
        i0, P1['jlo'], nrep, badrep or 'none', gate('C-REPRO-H', nrep > 0 and not badrep)))
    # ---- v2: reading P2 at t = 0, C-HARM-H under P2, C-HARM-H-M (A, P2) and PLANT-RES-M; C-P2-REG and C-REPRO-M at the first piece
    trb = float(BETA)
    c0 = float(hh0['c'].mid())
    alpha = (N - 1) / 2.0 - c0
    chV0 = ev0['chV']
    rho0 = max(abs(x) for x in jacobi_eig([[float(x.mid()) for x in row] for row in chV0['R']]))
    bp0, bu0, bl0 = bperp(alpha, rho0, 0.0, trb, alpha)
    out('INPUTS v2: T_M %d (NEAR_H %s, NEAR_V %s, DF_V %d, DF_H %d); c_N %.4f; alpha = (N-1)/2 - c(t = 0) = %.9f; TRB_H %.6f; t = 0: '
        'rho_1 %.9f, beta_perp %.6e = max(%.6e, %.6e)' % (T_M, NEAR_H, NEAR_V, DF_V, DF_H, CN, alpha, trb, rho0, bp0, bu0, bl0))
    prmP2_0 = setup_p2(ev0['chH'], ev0['prmV'], BETA, Fraction(bp0), pc0, vac0)
    _, ncP, _, bcP, _ = harm_check(dict(ev0, prmH=prmP2_0), 'P2', None)
    out('C-HARM-H P2 t=0: %d FLIP/SAME classes under reading P2, the harmonic value in [cov_lo, cov_hi]: failing %s -> %s' % (
        ncP, bcP[:6] or 'none', gate('C-HARM-H-P2', not bcP)))
    recM = []
    ncA, bdA = harm_check_m(ev0['chH'], ev0['prmH'], chV0, ev0['prmV'], recM)
    out('C-HARM-H-M t=0 (A, beta_H): %d mixed classes, the harmonic value in [cov_lo, cov_hi]: failing %s -> %s' % (
        ncA, bdA[:6] or 'none', gate('C-HARM-H-M', not bdA)))
    for (cl, v_, hv, lo_, hi_) in recM[:10]:
        out('HARMM %s: chain %.9e, harmonic %.9e, [%.6e, %.6e]' % (cl, v_, hv, lo_, hi_))
    ncP2, bdP2 = harm_check_m(ev0['chH'], prmP2_0, chV0, ev0['prmV'])
    out('C-HARM-H-M t=0 (P2): %d mixed classes: failing %s -> %s' % (ncP2, bdP2[:6] or 'none', gate('C-HARM-H-M-P2', not bdP2)))
    ncZ, bdZ = harm_check_m(ev0['chH'], zero_res(prmP2_0), chV0, zero_res(ev0['prmV']))
    out('PLANT-RES-M: every slot residual of both chains set to 0 at t = 0: containment fails for %d of %d mixed classes (%s) -> %s' % (
        len(bdZ), ncZ, bdZ[:4], 'FIRES' if bdZ else 'DOES NOT FIRE'))
    if not bdZ:
        fails.append('PLANT-RES-M')
    # ---- pk24: the RC reading at t = 0 against the harmonic strip (C-HARM-RC), its plant (tau' = 0), and the W'-block of R
    wA0 = float(HZ[mod.NPIECES - 1]['ce_hi']) - float(HZ[mod.NPIECES - 1]['ce_lo'])
    pnA0 = math.sqrt(max(alpha * bl0, 0.0))
    cRC0 = rc_chain(ev0['chH'], ev0['prmV'], bl0, BETA, vac0, wA0, pnA0)
    prmRC0 = rc_setup(cRC0[0], ev0['chH'], ev0['prmV'], BETA, bl0, pc0, vac0, pnA0, bp0)
    nR0, bR0, wR0 = harm_check_rc(cRC0, prmRC0, chV0, ev0['prmV'])
    out('C-HARM-RC t=0: %d MIXED and FLIP/SAME classes under RC, the harmonic value in [cov_lo, cov_hi]: failing %s -> %s; largest '
        'lo/harmonic %.6f at %s (lo %.6e, harmonic %.6e, hi %.6e)' % (nR0, bR0[:6] or 'none', gate('C-HARM-RC', not bR0), wR0[0], wR0[1],
                                                                      wR0[2], wR0[3], wR0[4]))
    cRCp = rc_chain(ev0['chH'], ev0['prmV'], 0.0, BETA, vac0, wA0, pnA0)
    prmRCp = rc_setup(cRCp[0], ev0['chH'], ev0['prmV'], BETA, 0.0, pc0, vac0, pnA0, bp0)
    nRp, bRp, wRp = harm_check_rc(cRCp, prmRCp, chV0, ev0['prmV'])
    out('PLANT-RC: tau\' = 0 (no centring and no Y ball) at t = 0: containment fails for %d of %d classes (%s) -> %s' % (
        len(bRp), nRp, bRp[:4], 'FIRES' if bRp else 'DOES NOT FIRE'))
    if not bRp:
        fails.append('PLANT-RC')
    xw0 = rc_xw(ev0['V'], HENT, t0, chV0, A['mains'][N])
    out('RCXW t=0: eigenvalues of the W\'-block of R %s against tau\' %.6e' % (' '.join('%.4e' % x for x in xw0), bl0))
    cnt0 = rc_contain(ev0['chH'], cRC0, setup_p2(ev0['chH'], ev0['prmV'], BETA, Fraction(bp0), pc0, vac0))
    out('RCIN t=0: |y_ex - centre| / rho: %s' % '; '.join('%s %.3e/%.3e (exact chain own error %.3e)' % (a, b, c, d) for a, b, c, d in cnt0))
    if ev1 is not None:
        bp1 = bp_piece(ev1['chV'], P1['jlo'], q1['ce_lo'], alpha, trb)
        pA_ = setup_p(ev1['chH'], ev1['prmV'], BETA, Fraction(bp1[0]), pc1)
        pB_ = setup_p2(ev1['chH'], ev1['prmV'], BETA, Fraction(bp1[0]), pc1, dict(vac1, s=ZERO, sp=ZERO))
        regok = all(same_val(pA_[key][d], pB_[key][d]) for key in ('rnX', 'Ap') for d in pA_[key]) and same_val(pA_['wn'], pB_['wnP2'])
        out('C-P2-REG piece %d: setup_p2 with s = s\' = 0 against setup_p (rnX and Ap at every slot, wn), ball for ball -> %s' % (
            i0, gate('C-P2-REG', regok)))
        prmP2_1 = setup_p2(ev1['chH'], ev1['prmV'], BETA, Fraction(bp1[0]), pc1, vac1)
        out('P2 piece %d: beta_perp %.6e; top-mode term pn R_w s\' %.3e (s\' %.3e, s %.3e, pn %.4e); wn\' %.6e against wn %.6e' % (
            i0, bp1[0], float(prmP2_1['tm1'].mid()), float(vac1['sp'].mid()), float(vac1['s'].mid()), float(prmP2_1['pn'].mid()),
            float(prmP2_1['wnP2'].mid()), float(pA_['wn'].mid())))
        nrm, badrm, RkM = 0, [], {}
        for kind in ('same', 'flip'):
            for (iH, dV, m_) in ((0, 1, 1), (1, 0, 1), (2, -1, 1), (0, 0, 2), (1, -1, 2), (0, -1, 3)):
                key = 'S5,xy,%d,HT,%d,%s' % (iH, 3 - dV, 'TM' if kind == 'same' else 'MB')
                ck = img.get(key)
                if ck is None or ck not in pv:
                    badrm.append('%s: no P2-13 value' % key)
                    continue
                exact = sum(c_ * tf ** j for j, c_ in enumerate(pv[ck]))
                for tagp, prmx in (('A', ev1['prmH']), ('P2', prmP2_1)):
                    bb = sf_pair2(ev1['chH'], prmx, ev1['chV'], ev1['prmV'], iH, dV, kind, m_, RkM, parity=False)
                    lo_, hi_ = float(bb[1].mid()), float(bb[7].mid())
                    nrm += 1
                    ok = lo_ <= exact <= hi_
                    out('REPROM %s %s (class %s, %s): exact %.9e, chain %.9e, [%.6e, %.6e] -> %s' % (
                        tagp, key, ck, kind, exact, bb[0], lo_, hi_, 'inside' if ok else 'OUTSIDE'))
                    if not ok:
                        badrm.append('%s %s' % (tagp, key))
        out('C-REPRO-M piece %d: %d mixed n = 5 rows (A and P2) inside [cov_lo, cov_hi] of P2-13\'s exact value: failing %s -> %s' % (
            i0, nrm, badrm or 'none', gate('C-REPRO-M', nrm > 0 and not badrm)))
    else:
        gate('C-P2-REG', False)
        gate('C-REPRO-M', False)
    # ---- pk24 scan: RC on certified inputs (rcm block header). Pieces: the first five of the range, then a spread to the last.
    gridm = sorted(set([i0 + j for j in range(10)] + [i0 + 20, i0 + 40, 150, 250, 400, 600, 800, 903]))
    conall = 0   # rcm4
    if PHASE == 'smoke':
        gridm = [i0]
    BARS = [(Fraction(1, 10000), Fraction(5, 100000)), (Fraction(3, 100000), Fraction(2, 100000)),
            (Fraction(3, 10000), Fraction(1, 10000)), (Fraction(1, 1000), Fraction(3, 10000)), (Fraction(0), Fraction(0))]
    trbF = CM.fr(BETA)
    mall, gfail = {}, []
    mall5, abs5 = {}, {}   # rcm6
    famkey = lambda f, x: (f, x[0], x[1][0] if f == 'M' else x[1][2])
    for i in gridm:
        r = mod.piece_eval_RB(N, A, i, rows=False)
        if r is None:
            out('M1PIECE %d: the certified piece_eval_RB gives no chain (law s, or no set with tau_B > 0); skipped' % i)
            gfail.append(i)
            continue
        P2row, vac, chU, prmV = r['P2row'], r['vac'], r['ch'], r['prm']
        q = HZ[i]
        law = mod.law_at(A, N, P2row['jlo'])
        tau_b, alo, gts = tau_cert(P2row, q, law, trbF)
        clo, chi = CM.fr(q['ce_lo']), CM.fr(q['ce_hi'])
        cfix = Fraction(int(round(float((q['ce_lo'] + q['ce_hi']) / 2) * 10 ** 9)), 10 ** 9)
        cin = bool(q['ce_lo'] <= cfix <= q['ce_hi'])
        w_b = (chi - clo).upper()
        pcH = (CM.fr(q['Qvt']) + w_b * vac['sp']).upper()
        kapS = (arb(N - 1) / 2 - clo).upper()
        pn_b = CM.sqrt_up((kapS * tau_b).upper())
        tp = arb(1) / CM.fr(Fraction(P2row['jlo']))
        V = CM.entry_vals(r['Ech'], tp)
        if not (all(gts.values()) and cin):
            gfail.append(i)
        bpF = Fraction(math.nextafter(float(tau_b.upper()), math.inf))
        chHe = chain_h(V, HENT, tp, chU, A['mains'][N], vac, BETA)
        chHe.pop('dual', None)   # rcm3: CM.sf_pair would read the vertical chain's dual run
        prmE = setup_p2(chHe, prmV, BETA, bpF, pcH, vac)
        if i == gridm[0]:   # rcm2: diagnostics at the first piece (INFO)
            fv = lambda x: '%.4e' % float(x.mid())
            fr_ = lambda x: '%.2e' % float(x.rad())
            out('  DIAG prmV (certified S8): sperp %s eta %s etap %s etam %s Rn %s r %s pc %s pn %s BN %s' % (
                fv(prmV['sperp']), fv(prmV['eta']), fv(prmV['etap']), fv(prmV['etam']), fv(prmV['Rn']), fv(prmV['r']), fv(prmV['pc']),
                fv(prmV['pn']), fv(prmV['BN'])))
            for d_ in (-1, 0, 1, 2, 3):
                out('  DIAG prmV d %d: rn1 %s rnX %s e %s cerr %s Ap %s' % (
                    d_, fv(prmV['rn1'][d_]), fv(prmV['rnX'][d_]), fv(prmV['e'][max(d_, 0)]),
                    '/'.join(fv(x) for x in prmV['cerr'][d_]), fv(prmV['Ap'][d_])))
            for d_ in (-1, 0, 1, 2):
                l_ = chU['L'][d_][0]
                out('  DIAG l(%d): u %s+-%s; W %s' % (d_, fv(l_[0]), fr_(l_[0]), ' '.join('%s+-%s' % (fv(x), fr_(x)) for x in l_[1])))
            for bF_, bS_ in ((Fraction(0), Fraction(0)), BARS[0]):
                chq = chain_h_fix(V, HENT, tp, chU, A['mains'][N], vac, BETA, cfix, bF_, bS_)
                for d_ in (0, 1):
                    y_ = chq['L'][d_][1]
                    out('  DIAG bar %g y(%d): u %s+-%s; W %s' % (float(bF_), d_, fv(y_[0]), fr_(y_[0]),
                                                               ' '.join('%s+-%s' % (fv(x), fr_(x)) for x in y_[1])))
                out('  DIAG bar %g slot 0: res2y0 %s+-%s, Ap2y0 %s+-%s' % (float(bF_), fv(chq['h']['res2y0']), fr_(chq['h']['res2y0']),
                                                                          fv(chq['h']['Ap2y0']), fr_(chq['h']['Ap2y0'])))
                cq = rc_chain_m(chq, prmV, tau_b, BETA, vac, w_b, pn_b)
                pq_ = rc_setup_m(cq[0], chq, prmV, BETA, tau_b, pcH, vac, pn_b)
                out('  DIAG bar %g RC prm: rnX %s; Ap %s; cerr0 %s' % (float(bF_), ' '.join('%d:%s' % (d_, fv(pq_['rnX'][d_])) for d_ in range(-1, 4)),
                                                                     ' '.join('%d:%s' % (d_, fv(pq_['Ap'][d_])) for d_ in range(-1, 4)),
                                                                     ' '.join('%d:%s' % (d_, fv(pq_['cerr'][d_][0])) for d_ in range(-1, 4))))
                for (a_, b_, k_, m_) in ((1, 1, 'flip', 2), (0, 'inf', 'same', 1), (0, 0, 'flip', 3), (1, 1, 'same', 1), (2, 2, 'flip', 1)):
                    inf_ = {}
                    bb = sf_pair2_rc(cq[0], cq[1], cq[2], pq_, cq[0], cq[1], cq[2], pq_, a_, b_, k_, m_, {}, info=inf_)
                    out('  DIAG bar %g row (%s, %s, %s, %d): lo %.6e hi %.6e v_RC %.6e; num_c %.4e lin %.3e t1 %.3e ddet %.3e zhi %.5f ALp %.3e '
                        'ARp %.3e boxerr %.3e' % (float(bF_), a_, b_, k_, m_, float(bb[1].mid()), float(bb[7].mid()), bb[0], inf_['numc'],
                                                  inf_['lin'], inf_['t1'], inf_['ddet'], inf_['zhi'], inf_['ALp'], inf_['ARp'], inf_['boxerr']))
        out('M1PIECE %d J_lo %.6g: tau\' %.6e (alpha_lo %.9f; gates %s), c_fix %s in the certified box [%.9f, %.9f]: %s; pc_H %.4e (Qvt_hi '
            '%.4e), w %.3e, pn_SH4 %.4e; S8 set %s, tau_B %.3e, R_w %.5f, rho_1 %.5f' % (
                i, P2row['jlo'], float(tau_b.mid()), float(alo.mid()), ' '.join('%s=%s' % (k, 'ok' if v else 'FAIL') for k, v in gts.items()),
                cfix, float(q['ce_lo']), float(q['ce_hi']), 'inside' if cin else 'OUTSIDE', float(pcH.mid()), float(q['Qvt']),
                float(w_b.mid()), float(pn_b.mid()), r.get('basis'), float(r['leak']['tau'].mid()), float(prmV['Rw'].mid()),
                float(prmV['rho1'].mid())))
        for bi, (bF, bS) in enumerate(BARS):
            chHf = chain_h_fix(V, HENT, tp, chU, A['mains'][N], vac, BETA, cfix, bF, bS)
            cR = rc_chain_m(chHf, prmV, tau_b, BETA, vac, w_b, pn_b)
            pR = rc_setup_m(cR[0], chHf, prmV, BETA, tau_b, pcH, vac, pn_b)
            bx = {}
            mr_, m0m = rows_mixed_rc(cR, pR, chU, prmV, bx)
            mrT, _ = rows_mixed(chHe, prmE, chU, prmV, m0o=m0m)
            mr, oa, ot = merge_rows(mr_, mrT)
            rh_, m0h = rows_h_rc(cR, pR, bx)
            rhT, _ = rows_h(chHe, prmE, m0o=m0h)
            rh, oa2, ot2 = merge_rows(rh_, rhT)
            rows = [('M', x) for x in mr] + [('H', x) for x in rh]
            bad = [(f, x) for f, x in rows if not (float(x[3].mid()) > 0 and x[2] >= 2.0)]
            wf, wx = min(rows, key=lambda z: z[1][2])
            out('  M1 bar (fT/hT %g, S4 HT %g) piece %d: rho slot 2 %.4e, slot 3 %.4e, inf %.4e; rnX slot 0 %.4e, slot 1 %.4e, slot 2 %.4e; '
                '%d rows, failing %d, smallest headroom %.4g at %s %s%s' % (
                    float(bF), float(bS), i, float(cR[2][2].mid()), float(cR[2][3].mid()), float(cR[2]['inf'].mid()),
                    float(pR['rnX'][0].mid()), float(pR['rnX'][1].mid()), float(pR['rnX'][2].mid()), len(rows), len(bad), wx[2], wx[0],
                    wx[1], ('; rows on one side only %s %s' % ((oa + oa2)[:3], (ot + ot2)[:3])) if (oa or ot or oa2 or ot2) else ''))
            mall.setdefault(bi, []).extend([(i, f, x) for f, x in rows])
            n5s = mall5.setdefault(bi, {})   # rcm6: this piece's n = 5 rows, and the n = 5 keys with no row (top-mode threshold m0)
            have = {}
            for f, x in rows:
                if n5key(x[0], x[1]) is not None:
                    have[(x[0], tuple(x[1]))] = x
            for k5 in N5KEYS:
                kk = (k5[0], tuple(k5[1]))
                if kk in have:
                    n5s.setdefault(kk, []).append((i, have[kk]))
                else:
                    m0x = m0m.get(k5[1][:4]) if k5[0] == 'M2' else m0h.get(k5[1][:3])
                    abs5.setdefault(bi, []).append((i, kk, m0x))
            if bi == 0 and i == gridm[0]:   # rcm6: C-REPRO-RC5, P2-13's exact n = 5 values against RC's [lo, hi]
                tf5 = float(tp.mid())
                n5c, n5b = 0, []
                for kk in sorted(have, key=str):
                    x = have[kk]
                    k5 = n5key(x[0], x[1])
                    ck = img.get(k5)
                    if ck is None or ck not in pv:
                        n5b.append('%s: no P2-13 value' % k5)
                        continue
                    ex = sum(c_ * tf5 ** j for j, c_ in enumerate(pv[ck]))
                    lo5, hi5 = float(x[3].mid()), float(x[5].mid())
                    ok5 = lo5 <= ex <= hi5
                    n5c += 1
                    out('  N5REPRO %s %s (P2-13 %s, class %s): exact %.9e, chain %.9e, RC [%.6e, %.6e] -> %s; headroom on the exact '
                        'value %.4g' % (x[0], x[1], k5, ck, ex, x[4], lo5, hi5, 'inside' if ok5 else 'OUTSIDE', CM.head(ex, x[3])))
                    if not ok5:
                        n5b.append(k5)
                out('C-REPRO-RC5 piece %d (J_lo %.6g): %d of %d n = 5 keys have a row; P2-13\'s exact value inside RC\'s [lo, hi]: '
                    'failing %s -> %s' % (i, P2row['jlo'], n5c, len(N5KEYS), n5b or 'none', gate('C-REPRO-RC5', n5c > 0 and not n5b)))
            if bi == 0:   # rcm4: the exact float chain's value against RC's [lo, hi]
                incs = [x for f, x in rows if float(x[3].mid()) > x[4] or (x[5] is not None and float(x[5].mid()) < x[4])]
                ratw = max([float(x[3].mid()) / x[4] for f, x in rows if x[4] > 0] or [0.0])
                out('  M1CONS piece %d: rows with the exact float value outside RC\'s [lo, hi] %d %s; largest lo/Cov %.4f' % (
                    i, len(incs), [(x[0], x[1]) for x in incs[:4]], ratw))
                conall += len(incs)
            if bi == 0:
                fm = {}
                for f, x in rows:
                    k_ = famkey(f, x)
                    if k_ not in fm or x[2] < fm[k_][2]:
                        fm[k_] = x
                out('  M1FAM piece %d: %s' % (i, '; '.join('%s %s %s %.4g' % (k_[1], k_[2], fm[k_][1], fm[k_][2]) for k_ in sorted(fm, key=str))))
                for f, x in bad[:12]:
                    out('  M1ROW %s %s: lo %.6e, Cov %.6e, headroom %.4g' % (x[0], x[1], float(x[3].mid()), x[4], x[2]))
    for bi, (bF, bS) in enumerate(BARS):
        rows = mall.get(bi, [])
        bad = [(i, f, x) for i, f, x in rows if not (float(x[3].mid()) > 0 and x[2] >= 2.0)]
        badc = sorted(set((x[0],) + tuple(x[1][:-1]) for i, f, x in bad), key=str)
        w_ = min(rows, key=lambda z: z[2][2]) if rows else None
        out('READING M1 bar (fT/hT %g, S4 HT %g)%s: %d of %d rows fail the rule; smallest headroom %s; failing classes %s' % (
            float(bF), float(bS), ' (primary)' if bi == 0 else ' (INFO)', len(bad), len(rows),
            ('%.4g at piece %d %s %s' % (w_[2][2], w_[0], w_[2][0], w_[2][1])) if w_ else 'n/a', badc or 'none'))
        if bi == 0:
            fm = {}
            for i, f, x in rows:
                k_ = famkey(f, x)
                if k_ not in fm or x[2] < fm[k_][1][2]:
                    fm[k_] = (i, x)
            for k_ in sorted(fm, key=str):
                i_, x = fm[k_]
                out('M1FAMILY %s %s %s: smallest headroom %.4g at piece %d, %s %s (lo %.6e, Cov %.6e)' % (
                    'MIXED' if k_[0] == 'M' else 'FLIP/SAME', k_[1], k_[2], x[2], i_, x[0], x[1], float(x[3].mid()), x[4]))
            cm = {}
            for i, f, x in rows:
                k_ = (x[0],) + tuple(x[1][:-1])
                if k_ not in cm or x[2] < cm[k_][1][2]:
                    cm[k_] = (i, x)
            for k_ in sorted(cm, key=str):
                i_, x = cm[k_]
                if x[2] < 4:
                    out('M1CLASS %s: smallest headroom %.4g at piece %d, m %d (lo %.6e, Cov %.6e)' % (k_, x[2], i_, x[1][-1], float(x[3].mid()),
                                                                                                 x[4]))
    for bi, (bF, bS) in enumerate(BARS):   # rcm6: every n = 5 two-sided key, its smallest headroom over the pieces
        n5s = mall5.get(bi, {})
        for k5 in N5KEYS:
            kk = (k5[0], tuple(k5[1]))
            if kk not in n5s:
                out('N5ROW bar (fT/hT %g, S4 HT %g) %s %s (P2-13 %s): no row on any piece' % (float(bF), float(bS), kk[0], kk[1],
                                                                                           n5key(kk[0], kk[1])))
                continue
            i_, x = min(n5s[kk], key=lambda z: z[1][2])
            nf = sum(1 for j_, y in n5s[kk] if not (float(y[3].mid()) > 0 and y[2] >= 2.0))
            out('N5ROW bar (fT/hT %g, S4 HT %g) %s %s (P2-13 %s): %d pieces, failing %d, smallest headroom %.4g at piece %d (lo %.6e, '
                'Cov %.6e)' % (float(bF), float(bS), kk[0], kk[1], n5key(kk[0], kk[1]), len(n5s[kk]), nf, x[2], i_, float(x[3].mid()),
                               x[4]))
        ab = abs5.get(bi, [])
        out('N5ABSENT bar (fT/hT %g, S4 HT %g): %d (piece, key, m0) with no row %s' % (float(bF), float(bS), len(ab), ab[:8]))
    out('M1 GATES: pieces with a failing gate, c_fix outside its box, or no certified chain: %s' % (gfail or 'none'))
    out('M1 CONSISTENCY (primary reading): rows with the exact float chain value outside RC\'s [lo, hi]: %d' % conall)
    if gfail:
        fails.append('M1-GATES')
except Exception as ex:
    out('ERROR %s: %s' % (type(ex).__name__, ex))
    for ln in traceback.format_exc().splitlines()[-14:]:
        out('TRACE ' + ln)
    fails.append('ERROR')
out('ITEM %s %s cpu %.1f s' % (ITEM, PHASE, cpu()))
out('VERDICT %s' % ('VALID' if not fails else 'INVALID (%s)' % ', '.join(sorted(set(fails)))))
