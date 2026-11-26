#!/usr/bin/env python3
"""kt_s67_cert_v2_2.py (no run without the approval naming this file's sha8) -- pk07 (code/pk07/).
v2_2 of kt_s67_cert_v2_1.py (98cde3a0; runs 42dd5429, 759af4b9), plan and the kbar argument in
FREEZE_NOTE_kt_s67_cert_v2_2.md:
  - (1) endw's r_main enters q as its matrix-tree enclosure in mp.iv (r_main_iv, moved out of C-HARM), not as the
    stored float; C-HARM keeps comparing the two, and PLANT-HARM swaps the closed-form conductances;
  - (2) m2's kbar is a free centering constant of the construction, not an input (the freeze note gives the
    argument from PK10_NOTES 19.5.1, 19.5.4, 19.6.2-3); C-KBAR gates kbar >= 0, u_h >= its centering term and t1 >= kbar (1 + eps_r),
    with PLANT-KBAR;
  - (3) the sweep writes a per-piece export for S8, EXPORT_KT_S67_v1 (S4U_KV_v1), with the J ends
    and pk11's 17 bounds (EXPORT_FIELDS) as directed decimals, the claimed pairs' Jensen and mode indices, the input tags with their
    status and EXPORT_STATUS; C-EXPORT reads it back with both S4U_KV_v1 readers and the sha-pinned producer's reader
    kt_s67_export_reader_v1.py before it is written, with PLANT-EXPORT; the run prints the export's sha256 for the importer's pin.
v2_1 of kt_s67_cert_v2.py (da3837e1; runs b04b2d1a, 5afcd1ce), plan in FREEZE_NOTE_kt_s67_cert_v2_1.md:
  - the S4-TRB provider for pk08's S4_TRB_CERTIFIED_v1 (91109301): C-HASH, C-FMT against the same S4U_KV_v1
    reference parser, C-SRC of N*_TRB, its pieces, PR and T_v against the READING lines of the sha-pinned asm outputs, PLANT-TSRC and
    PLANT-FMT-S4T; the tag 'CERTIFIED pk08 91109301' is set by provide_s4trb only. Ctx.TRB takes the record's N*_TRB, one constant
    per N for every J >= 300 (CONSTANT_PER_N); path A's reproductions keep the FLOAT TRB with the FLOAT U (float_s4). KR4 adds TRB
    (N*_TRB <= 1.02 x the FLOAT TRB, a gate), and C-TARGETS takes the certified TRB in place of its target;
  - N-a, C-TAG expects the run's tags to read CERTIFIED exactly when every input has a pin; N-c, the TARGETS line
    drops "S4-TRB, pending"; N-d, the scan's distances are stated as measured from the certified S4 values (INFO), also in the d = 3
    INFO line. M2 and M3 stay FLOAT (no pin) until pk02's records exist.
v2 (below) was written to pk11's plan PLAN_P2_CERT_FIXES_v1 (ca2637a7). Base: pk11's kt_s67_cert_v1_2.py (e7e973d0), which is v1_1 (b0b30114) with the d = 3 CLAIM
(NOTE1_d3, e64e90cf). v2 is the certified-item revision. It folds in the P2 review (ec33e7dd: F1, F2, S1-S3, N-a to N-c) and
d = 3 review (961b21b3: D1, D2, N-b). The changes, by item:
  - F1: a tag reads certified only as 'CERTIFIED <producer> <sha8>' with that input's pins (tag_certified, an allowlist). Only a
    provider sets it, after its C-HASH, C-FMT, C-SRC and C-POS pass. verdict_word gives CERTIFIED only when every tag is certified,
    FLOAT-PASS otherwise (P4's partial flips). PLANT-TAG has three cases: FLOAT tags, a non-FLOAT non-CERTIFIED tag ('S4-TRB,
    pending'), and a well-formed CERTIFIED tag with a wrong sha8.
  - F2: Ctx.U is U(t) = LEAD_HI (1 + C1_HI t + C2_HI t^2 + C3_HI t^3) + R_CERT per N, from pk08's S4_U_CERTIFIED_v2 (b1b6b99b, its
    CLAIM_F2 form), through provide_s4u. C-POS certifies LEAD_LO, C1_LO, C2_LO, C3_LO > 0, so the HI ends bound U3 from above for
    t > 0. The dual kind's derivative is LEAD_HI (C1_HI + 2 C2_HI t + 3 C3_HI t^2); R_CERT is a constant with zero derivative; point
    and dual kinds use the same polynomial. KR3 reads N*_QUAD_TW_PART. KR4 and an INFO line bound certified minus float U on every
    piece. The FLOAT U of PARAMS (trt2, rem(170)) stays only for path A's reproductions (C-REPRO, C-REPRO300, C-FLIP170: float_s4)
    and for that comparison.
  - S1, D2: self-calibrating margin plants on [300, 303]: per N for U (additive), R_w and TRB (scale factors) on S7, and at N = 4
    for the d = 3 binding direction (C_1 = c5 / F, bars x F; the loss is required of the flip d = 3 pair). F is the scan's bisected
    flip; each plant needs a hold at F / 1.1 and a loss at 1.1 F (margin_plant, shared, as ADD1's S5 plants). No flip in the
    bracket: DOES NOT FIRE.
  - S2: PLANT-PARITY sets one cross-parity coefficient of the symmetrized copy to 1e-12, and C-PARITY must flag it. C-PARITY gates
    once M3's tag is certified (INFO before).
  - S3: the S4-U reader of the port, with C-HASH, C-FMT against the separate sha-pinned reference parser s4u_kv_ref_v1.py (no shared
    code), C-SRC against s4c_m2ba's C-NORM / C-C123 lines (ball strings, exact *_LO / *_HI = mid -+ rad, R_CERT_RULE) and the plants
    PLANT-FMT-S4U, PLANT-KEYSWAP and PLANT-POS. M2's vacuum tuple and wt, dl, S4-TRB and M3's files keep their FLOAT PARAMS and tags
    until their formats are cited (SPEC sect. 3).
  - N-a: C-MODULE adds pt() and the S4-U provider, readers and tag functions. N-b: PLANT-MVB is judged on S5 Dd, where the bars
    enter at full weight. N-c: M3's tag stays FLOAT; its provider will need a key stating the bars for every J >= 300, t = 0 included.
  - D1: C-FLIP170 runs on the own claim (FLIP170_CLAIM) with C_1 = Cov_1 at [170, 171.7], whatever CLAIM is, and stays a gate;
    the d = 3 distances at [300, 303] are set beside NOTE1_d3's recorded run as INFO. N-b (d = 3): the label in the header and
    OUT_PATH come from this file's own name.
  - D-1, C-SRC also checks N*_PREF2_RE, N*_PREF2_RHO4 and N*_M3_SUM against the READING lines of
    their sha-pinned asm outputs, R_CERT as their exact sum and QUAD_TW_PART by its rule, with PLANT-RSRC; D-2, KR4 (and KR3) are
    gates in both items, and C-TARGETS runs with the certified U in place of its target; D-3, S4-TRB's future reader (comment at
    TAG_PINS); C-POS includes LEAD_LO, and Ctx.U says how the last piece meets t = 0; margin_plant states the search's
    bracket and tolerance; the record pinned is v2 b1b6b99b.
M6 P2: the port of Theorem S's S5 (Prop. 19.3, the binding pair), S6 (Prop. 19.5b) and S7 (Prop. 19.6) on J >= 300, N = 3, 4, per
SPEC_M6_S67_v1_2 (76e14cc3), which folds in the S5 addendum and the two reviews (5f1d091b, 3416f328).
S4-U and, since v2_1, S4-TRB enter through their certified providers. M3's entries and M2's vacuum stay FLOAT-tagged (today's J = 170
entries and parameters, as in P0), so the verdicts read FLOAT-PASS or FAIL until their providers exist (C-TAG).
Arithmetic (SPEC v1_1 sect. 2):
  - mp.iv with outward rounding for everything that enters a verdict;
  - float64 only for the eigh preconditioner (used as an exact matrix), the fixed index order (any choice is valid), the FLOAT providers
    (vac_float; the certified item replaces it) and INFO prints;
  - no numpy.linalg, no libm, no erfc, no fractional power in a verdict path, no python-flint (C-MODULE scans the sources);
  - M-d: finiteness asserts, and a nonnegative quantity whose enclosure lies below 0 stops the evaluation (nn); M-e probes at start
    and end.
Pieces: t = 1/J on [300, 400] at ratio 1.0025, on [400, 1e6] at ratio 1.01, and a last piece [0, 1e-6]. Endpoints are rounded outward:
  t_lo = (1/J_hi).a and t_hi = (1/J_lo).b (RV13_1 N1).
Centered forms (SPEC v1_2 sect. 2): for f in {rho^2, the L1 argument, the L2 argument, S5's even - odd}, f(P) is contained in
  F(t_m) + D(P)[-h, h]; for the three U-sensitive forms the bound used is the smaller of this upper end and the naive one (N-e), for S5
  the intersection of two true enclosures. Here:
  - F(t_m) is the naive value at the point t_m, with the bars; h covers t_m's distance to both ends of the piece;
  - D(P) is d f/dt by forward-mode interval differentiation (class D below), with value inputs c(P) + B and derivative inputs c'(P);
  - the four port conditions hold by construction: one bar box per piece, D(P) without derivatives for delta, the same function and
    constants in F(t_m) and D(P) (fixed index order, constant radius), and a kink or a non-finite D(P) falls back to the naive bound
    (counted, N-d).
  Smooth forms:
  - rho^2 uses sum_i A'_ii^2 (Schur);
  - L1 uses the fixed diagonal i0 and the fixed row iy with the constant radius R_y (N-d), mu_y = A'_yy - R_y. It is used only if
    C-ORDER holds on the whole piece and box: row iy certified as the minimizing Gershgorin row (F2), and A_00, mu_z and A'_yy - R_y
    positive (the form squares them);
  - L2 uses the 2 x 2 (i0, ix) interlacing bound, only if A_00 and mu_z are positive and mu_x's square-root argument stays positive
    (mu_x > 0 is asserted).
  The centered forms remove the t-dependency only; the bars enter F(t_m) at full weight.
Path A, the reference: the author's functions, sliced by line ranges and checked by sha256 before exec:
  - m2_unif3.py l.31-130;
  - endpairs4.py l.31-246;
  - assemble_binding_unif4.py l.19-35 (VQ, KAPPA, chi3, vac) and l.38-78 (item, cov_lower).
Controls, both items (gates unless INFO):
  - C-HASH, C-BLOCK, C-ENV;
  - the S4-U provider (F2, S3): C-HASH on the bytes it parses, C-FMT (the port's reader against the reference parser, every key; the
    header keys as pinned), C-SRC (s4c_m2ba's lines), C-POS; PLANT-FMT-S4U, PLANT-KEYSWAP, PLANT-POS; INFO U at t = 1/300 and t -> 0;
  - C-REPRO at [170, 171.7]: path A rebuilds the author's printed lines (m2_unif3, endpairs4 "J = 170", assemble_unif4) and the review's
    coverage lines; path B (naive enclosures, the author's forms, path A's FLOAT U) equals A to 1e-10 on every S5, S6 and S7 quantity and on all 24
    coverage pairs; path B with the production forms (RV13_1 N3) never beats A beyond 1e-12 (R+, rho, rho1, c_x, c5). This one-sided
    test applies to the naive enclosures: the centered forms are tighter by design and are checked by C-MV and C-PIECE instead.
    PLANT-S2UP (S2_even from the upper ends) fires through the one-sided test, not through the R+/rho check (SPEC v1_1 sect. 4 has it
    backwards: upper ends make rho smaller, so the R+/rho check passes more easily). PLANT-PATHB (sp = 0) fires through the two-sided test;
  - C-C2: the central S5 assembly at t = 0 equals c2 = (N-1)T^2/2 to 1e-10; PLANT-ODDSIGN, PLANT-T;
  - C-HARM (matrix-tree r_main, q^2(t=0)), C-IP3 (a_0, a_1, a_2 to 1e-12);
  - C-PARITY on the cross-parity Gram entries g(0,2), g(1,2), g(2,3): INFO while M3's tag is FLOAT, as today's files are
    unsymmetrized, a gate once it is certified; its control (a symmetrized copy passes) and PLANT-PARITY (S2: the symmetrized copy with
    one coefficient set to 1e-12 must fail) gate. A_2 is the genuine odd amplitude (0.132 at N = 4), not a parity zero, so ADD1 sect. 2's
    mention of it is left out;
  - C-MODULE (source scan of the verdict-path functions and classes; PLANT-MODULE), C-TAG (wording control with control pins;
    PLANT-TAG's three cases, F1);
  - C-FMT (S2): the port's reader against the author's item() on every stored entry; PLANT-FMT (a copy with two coefficient lists
    swapped).
Item sweep: every piece of [300, inf), both N, S5 first (its per-piece c5 is S7's C_1 at m = 1), then S6 and S7 with the interval pass
  tests (the claim check: the first mode success k <= KMAX, then Jensen for m = 1..k with Dm1 < 1) and the Lemma S7-mono (a) hypotheses;
  C-MV on every piece (4 smooth forms x 9 points); C-REPRO300 on every 100th piece and the last; on the binding pieces C-PIECE
  (term-level, naive: halves inside the parent, the parent around its end and midpoint values, no final bound outward beyond 1e-15),
  C-UNIF and C-MV-B (the gradient-sign corners of B); PLANT-RIGHTEND (C-UNIF and C-PIECE), PLANT-MV, PLANT-MVB (B = 0 in F(t_m); it
  must fail S5 Dd, N-b); INFO at the first and last pieces, and the fallback counts; KR1, KR5a (c5 > 0 part), KR5b.
Item scan: distances to flip at [300, 303] (P0's binding width; S5, S6 and S7, both N, naive enclosures) and at the last piece (joint,
  bars, U, TRB); the margin plants from those flips (S1: U, R_w, TRB on S7, both N; D2: C_1 and bars at N = 4 against the flip d = 3
  pair); ADD1's S5 plants (N_delta bar, TRB: S5 holds at F/1.1 and fails at 1.1F); C-FLIP170 (the claim and distances to 1%; D1)
  with the d = 3 regression (INFO); C-TARGETS (F1: the set T2 at lambda = 1 and 1.25 on every piece, naive; certified inputs enter
  with their certified values instead of their targets, SPEC sect. 4); certified minus float U on every piece (F2, INFO); the v1_2
  targets and the single-input headrooms (INFO); KR2, KR3 (the record's QUAD_TW_PART <= 3.9e-4), KR4 (S4-U against T2's +7.8e-4),
  KR5a (joint part), KR-J.
Cost [E]: sweep 70-150 s (1808 piece evaluations in mp.iv, C-MV doubling each), LIM 400; scan 40-100 s (C-TARGETS: 3616 naive piece
  evaluations), LIM 250. One core each, AS 8 GiB, run one after the other in the foreground. The script writes only
  pk07/out/out_<this file's name>_<item>[_TAG].out (a few kB) and, since v2_2, after a complete sweep the export
  pk07/out/export_<this file's name>_sweep[_TAG].kv (about 0.3 MB), both as new files.
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, time, math, hashlib, signal, traceback, json, re, types, inspect
from fractions import Fraction

LABEL = os.path.basename(__file__)[:-3] if os.path.basename(__file__).endswith('.py') else ''   # N-b (d = 3): label and OUT_PATH
if not re.fullmatch(r'[A-Za-z0-9_]{1,40}', LABEL):
    print('bad file name %r for the label' % os.path.basename(__file__))
    sys.exit(2)
if len(sys.argv) < 3 or sys.argv[1] not in ('sweep', 'scan'):
    print('usage: %s.py sweep|scan LIM [TAG]   (LIM = RLIMIT_CPU soft limit in s, hard LIM + 5)' % LABEL)
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
TAG = sys.argv[3] if len(sys.argv) > 3 else ''
if not (5 <= LIM <= 550) or not (TAG == '' or (TAG.isalnum() and len(TAG) <= 8)):
    print('bad LIM %r (need 5 <= LIM <= 550) or bad TAG %r' % (sys.argv[2], TAG))
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))
STAGE = ['start']

CODEDIR = '/mnt/g2/release/root/code'
SCR = CODEDIR + '/pk10/scripts'
SC = CODEDIR + '/pk10/scratch'
OWN = CODEDIR + '/pk07'
OUTD = OWN + '/out'
OUT_PATH = os.path.join(OUTD, 'out_%s_%s%s.out' % (LABEL, MODE, ('_' + TAG) if TAG else ''))   # N-b (d = 3): from the file's name
if not (os.path.isdir(OUTD) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUTD)
        and os.path.realpath(OUTD).startswith(os.path.realpath(OWN) + os.sep)):
    print('output directory check failed for %s' % OUT_PATH)
    sys.exit(2)
FH = open(OUT_PATH, 'x')


def cpu():
    return time.process_time()


def out(line):
    FH.write(line + '\n')
    FH.flush()


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)

FILES = {
    'pk10/scripts/m2_unif3.py': '8a693b9b', 'pk10/scripts/endpairs4.py': '0760d96e', 'pk10/scripts/vacmod2.py': '533546b1',
    'pk10/scripts/assemble_binding_unif4.py': '8e346bb0',
    'pk10/scratch/m2_N4_J170.json.b': '7c0d4316', 'pk10/scratch/m2_N3_J170.json.b': '55da99fd',
    'pk10/scratch/b5_N4_J170.json': 'f19d1e08', 'pk10/scratch/b5_N3_J170.json': '567f5543',
    'pk10/scratch/clT_N4_J170.json': 'cfd2ab7c', 'pk10/scratch/clT_N3_J170.json': '7d62c303',
    'pk10/scratch/binding4_N4_J170.json': '46a47036', 'pk10/scratch/binding4_N3_J170.json': 'f5e90b08',
    'pk10/scratch/endw_N4_J170.json': 'e8b1fe30', 'pk10/scratch/endw_N3_J170.json': '0db59cc3',
    'pk10/scratch/vacres_K3_N4.json': '516b2501', 'pk10/scratch/vacres_K3_N3.json': 'ebcbd08c',
    'pk10/scratch/m2_unif3_N4.txt': '91f6f1a4', 'pk10/scratch/m2_unif3_N3.txt': '643b702d',
    'pk10/scratch/endpairs4_N4.txt': '6b2702ef', 'pk10/scratch/endpairs4_N3.txt': '540b079f',
    'pk10/scratch/assemble_unif4_N4.txt': 'c1a0fc55', 'pk10/scratch/assemble_unif4_N3.txt': '600ee8bf',
    'pk20/rv13/c5/rc_m2_sens_N4.txt': '63af92fe', 'pk20/rv13/c5/rc_m2_sens_N3.txt': '37cf94c7',
    'pk20/rv13/c6/rc_end_sens_N4.txt': '973a64ca', 'pk20/rv13/c6/rc_end_sens_N3.txt': '5ecf4865',
    'pk20/rv13/c6/rc_end_sens.py': '8b496a35', 'pk20/rv13/c5/rc_m2_sens.py': 'f894df02',
    'pk08/S4_U_CERTIFIED_v2.md': 'cd2b32d7', 'pk05/out/s4c_m2ba_n4.out': '553395a3', 'pk05/out/s4c_m2ba_n3.out': '32ade026',
    'pk07/s4u_kv_ref_v1.py': '5a786edb', 'pk11/out/out_kt_s67_cert_v1_1_scan_d3.out': 'd8a514be',
    'pk08/out/px08_m2bb4_n4_asm.out': 'a563d888', 'pk08/out/px08_m2bc3_n4_asm.out': 'f181a623',
    'pk08/out/px08_px03_v4_n4_asm.out': 'f55df592', 'pk08/out/px08_m2bb4_n3_asm.out': '29773c44',
    'pk08/out/px08_m2bc4_n3_asm.out': 'fc41f247', 'pk08/out/px08_px03_v4_n3_asm.out': 'b5c8bb3f',
    'pk08/S4_TRB_CERTIFIED_v1.md': '2c17c287', 'pk08/out/px08_trbcert_v1_1_n4_asm.out': '9d3e8f62',
    'pk08/out/px08_trbcert_v1_1_n3_asm.out': 'ff2d93d0', 'pk07/kt_s67_export_reader_v1.py': 'c697418b',
}
# F2, S3: the S4-U record, its C-FMT reference parser and the C-SRC outputs, by full sha256
S4U = dict(path='pk08/S4_U_CERTIFIED_v2.md', sha256='cd2b32d72a49b37feece322e2018c071281c8e93ae9feb6b6349abe24e8a6aa4',
           producer='pk08', fmt='S4U_KV_v1', record='S4_U_CERTIFIED_v2')
S4U_REF = ('pk07/s4u_kv_ref_v1.py', '5a786edb1eb62608ecf7440b70124044d6207d87523b9c957394666ab4448c98')
S4U_SRC = {4: ('pk05/out/s4c_m2ba_n4.out', '553395a32dcfbf62777db22dca6a9e18aaad6d56ab343077c674f98972d8c735'),
           3: ('pk05/out/s4c_m2ba_n3.out', '32ade026f587cf3fc69fff607856eb9887013d741733e318102cb3c73dc5321f')}
# D-1: the asm outputs whose READING lines give the remainder pieces R_CERT sums (the record's N*_PREF2_RE_OUTPUT, N*_PREF2_RHO4_OUTPUT
# and N*_M3_OUTPUT tokens)
S4U_ASM = {(4, 'PREF2_RE'): ('pk08/out/px08_m2bb4_n4_asm.out', 'a563d888dd062b93d7c284c720513687fb619c10d554caa297405881b6c2094b'),
           (4, 'PREF2_RHO4'): ('pk08/out/px08_m2bc3_n4_asm.out', 'f181a623b671c06515207e0e20126e71f13b5d23cb8e7014f34d85375dc78c1d'),
           (4, 'M3_SUM'): ('pk08/out/px08_px03_v4_n4_asm.out', 'f55df5922eb0a026b2d814f2a7c665d7e1ff416a8a6a52aabbd8a90d3bcbd4df'),
           (3, 'PREF2_RE'): ('pk08/out/px08_m2bb4_n3_asm.out', '29773c441cbcb7e72818e4a8379410283a21e8702ca0688ed5277e5c69f1319c'),
           (3, 'PREF2_RHO4'): ('pk08/out/px08_m2bc4_n3_asm.out', 'fc41f24724922f2f7fd3b8d385936254c7550ff01b40408c41e4009c51e00053'),
           (3, 'M3_SUM'): ('pk08/out/px08_px03_v4_n3_asm.out', 'b5c8bb3f56a63b6b1146ec5576ddf16ea5778a8be6bd8e25924c2352de617965')}
# v2_1: the S4-TRB record and the asm outputs whose READING lines it copies, by full sha256
S4T = dict(path='pk08/S4_TRB_CERTIFIED_v1.md', sha256='2c17c287c0affbfe0e0fcbd8097edff2258ea1109d91381d6206a11d4efdd694',
           producer='pk08', fmt='S4U_KV_v1', record='S4_TRB_CERTIFIED_v1')
S4T_ASM = {4: ('pk08/out/px08_trbcert_v1_1_n4_asm.out', '9d3e8f622c6bf01ec26c75dfc414be730dbbfb87761af78b40cca2e75f2db9a2'),
           3: ('pk08/out/px08_trbcert_v1_1_n3_asm.out', 'ff2d93d01bdf2303e51d8d6f0499fd359a872db6f13132fc7d9f95c28aac08fe')}
D3_REF = 'pk11/out/out_kt_s67_cert_v1_1_scan_d3.out'     # D1: NOTE1_d3's recorded scan (v1_2 under TAG d3)
# v2_2 (3): the producer's reader of the per-piece export the sweep writes for S8, by full sha256
EXPORT_READER = ('pk07/kt_s67_export_reader_v1.py', 'c697418bc62f30523f91a2d3e5c15373aaa23f066d4e38f9f78e605d180f9cde')
EXPORT_FIELDS = ('jlo jhi c5_lo vSv_p_lo vSv_m_hi rp_lo rho_hi rho1_hi vp2_lo vp2_hi vm2_hi Bp_hi Bm_hi cx_lo r2_hi ro_hi Rw_hi c_lo '
                 'c_hi')                                     # pk11's list for S8 (its 15 numbers, then c_lo c_hi), after jlo jhi
EXPORT_PAIR_FIELDS = 'kind d m_checked k_mode holds'
EXPORT_ROWS = {4: [], 3: []}
BLOCKS = {
    'm2u3': ('pk10/scripts/m2_unif3.py', 31, 130, 'e5ccf3b4d3504b7d2f599d465d6acbffe9e9f3aa381bb2df6dd3a33e3140a63e'),
    'ep4': ('pk10/scripts/endpairs4.py', 31, 246, 'a95912cd172920204ea40b1cb8ea24f231144a55a1b25b4df4b0a5a4dc1c070d'),
    'ab4a': ('pk10/scripts/assemble_binding_unif4.py', 19, 35, '7edaaa88c230f1bc45570eb71370fe5cc22296fa3c12c91b1985016392a6bf85'),
    'ab4b': ('pk10/scripts/assemble_binding_unif4.py', 38, 78, 'af85ba2d045cce877397cda419cdeca8a6b1c18b25802e62a4ba153c7a2cb951'),
}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return sha_bytes(fh.read())
    except OSError:
        return 'MISSING'


def env_probe():
    """M-e: round-to-nearest, no flush-to-zero, no denormals-are-zero (operands built at runtime)."""
    e = math.ldexp(3, -54)
    ok = (1.0 + e == 1.0 + math.ldexp(1, -52)) and (-1.0 - e == -(1.0 + math.ldexp(1, -52)))
    ok = ok and math.ldexp(1, -1074) > 0 and math.ldexp(1, -1022) / 2 != 0
    return ok


out('%s sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d) TAG=%r' % (LABEL, sha_file(os.path.abspath(__file__)), MODE, LIM,
                                                                           LIM, LIM + 5, TAG))          # N-b (d = 3): LABEL
_bad = [n for n in sorted(FILES) if sha_file(os.path.join(CODEDIR, n))[:8] != FILES[n]]
out('C-HASH %s (%d files)%s' % ('PASS' if not _bad else 'FAIL', len(FILES), (': ' + ', '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
SRC = {}
_badb = []
for _k, (_p, _lo, _hi, _sha) in BLOCKS.items():
    with open(os.path.join(CODEDIR, _p)) as _fh:
        _lines = _fh.read().split('\n')
    SRC[_k] = '\n'.join(_lines[_lo - 1:_hi]) + '\n'
    if sha_bytes(SRC[_k].encode()) != _sha:
        _badb.append(_k)
out('C-BLOCK %s (author slices by sha256)%s' % ('PASS' if not _badb else 'FAIL', (': ' + ', '.join(_badb)) if _badb else ''))
if _badb:
    out('VERDICT INVALID (C-BLOCK)')
    sys.exit(2)

import numpy as np
import scipy.linalg as sla
import mpmath as mp
from scipy.special import erfc
iv = mp.iv
iv.dps = 25
IVT = type(iv.mpf(1))
_env0 = env_probe()
out('C-ENV start: %s (numpy %s, mpmath %s, python %s)' % ('PASS' if _env0 else 'FAIL', np.__version__, mp.__version__, sys.version.split()[0]))
if not _env0:
    out('VERDICT INVALID (C-ENV)')
    sys.exit(2)

# ------------------------------------------------------------------ inputs (FLOAT providers; tags)
# PARAMS: the FLOAT inputs of M2 (vac, wt, dl) and the J >= 170 Cov_1, which the verdicts still use until their providers exist (S3);
# trt2, S4's FLOAT U, and TRB, S4's FLOAT TRB, serve since v2 and v2_1 only path A's reproductions (float_s4) and the KR4 comparisons:
# the verdicts take U from provide_s4u (F2) and TRB from provide_s4trb (v2_1).
PARAMS = {
    4: dict(TRB='1.312607', vac=(2.6744e-06, 1.6450e-04, 4.2950e-06, 7.4706e-06, 3.837e-10, 1.1950e-06, 7.250e-11, 1.8816e-05, 0.999993,
                                 1.332042, 0.360),
            wt=(3.4712e-06, 5.287e-05, 7.487e-06, 170.0), dl=(2.4733e-06, 5.027e-05, 6.219e-06, 170.0),
            trt2=(1.0302393041, 0.846041, 0.639530, 0.498940, 6.509e-4), cov1=1.1765e-4),
    3: dict(TRB='0.942262', vac=(1.1426e-06, 5.2050e-05, 1.9050e-06, 2.5677e-06, 1.361e-10, 6.2950e-07, 5.250e-17, 1.4354e-05, 0.999998,
                                 1.331271, 0.360),
            wt=(1.2665e-06, 1.631e-05, 3.322e-06, 170.0), dl=(9.8425e-07, 1.515e-05, 2.752e-06, 170.0),
            trt2=(1.0302393041, 0.742488, 0.53795, 0.43804, 1.592e-4), cov1=2.2043e-4),
}
TAGS = {'M3 entries': 'FLOAT (pk10/scratch J = 170 JSONs)', 'M2 vacuum': 'FLOAT (vacscale parameters, rc_end_sens d3e142f3)',
        'S4 U': 'FLOAT (trace polynomial and rem(170))', 'S4 TRB': 'FLOAT (twrig4 at J = 170)'}
# F1: the pins of the inputs that have a provider. A tag reads certified only as 'CERTIFIED <producer> <sha8>' with these (tag_certified),
# and only the provider sets it (provide_s4u, provide_s4trb). M3 and M2 have no provider in v2_1, so no pin: their tags cannot read
# certified. D-3 (v2_1): S4-TRB's provider has C-HASH and C-FMT against the same S4U_KV_v1 reference parser, and C-SRC.
TAG_PINS = {'S4 U': (S4U['producer'], S4U['sha256'][:8]), 'S4 TRB': (S4T['producer'], S4T['sha256'][:8])}
CXI = 0.6594
VQ = [0.66767, 0.56373]
KAPPA = 0.41729
DS = list(range(0, 9)) + [10, 12, 15, 20]
MMAX, KMAX = 3000, 60
CLAIM = {4: (('flip', 3), ('same', 1)), 3: (('flip', 3), ('same', 1))}
FLIP170_CLAIM = {4: (('flip', 4), ('same', 1)), 3: (('flip', 3), ('same', 1))}   # D1: the own claim at J = 170, for C-FLIP170 only
TOL_B = 1e-10
MCAP = 2048.0


def jl(name):
    with open(os.path.join(SC, name)) as fh:
        return json.load(fh)


def load(N, S4, ST):
    """this N's inputs; U5 is the S4-U provider's U tuple (F2), quad and umf the record's N*_QUAD_TW_PART and N*_U_MINUS_FLOAT; TRBv
    is the S4-TRB provider's N*_TRB as an exact-decimal enclosure and trb its string (v2_1); r_iv is r_main by the matrix-tree theorem
    in mp.iv (v2_2 (1))."""
    return dict(N=N, M2=jl('m2_N%d_J170.json.b' % N), B5=jl('b5_N%d_J170.json' % N), CT=jl('clT_N%d_J170.json' % N),
                B4=jl('binding4_N%d_J170.json' % N), EW=jl('endw_N%d_J170.json' % N), mser=jl('vacres_K3_N%d.json' % N), P=PARAMS[N],
                U5=S4['U5'][N], quad=S4['quad'][N], umf=S4['umf'][N], TRBv=ST['TRBv'][N], trb=ST['trb'][N], r_iv=r_main_iv(N))


def float_s4(inp):
    """the same inputs with S4's FLOAT U (PARAMS trt2: lead, c1, c2, c3, rem(170)) and FLOAT TRB (PARAMS TRB), path A's: for the
    reproductions of the author's lines and of the distances (C-REPRO, C-REPRO300, C-FLIP170) and for the KR4 comparison (F2;
    v2_1 adds TRB, which was float_u's U only in v2)."""
    return dict(inp, U5=inp['P']['trt2'], TRBv=inp['P']['TRB'])


def path_a(inp, which):
    """the author's slices in a fresh namespace with this N's inputs ('m2u3', 'ep4', or 'ab4' = l.19-35 then l.38-78)."""
    P = inp['P']
    ns = dict(math=math, json=json, np=np, sla=sla, mp=mp, iv=iv, erfc=erfc, sys=types.SimpleNamespace(argv=[]), NN=inp['N'], J1=170.0,
              kbar=inp['M2']['kbar'], mser=inp['mser'], M2=inp['M2'], B5=inp['B5'], CT=inp['CT'], B4=inp['B4'], EW=inp['EW'],
              TRB=mp.mpf(P['TRB']), cxi=CXI, COV1=P['cov1'], RATIO=1.01)
    for k, v in zip(('nP', 'D5', 'R0', 'tX', 'tB', 'ann', 'far', 'gB', 'z2', 'Rtr', 'ae'), P['vac']):
        ns[k] = v
    for k, v in zip(('nPwM', 'D5w', 'R0w', 'J0w'), P['wt']):
        ns[k] = v
    for k, v in zip(('nPdM', 'D5d', 'R0d', 'J0d'), P['dl']):
        ns[k] = v
    for k, v in zip(('lead', 'c1', 'c2', 'c3', 'remT'), P['trt2']):
        ns[k] = v
    if which == 'ab4':
        ns['cxi'] = mp.mpf(repr(CXI))
        exec(compile(SRC['ab4a'], BLOCKS['ab4a'][0] + ':19-35', 'exec'), ns)
        exec(compile(SRC['ab4b'], BLOCKS['ab4b'][0] + ':38-78', 'exec'), ns)
    else:
        exec(compile(SRC[which], BLOCKS[which][0], 'exec'), ns)
    return ns


# ------------------------------------------------------------------ interval helpers and forward-mode differentiation
def pt(x):
    """a point interval (exact for floats, ints, strings rounded outward)."""
    return x if isinstance(x, IVT) else iv.mpf(x)


def ivlo(x):
    return pt(x).a


def ivhi(x):
    return pt(x).b


def isect(x, y):
    a = x.a if (x.a > y.a) is True else y.a
    b = x.b if (x.b < y.b) is True else y.b
    if (a > b) is True:
        raise AssertionError('empty intersection of two enclosures')
    return iv.mpf([a, b])


def finite(x, what):
    """M-d: an enclosure must have finite ends."""
    s = str(x)
    if 'inf' in s or 'nan' in s:
        raise ArithmeticError('non-finite %s: %s' % (what, s))
    return x


def pmax(xs):
    """the largest of point intervals, by exact comparison."""
    best = xs[0]
    for x in xs[1:]:
        if (x > best) is True:
            best = x
    return best


def pmin(xs):
    """the smallest of point intervals, by exact comparison (ties keep the first, which is equal)."""
    best = xs[0]
    for x in xs[1:]:
        if (x < best) is True:
            best = x
    return best


def contains(outer, inner):
    return (inner.a >= outer.a) is True and (inner.b <= outer.b) is True


class D:
    """value and t-derivative, both mp.iv intervals."""
    __slots__ = ('v', 'd')

    def __init__(self, v, d=0):
        self.v = pt(v)
        self.d = pt(d)

    def __add__(s, o):
        o = lift(o)
        return D(s.v + o.v, s.d + o.d)

    __radd__ = __add__

    def __sub__(s, o):
        o = lift(o)
        return D(s.v - o.v, s.d - o.d)

    def __rsub__(s, o):
        return lift(o) - s

    def __mul__(s, o):
        o = lift(o)
        return D(s.v * o.v, s.d * o.v + s.v * o.d)

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = lift(o)
        q = s.v / o.v
        return D(q, (s.d - q * o.d) / o.v)

    def __rtruediv__(s, o):
        return lift(o) / s

    def __neg__(s):
        return D(-s.v, -s.d)

    def __pow__(s, k):
        assert isinstance(k, int) and k >= 1
        r = s
        for _ in range(k - 1):
            r = r * s
        return r


def lift(x):
    return x if isinstance(x, D) else D(x, 0)


def dsum(xs):
    """a sum with no interval start value: mp.iv raises (it does not return NotImplemented) when a dual number is its right operand."""
    r = None
    for x in xs:
        if r is None:
            r = x
        elif isinstance(x, D) and not isinstance(r, D):
            r = x + r
        else:
            r = r + x
    return pt(0) if r is None else r


def nn(x, what):
    """[0, x.b] for a quantity that is >= 0 by construction (the author's max(., 0) keeps only the upper end); an enclosure entirely
    below 0 is an input inconsistency and stops the evaluation (M-d)."""
    if (x.b < 0) is True:
        raise ArithmeticError('the enclosure of the nonnegative %s lies below 0' % what)
    return iv.mpf([0, x.b])


def sqrt_any(x):
    if isinstance(x, D):
        r = iv.sqrt(x.v)
        return D(r, x.d / (2 * r))
    return iv.sqrt(pt(x))


def chol(G, m):
    L = [[pt(0)] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1):
            s = G[i][j] - dsum((L[i][k] * L[j][k] for k in range(j)))
            L[i][j] = sqrt_any(s) if i == j else s / L[j][j]
    return L


def lsolve(L, b, m):
    w = [pt(0)] * m
    for i in range(m):
        w[i] = (b[i] - dsum((L[i][k] * w[k] for k in range(i)))) / L[i][i]
    return w


def congruent(L, A, m):
    Y = [[pt(0)] * m for _ in range(m)]
    for j in range(m):
        for i in range(m):
            Y[i][j] = (A[i][j] - dsum((L[i][k] * Y[k][j] for k in range(i)))) / L[i][i]
    Ap = [[pt(0)] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            Ap[i][j] = (Y[i][j] - dsum((L[j][k] * Ap[i][k] for k in range(j)))) / L[j][j]
    return Ap


# ------------------------------------------------------------------ pieces
def pieces():
    out_ = []
    J = 300.0
    while J < 1e6:
        Jn = J * (1.0025 if J < 400.0 else 1.01)
        out_.append((J, Jn))
        J = Jn
    out_.append((J, None))
    return out_


def t_interval(Jlo, Jhi):
    """outward: [(1/J_hi).a, (1/J_lo).b], or [0, (1/J_lo).b] for the last piece."""
    hi_ = (pt(1) / pt(Jlo)).b
    lo_ = pt(0) if Jhi is None else (pt(1) / pt(Jhi)).a
    return iv.mpf([lo_, hi_])


# ------------------------------------------------------------------ entries as naive intervals, point values or dual numbers
class Ctx:
    """one N and one piece: entry and polynomial evaluation in the kinds 'naive' (over tI, with bars), 'point' (at t_m, with bars) and
    'dual' (value c(tI) + B, derivative c'(tI)); 'cnaive', 'central' and 'cdual' are the same without bars; 'offset' is a point input
    c(t_m) + delta at a corner of the bar box (C-MV-B). sc holds the scan hooks and the plants."""

    def __init__(self, inp, Jlo, Jhi, sc):
        self.inp, self.Jlo, self.Jhi, self.sc = inp, Jlo, Jhi, sc
        self.tI = t_interval(Jlo, Jhi)
        self.tm = self.tI.mid                                   # the rounded midpoint, inside tI; h covers its distance to both ends
        self.h = iv.mpf([0, pmax([pt((self.tm - self.tI.a).b), pt((self.tI.b - self.tm).b)])])
        self.tc = 1.0 / Jlo
        self.cache = {}

    def tvar(self, kind):
        """t for the kind: the point t_m, or the piece tI (PLANT-RIGHTEND: its right end in J, t = t_lo, for the naive kind)."""
        if kind in ('point', 'central', 'offset'):
            return self.tm
        if kind in ('naive', 'cnaive') and self.sc.get('right_end'):
            return iv.mpf([self.tI.a, self.tI.a])
        return self.tI

    def bar(self, src, name, d):
        """the bar's upper end: the stored components summed outward, times the scan hooks (all 1 outside the scans)."""
        sc = self.sc
        m = sc.get('bar_all', 1.0)
        if (src == 'B5' and name.startswith('g,')) or src == 'CT':
            m *= sc.get('bar_ritz', 1.0)
        if src == 'B5' and name.startswith('A,'):
            m *= sc.get('bar_amp', 1.0)
        if src in ('M2', 'B5', 'B4') and name in ('I3p', 'Ip3', 'Nw', 'Ndel', 'I_N'):
            m *= sc.get('bar_' + name, 1.0)
        if src == 'EW':
            m *= sc.get('bar_endw', 1.0)
        e = pt(d['err']) if 'err' in d else sum((pt(v) for v in d['B'].values()), pt(0))
        return (e * m).b

    def cmul(self, src, name):
        sc = self.sc
        if src == 'M2' and name == 'I3p':
            return 1.0 - sc.get('I3p_c', 0.0)
        if src == 'M2' and name == 'Ip3':
            return 1.0 + sc.get('Ip3_c', 0.0)
        if src == 'M2' and name == 'Nw':
            return 1.0 - sc.get('Nw_c', 0.0)
        return 1.0

    def entry(self, src, name, kind='naive'):
        key = (src, name, kind)
        if key in self.cache:
            return self.cache[key]
        d = self.inp['B4'][name] if src == 'B4' else self.inp[src]['items'][name]
        c = pt(self.cmul(src, name))
        ak = [pt(a) * c for a in d['ak']]
        e = self.bar(src, name, d)
        if kind == 'offset':                       # C-MV-B: a corner of the bar box, sc['offsets'][(src, name)] in {-1, 0, 1} times the bar
            B = e * self.sc.get('offsets', {}).get((src, name), 0)
        else:
            B = iv.mpf([-e, e]) if kind in ('naive', 'point', 'dual') else pt(0)
        t = self.tvar(kind)
        val = sum((ak[k] * t ** k for k in range(len(ak))), pt(0)) + B
        if kind in ('dual', 'cdual'):
            der = sum((k * ak[k] * self.tI ** (k - 1) for k in range(1, len(ak))), pt(0))
            r = D(val, der)
        else:
            r = val
        self.cache[key] = r
        return r

    def poly(self, coeffs, kind='naive'):
        """sum c_k t^k for t-polynomials such as m-hat and U's polynomial part."""
        cs = [pt(c) for c in coeffs]
        t = self.tvar(kind)
        val = sum((cs[k] * t ** k for k in range(len(cs))), pt(0))
        if kind in ('dual', 'cdual'):
            return D(val, sum((k * cs[k] * self.tI ** (k - 1) for k in range(1, len(cs))), pt(0)))
        return val

    def mhat(self, kind='naive'):
        ms = self.inp['mser']
        return self.poly([1.0, ms['m1'], ms['m2'], ms['m3']], kind)

    def U(self, kind='naive'):
        """F2: U(t) = lead (1 + c1 t + c2 t^2 + c3 t^3) + rem from the tuple inp['U5']: the S4-U provider's (LEAD_HI, C1_HI, C2_HI, C3_HI,
        R_CERT), or path A's FLOAT tuple under float_s4. The dual kind's derivative is lead (c1 + 2 c2 t + 3 c3 t^2); rem is a constant
        with zero derivative (port condition (ii)); point and dual kinds use the same polynomial (condition (iii)). The record's
        CLAIM_F2 holds for t in (0, 1/300]; the last piece [0, (1/J_lo).b] meets t = 0 only as the closure of that range, where the
        bound is its limit LEAD_HI + R_CERT (the record's U_T_RULE_AT_0)."""
        lead, c1, c2, c3, remT = self.inp['U5']
        ld = pt(lead)
        pu = self.poly([ld, ld * pt(c1), ld * pt(c2), ld * pt(c3)], kind)
        rest = pt(remT) * self.sc.get('remT', 1.0) + self.sc.get('U_add', 0.0)
        return pu + rest

    def TRB(self):
        """v2_1: inp['TRBv'], the S4-TRB provider's N*_TRB as an exact-decimal enclosure (one constant per N for every J >= 300, the
        record's CONSTANT_PER_N), or path A's FLOAT decimal under float_s4, enclosed outward; only its upper end enters beta."""
        return pt(self.inp['TRBv']) * self.sc.get('TRB', 1.0)


def chi3(s, N):
    return math.exp(-s / 2) if N == 3 else erfc(math.sqrt(s / 2)) + math.sqrt(2 * s / math.pi) * math.exp(-s / 2)


def vac_float(inp, J, sc):
    """the M2 FLOAT vacuum terms at the piece's left end (the author's vac(J) with hooks); returned as point intervals."""
    N = inp['N']
    nP, D5, R0, tX, tB, ann, far, gB, z2, Rtr, ae = inp['P']['vac']
    k = sc.get('vac_all', 1.0)
    nP, D5, R0, tX, tB, ann, far, gB = (x * k for x in (nP, D5, R0, tX, tB, ann, far, gB))
    D5 *= sc.get('D5', 1.0)
    gB *= sc.get('gB', 1.0)
    s_ = 150.0 / J
    dec = math.exp(-0.3 * ae * (J - 150) / 2)
    tBJ = tB * max(math.sqrt(chi3(J * KAPPA / v, N) / chi3(150 * KAPPA / v, N)) for v in VQ)
    tails = (tX + ann) * dec + tBJ
    near = nP * s_ ** 2 + (D5 + R0) * s_ ** 5 + tails
    fJ = far * (J / 150.0) ** 2 * math.exp(-0.5 * 0.3025 * (J - 150))
    g = gB * (J / 150.0) * math.exp(-0.95 * (1 - math.cos(math.radians(40))) * (J - 150) / 2)
    eps = (math.sqrt(near ** 2 + fJ) + g) / math.sqrt(z2)
    s = eps / (2 - Rtr - eps)

    def wres(cw, Wg):
        return (math.sqrt((cw * J * near) ** 2 + (Wg * J) ** 2 * fJ) + Wg * J * g) / math.sqrt(z2)

    def ew(nPM, D5x, R0x, J0, cw, Wg):
        sw = J0 / J
        nw = nPM * sw ** 2 + (D5x + R0x) * sw ** 5 + cw * J * tails
        return (math.sqrt(nw ** 2 + (Wg * J) ** 2 * fJ) + Wg * J * g) / math.sqrt(z2)
    kw = sc.get('eps_w', 1.0)
    return dict(eps_r=pt(eps), s=pt(s), eps_a=pt(wres(CXI, 2.0) * sc.get('eps_a', 1.0)), eps_ds5=pt(wres(CXI / 2, 1.0) * sc.get('eps_ds5', 1.0)),
                eps_w=pt(ew(*inp['P']['wt'], CXI, 2.0) * kw), eps_d=pt(ew(*inp['P']['dl'], CXI / 2, 1.0) * kw), tag=TAGS['M2 vacuum'])


# ------------------------------------------------------------------ the Ritz blocks and the U-sensitive differences
def ritz_basis(cx):
    """the float eigh preconditioners at t_c (exact matrices afterwards)."""
    Ub = {}
    for idx, nm in (([0, 1, 3], 'even'), ([2], 'odd')):
        kg = lambda a, b: 'g,%d,%d' % (min(a, b), max(a, b))
        kt = lambda a, b: 'T,%d,%d' % (min(a, b), max(a, b))
        cen = lambda d: sum(a * cx.tc ** k for k, a in enumerate(d['ak']))
        Gc = np.array([[cen(cx.inp['B5']['items'][kg(a, b)]) for b in idx] for a in idx])
        Tc = np.array([[cen(cx.inp['CT']['items'][kt(a, b)]) for b in idx] for a in idx])
        nu, Uv = sla.eigh(Tc, Gc)
        Ub[nm] = (idx, [[pt(float(Uv[i, j])) for j in range(len(idx))] for i in range(len(idx))])
    return Ub


def ritz_matrix(cx, Ub, nm, kind):
    """L^-1 (U^T T U) L^-T with L = chol(U^T G U), U the exact preconditioner; the congruence as U^T (X U), which gives the same
    enclosure as the termwise sum (each stored entry still enters each product once). Cached per piece and kind."""
    key = ('rm', nm, kind)
    if key in cx.cache:
        return cx.cache[key]
    idx, Ui = Ub[nm]
    m = len(idx)
    kg = lambda a, b: 'g,%d,%d' % (min(a, b), max(a, b))
    kt = lambda a, b: 'T,%d,%d' % (min(a, b), max(a, b))
    GI = [[cx.entry('B5', kg(idx[a], idx[b]), kind) for b in range(m)] for a in range(m)]
    TI = [[cx.entry('CT', kt(idx[a], idx[b]), kind) for b in range(m)] for a in range(m)]

    def cg(X):
        W = [[dsum((X[a][b] * Ui[b][j] for b in range(m))) for j in range(m)] for a in range(m)]
        return [[dsum((W[a][j] * Ui[a][i] for a in range(m))) for j in range(m)] for i in range(m)]
    Mm, Am = cg(GI), cg(TI)
    r = congruent(chol(Mm, m), Am, m)
    cx.cache[key] = r
    return r


def gersh_lo(Ap, i, m):
    """A'_ii - sum_{j != i} |A'_ij| as an interval (naive)."""
    r = sum((abs(Ap[i][j]) for j in range(m) if j != i), pt(0))
    return Ap[i][i] - r, r


def order_from_central(cx, Ub):
    """the fixed index choices (i0 top, ix second, iy lowest) from the central diagonal at t_m. Any fixed choice gives valid bounds for
    mu_0 and mu_x; iy's Gershgorin row is used only after C-ORDER (in quantities) shows its disc lowest on the whole piece and box."""
    if 'order' not in cx.cache:
        Ac = ritz_matrix(cx, Ub, 'even', 'central')
        cen = [float(Ac[i][i].mid) for i in range(3)]
        o = sorted(range(3), key=lambda i: cen[i])
        cx.cache['order'] = (o[2], o[1], o[0])
    return cx.cache['order']


def radius_const(cx, Ub):
    """N-d: the fixed row iy's Gershgorin radius as a constant on the piece, the naive upper end of sum_{j != iy} |A'_iy,j| over P x B.
    Shared by every kind of the piece (condition (iii)); sub-contexts of the same piece receive it."""
    if 'R_iy' not in cx.cache:
        iy = order_from_central(cx, Ub)[2]
        cx.cache['R_iy'] = pt(gersh_lo(ritz_matrix(cx, Ub, 'even', 'naive'), iy, 3)[1].b)
    return cx.cache['R_iy']


def udiffs(cx, Ub, kind):
    """the three U-sensitive differences as smooth functions (fixed index choices from the central diagonal), plus what the naive bound
    adds; kind 'naive'|'point'|'dual'|'central'|'cdual'."""
    Ae = ritz_matrix(cx, Ub, 'even', kind)
    Ao = ritz_matrix(cx, Ub, 'odd', kind)
    U = cx.U(kind)
    diag = [Ae[i][i] for i in range(3)]
    f_rho2 = U - dsum((x * x for x in diag))
    i0, ix, iy = order_from_central(cx, Ub)
    a_, c_, b_ = Ae[i0][i0], Ae[ix][ix], Ae[i0][ix]
    mux = (a_ + c_) / 2 - sqrt_any(((a_ - c_) / 2) ** 2 + b_ * b_)
    muz = Ao[0][0]
    f_L1s = U - Ae[i0][i0] ** 2 - (Ae[iy][iy] - radius_const(cx, Ub)) ** 2 - muz ** 2      # N-d: mu_y = A'_yy - R_y, R_y constant
    f_L2 = U - Ae[i0][i0] ** 2 - mux ** 2 - muz ** 2
    return dict(Ae=Ae, Ao=Ao, U=U, f_rho2=f_rho2, f_L1s=f_L1s, f_L2=f_L2, i0=i0, ix=ix, iy=iy, mux=mux, muz=muz)


def ud_kind(cx, Ub, kind):
    key = 'ud_' + kind
    if key not in cx.cache:
        cx.cache[key] = udiffs(cx, Ub, kind)
    return cx.cache[key]


def centered(cx, Ub, key, naive_val):
    """the upper end of a U-sensitive difference over the piece and box, as a point: the smaller of the naive bound's and of
    [F(t_m) + D(P)[-h, h]] (SPEC v1_2 sect. 2, N-e). Where F(t_m) or D(P) is not finite, or the evaluation meets a kink, the naive upper
    end is used and the fallback is counted (N-d)."""
    try:
        Fm = ud_kind(cx, Ub, 'point')[key]
        Dp = ud_kind(cx, Ub, 'dual')[key]
        cen = finite(Fm + finite(Dp.d, 'D(P) of ' + key) * cx.h * iv.mpf([-1, 1]), key)
    except (ArithmeticError, ValueError, ZeroDivisionError):
        cx.cache['fallbacks'] = cx.cache.get('fallbacks', 0) + 1
        return pt(naive_val.b), None
    return pmin([naive_val.b, cen.b]), cen


MV_KEYS = ('f_rho2', 'f_L1s', 'f_L2', 'S5 Dd')


def mv_values(cx, Ub, kind):
    """the four smooth functions of the centered forms (bar-free kinds 'central' and 'cdual'), with the piece's fixed index order."""
    r = dict(udiffs(cx, Ub, kind))
    r['S5 Dd'] = s5_parts(cx, dict(eps_ds5=pt(0)), kind)['Dd']
    return r


def mv_check(cx, Ub, zero_derivative=False):
    """C-MV: each bar-free f_c at 9 equispaced points of the piece lies in f_c(t_m) + D_c(P)[-h, h]; returns the keys that fail.
    zero_derivative is PLANT-MV (D_c replaced by 0)."""
    fm = mv_values(cx, Ub, 'central')
    dc = mv_values(cx, Ub, 'cdual')
    enc = {k: fm[k] + (pt(0) if zero_derivative else dc[k].d) * cx.h * iv.mpf([-1, 1]) for k in MV_KEYS}
    bad = set()
    for j in range(9):
        tj = cx.tI.a + (cx.tI.b - cx.tI.a) * j / 8
        sub = Ctx(cx.inp, cx.Jlo, cx.Jhi, cx.sc)
        sub.tm = iv.mpf([tj.a, tj.a])
        sub.cache['order'] = order_from_central(cx, Ub)
        sub.cache['R_iy'] = radius_const(cx, Ub)
        fj = mv_values(sub, Ub, 'central')
        bad.update(k for k in MV_KEYS if not contains(enc[k], fj[k]))
    return sorted(bad)


# ------------------------------------------------------------------ S6 and S7 quantities (rigorous intervals; naive form = P0 path B)
def quantities(cx, Ub, V, use_centered=True):
    inp, sc = cx.inp, cx.sc
    mh = cx.mhat()
    er = V['eps_r']
    s = V['s']
    if sc.get('drop_sp'):
        s = pt(0)
    c = iv.sqrt(1 - s * s)
    sp = s * iv.sqrt(2 / (1 + c))
    kbar = pt(inp['M2']['kbar'])
    g00 = cx.entry('M2', 'g00')
    gb00 = cx.entry('B5', 'g,0,0')
    alpha = cx.entry('B5', 'A,0') / (mh * gb00)
    Bu2 = (2 * cx.entry('B5', 'Ia') / mh - cx.entry('B5', 'Na')) / gb00 + iv.mpf([0, (V['eps_a'] ** 2).b])
    vtr = iv.sqrt(nn(Bu2 - alpha ** 2, 'Bu2 - alpha^2'))
    Dm = cx.TRB() - alpha
    beta = pt(((alpha + Dm) / 2 + iv.sqrt(((Dm - alpha) / 2) ** 2 + vtr ** 2)).b)
    kb = pt((kbar * (1 + er)).b)
    Bop = pmax([beta, kb])
    nv = udiffs(cx, Ub, 'naive')
    Ae, Ao = nv['Ae'], nv['Ao']
    s2end = (lambda x: x.b) if sc.get('s2_upper') else (lambda x: x.a)                  # PLANT-S2UP takes S2_even from the upper ends
    de = [pt(0) if (Ae[i][i].a < 0) is True else pt(s2end(Ae[i][i])) for i in range(3)]
    gl = [gersh_lo(Ae, i, 3)[0] for i in range(3)]
    mu0 = pmax(de)
    muy_n = pmin([pt(g.a) for g in gl])
    muy_n = pt(0) if (muy_n < 0) is True else muy_n
    muz = pt(0) if (Ao[0][0].a < 0) is True else pt(Ao[0][0].a)
    U = cx.U()
    rho2_n = U - sum((x * x for x in de), pt(0))
    L1s_n = U - mu0 ** 2 - muy_n ** 2 - muz ** 2
    rho2, L1arg = rho2_n, L1s_n
    order_ok = None
    if use_centered:
        rho2, _ = centered(cx, Ub, 'f_rho2', rho2_n)                     # Schur: valid whatever the signs
        i0, iy = nv['i0'], nv['iy']
        gy = gersh_lo(Ae, iy, 3)[0]
        # C-ORDER (F2, E4): row iy certified as the minimizing Gershgorin row (up(g_iy) < lo(g_j)), and A_00, mu_z and A_yy - R_y positive
        # on the whole piece and box, since the smooth L1 form squares them; otherwise L1 keeps its naive bound (the minimum over rows)
        order_ok = ((Ae[i0][i0].a > 0) is True and (Ao[0][0].a > 0) is True and ((Ae[iy][iy] - radius_const(cx, Ub)).a > 0) is True
                    and all((gersh_lo(Ae, j, 3)[0].a > gy.b) is True for j in range(3) if j != iy))
        if order_ok:
            L1arg, _ = centered(cx, Ub, 'f_L1s', L1s_n)
    L1o = iv.sqrt(nn(rho2, 'rho^2 lambda_0^2'))
    L1 = iv.sqrt(nn(L1arg, 'the L1 argument'))
    L1 = L1 if (L1.b >= L1o.b) is True else L1o
    L1 = pt(L1.b)
    L1o = pt(L1o.b)
    lam0 = pt((mh * (1 - er)).a) if sc.get('author_forms') else pt((mh * (1 - er / c)).a)   # RV13_1/C5/C6 n1 (N3)
    lam0 = pmax([mu0, lam0])
    rho1 = pt((L1 / lam0).b)
    rho = pt((L1o / lam0).b)
    HT = cx.entry('M2', 'I3p') / (g00 * mh)
    Nw = cx.entry('M2', 'Nw')
    ew = V['eps_w']
    Dn2 = (2 * cx.entry('M2', 'Ip3') / mh - Nw) / g00 + ew ** 2
    Dn = iv.sqrt(nn(Dn2, 'Dn^2'))
    uh = abs(cx.entry('M2', 'kn') - kbar * g00) / g00 + sp * iv.sqrt(Nw / g00)
    ua = abs(cx.entry('M2', 'A0w')) / (mh * g00) + sp * Dn
    NT2 = pt((HT - 2 * ew * (iv.sqrt(L1 * HT / mh) + (1 + er) * uh) - (1 + er) * ua ** 2).a)
    nt = pt(0) if (NT2 < 0) is True else NT2
    num = pt((iv.sqrt(nt) - s * iv.sqrt(L1 / mh.a) * Bop).a)
    num = pt(0) if (num < 0) is True else num
    Rp = pt((num ** 2 / ((1 + er) * (pt(Dn.b) + s * Bop) ** 2)).a)
    vSv_p = pt((num ** 2 / (1 + er) ** 3).a)
    vp = pt(((pt(Dn.b) + s * Bop) / (c * (1 - er))).b)
    Hd = pt((cx.entry('M2', 'I3m') / (g00 * mh)).b)
    rp_ = pt((L1o / mh.a).b)
    ed = V['eps_d']
    vSv_m = pt(((iv.sqrt(Hd + 2 * ed * iv.sqrt(rp_ * Hd) + rp_ * ed ** 2) + s * iv.sqrt(rp_) * beta / 2) ** 2
                / (c * c * (1 - er) ** 3)).b)
    odd2 = pt(((2 * cx.entry('B4', 'I_N') / mh - cx.entry('B5', 'Ndel')) / g00 + ed ** 2).b)
    vm = pt(((iv.sqrt(nn(odd2, '|v-|^2')) + s * beta / 2) / (c * (1 - er))).b)
    Ew = pt(((abs(cx.entry('M2', 'A0w')) / (mh * g00) + sp * (2 * Dn + Bop * sp)) / (1 - er)).b)
    t1 = pt(((kbar + Ew) * (1 + er)).b)
    nBp = pt(((beta if (beta.b >= t1.b) is True else t1) / (1 - er)).b)
    nBm = pt((beta / 2 / (1 - er)).b)
    q = (cx.entry('EW', 'I_mix') * iv.sqrt(inp['r_iv'] / (pt(g00.b) * pt(cx.entry('EW', 'I_free').b)))).a   # v2_2 (1): r_main in mp.iv
    Rw = pt(iv.sqrt(nn(1 / (pt(q) - sp) ** 2 - 1, 'R_w^2')).b)
    return dict(rho1=rho1, rho=rho, Rp=Rp, vSv_p=vSv_p, vp=vp, vSv_m=vSv_m, vm=vm, nBp=nBp, nBm=nBm, Rw=Rw, L1=L1, L1o=L1o, beta=beta,
                lam0=lam0, mu0=mu0, muz=muz, mh=mh, s=s, sp=sp, er=er, c=c, Bu2=Bu2, alpha=alpha, vtr=vtr, nv=nv, rho2=rho2,
                rho2_naive=rho2_n, L1arg=L1arg, L1_naive=L1s_n, U=U, order_ok=order_ok, uh=uh, Ew=Ew, t1=t1, kb=kb)   # v2_2 (2): C-KBAR INFO


def mode(cx, Ub, Q, V, use_centered=True):
    inp = cx.inp
    mh, s, sp, er, c = Q['mh'], Q['s'], Q['sp'], Q['er'], Q['c']
    idx = [0, 1, 3]
    Ge = [[cx.entry('B5', 'g,%d,%d' % (min(a, b), max(a, b))) for b in idx] for a in idx]
    Te = [[cx.entry('CT', 'T,%d,%d' % (min(a, b), max(a, b))) for b in idx] for a in idx]
    Aa = [cx.entry('B5', 'A,%d' % a) for a in idx]
    L = chol(Ge, 3)
    w = lsolve(L, Aa, 3)
    g00 = Ge[0][0]
    ax = abs(w[1] / (mh * iv.sqrt(g00)))
    Tm = congruent(L, Te, 3)
    qx = pt(Tm[1][1].a)
    nv = Q['nv']
    i0, ix = nv['i0'], nv['ix']
    Ae = nv['Ae']
    mux_n = pt(((Ae[i0][i0].a + Ae[ix][ix].a) / 2 - iv.sqrt(((pt(Ae[i0][i0].a) - Ae[ix][ix].a) / 2) ** 2 + pt(abs(Ae[i0][ix]).b) ** 2)).a)
    if (mux_n > 0) is not True:                                         # the L2 bound squares it
        raise ArithmeticError('the mu_x lower bound is not positive')
    mux = mux_n
    U = Q['U']
    L2arg_n = U - Q['mu0'] ** 2 - mux ** 2 - Q['muz'] ** 2
    L2arg = L2arg_n
    sq_arg = ((Ae[i0][i0] - Ae[ix][ix]) / 2) ** 2 + Ae[i0][ix] ** 2
    if (use_centered and (Ae[i0][i0].a > 0) is True and (Q['muz'] > 0) is True    # the smooth L2 form squares A_00 and mu_z too,
            and (sq_arg.a > 0) is True):                                          # and mu_x's square root must stay off its kink (N-d)
        L2arg, _ = centered(cx, Ub, 'f_L2', L2arg_n)
    L2 = pt(iv.sqrt(nn(L2arg, 'the L2 argument')).b)
    alpha_ = cx.entry('B5', 'A,0') / (mh * g00)
    Bu2 = (2 * cx.entry('B5', 'Ia') / mh - cx.entry('B5', 'Na')) / g00 + iv.mpf([0, (V['eps_a'] ** 2).b])
    vtr = iv.sqrt(nn(Bu2 - alpha_ ** 2, 'Bu2 - alpha^2'))
    Dm = cx.TRB() - alpha_
    beta = pt(((alpha_ + Dm) / 2 + iv.sqrt(((Dm - alpha_) / 2) ** 2 + vtr ** 2)).b)
    den3 = (1 - er) if cx.sc.get('author_forms') else (c - er)                                  # RV13_1 N3
    Dlt = pt((sp * (beta + alpha_ + 2 * iv.sqrt(Bu2) + beta * sp) / (1 - er) + vtr * er / den3).b)
    lam_ = Q['lam0']
    L1 = Q['rho1'] * lam_
    qxp = pt((qx - (1 + er) * mh.b * sp * sp).a)
    al2 = ((qxp - L2) / (L1 - L2)).a
    al2 = pt(0) if (pt(al2) < 0) is True else (pt(1) if (pt(al2) > 1) is True else pt(al2))
    axl = pt((pt(ax.a) - Dlt).a)
    cx_ = (iv.sqrt(al2) * axl - iv.sqrt(1 - al2) * iv.sqrt(nn(Q['vp'] ** 2 - axl ** 2, '|v+|^2 - a_x^2'))).a
    return dict(cx=pt(cx_), r2=pt((L2 / mux).b), ro=pt((Q['rho'] * lam_ / mux).b), al2=al2, L2=L2, mux=mux, qx=qx, ax=pt(ax.a), Dlt=Dlt,
                simple=(L2 < mux) is True, L2arg=L2arg, L2_naive=L2arg_n)


def pj(Q, d, m, kind, sc, C1):
    """Jensen inequality (endpairs4 passes_jensen) in intervals; True only if the lower end of the left side is > 0."""
    e = Q['Rw'] * sc.get('Rw', 1.0) * Q['rho1'] ** d
    r1, r = Q['rho1'], Q['rho']
    pX = iv.sqrt(Q['vp'] ** 2 + Q['vm'] ** 2)
    nBp, nBm = Q['nBp'] * sc.get('nB', 1.0), Q['nBm'] * sc.get('nB', 1.0)
    Dm1 = r1 ** (m + 1) * e * e
    if (Dm1 < 1) is not True:
        return False
    au = e * pX
    t2 = au * au * Dm1 / (1 - Dm1) + (2 * au * r1 ** m * e * (pX + nBp * e) + (r1 ** m * e * (pX + nBp * e)) ** 2) / (1 - Dm1)
    hm = lambda x: iv.sqrt(x) ** (m - 1) if m > 1 else pt(1)
    if kind == 'flip':
        Cm = C1 if m == 1 else Q['vSv_p'] * Q['Rp'] ** (m - 2) - Q['vSv_m'] * r ** (m - 2)
        ep = hm(r1) * nBp * e
        em = hm(r) * nBm * e
        err = hm(r1) * Q['vp'] * 2 * ep + ep * ep + hm(r) * Q['vm'] * 2 * em + em * em
        return ((Cm - err - t2) > 0) is True
    P = iv.sqrt(Q['vSv_p'] / r1) if m == 1 else iv.sqrt(Q['vSv_p'] * Q['Rp'] ** (m - 2))
    et = hm(r1) * nBp * e
    return (P >= et) is True and ((P * (P - 2 * et) - et * et - t2) > 0) is True


def pm(Q, Mq, d, k, kind, sc):
    """mode inequality M(k, e) of SPEC v1_1 sect. 1a in intervals."""
    e = Q['Rw'] * sc.get('Rw', 1.0) * Q['rho1'] ** d
    nBp, nBm = Q['nBp'] * sc.get('nB', 1.0), Q['nBm'] * sc.get('nB', 1.0)
    X = Mq['cx'] / sc.get('cx_div', 1.0) - nBp * e
    if (X > 0) is not True:
        return False
    pX = iv.sqrt(Q['vp'] ** 2 + Q['vm'] ** 2)
    r1 = Q['rho1']
    E = Mq['r2'] ** k * (Q['vp'] + nBp * e) ** 2
    O = Mq['ro'] ** k * ((Q['vm'] + nBm * e) ** 2 if kind == 'flip' else 2 * Q['vm'] * nBm * e + (nBm * e) ** 2)
    Dm1 = r1 ** (k + 2) * e * e
    if (Dm1 < 1) is not True:
        return False
    T = (r1 ** 2 * (e * pX) ** 2 * e * e + 2 * r1 * e * pX * e * (pX + nBp * e) + r1 ** (k + 2) * (e * (pX + nBp * e)) ** 2) / (1 - Dm1)
    return ((X * X - E - O - T) > 0) is True


def s7mono_hyp(Q, Mq, d, k0, sc):
    """the hypotheses of Lemma S7-mono (a) at the claimed d: r2, ro, rho1 < 1, X > 0, rho1^(k0+2) e^2 < 1."""
    e = Q['Rw'] * sc.get('Rw', 1.0) * Q['rho1'] ** d
    X = Mq['cx'] / sc.get('cx_div', 1.0) - Q['nBp'] * sc.get('nB', 1.0) * e
    return ((Mq['r2'] < 1) is True and (Mq['ro'] < 1) is True and (Q['rho1'] < 1) is True and (X > 0) is True
            and (Q['rho1'] ** (k0 + 2) * e * e < 1) is True)


def coverage(Q, Mq, sc, C1, pairs):
    res = {}
    for kd, d in pairs:
        m = 1
        while m <= MMAX and pj(Q, d, m, kd, sc, C1):
            m += 1
        k = 1
        while k <= KMAX and not pm(Q, Mq, d, k, kd, sc):
            k += 1
        res[(kd, d)] = (m - 1, k)
    return res


def coverage_claim(Q, Mq, sc, C1, pairs):
    """the same verdict as coverage() for the claimed pairs, with less work: k = the first mode success (Lemma S7-mono covers m >= k + 1),
    then Jensen only for m = 1..k. Returns (m checked, k); the claim holds iff m checked >= k (m checked stops at k)."""
    res = {}
    for kd, d in pairs:
        k = 1
        while k <= KMAX and not pm(Q, Mq, d, k, kd, sc):
            k += 1
        m = 1
        while k <= KMAX and m <= k and pj(Q, d, m, kd, sc, C1):
            m += 1
        res[(kd, d)] = (m - 1, k)
    return res


def claim_holds(cv, p):
    """Jensen for m = 1..k and the mode inequality at k <= KMAX (so Lemma S7-mono covers m >= k + 1)."""
    return cv[p][1] <= KMAX and cv[p][0] >= cv[p][1]


# ------------------------------------------------------------------ S5 (binding pair) with the centered even - odd
def s5_parts(cx, V, kind):
    mh = cx.mhat(kind)
    idx = [0, 1, 3]
    Ge = [[cx.entry('B5', 'g,%d,%d' % (min(a, b), max(a, b)), kind) for b in idx] for a in idx]
    Aa = [cx.entry('B5', 'A,%d' % a, kind) for a in idx]
    L = chol(Ge, 3)
    w = lsolve(L, Aa, 3)
    g00 = Ge[0][0]
    sg = sqrt_any(g00)
    ax = w[1] / (mh * sg)
    ay = w[2] / (mh * sg)
    even = ax * ax + ay * ay
    edl = V['eps_ds5'] if kind in ('naive', 'point', 'dual', 'offset', 'cnaive') else pt(0)
    odd = (2 * cx.entry('B4', 'I_N', kind) / mh - cx.entry('B5', 'Ndel', kind)) / g00 + edl * edl
    if cx.sc.get('odd_sign'):
        odd = -odd
    return dict(even=even, odd=odd, Dd=even - odd, g00=g00, mh=mh)


def s5_bound(cx, V, use_centered=True):
    nv = s5_parts(cx, V, 'naive')
    Dd = nv['Dd']
    if use_centered:
        try:
            Fm = s5_parts(cx, V, 'point')['Dd']
            Dp = s5_parts(cx, V, 'dual')['Dd']
            cen = finite(Fm + finite(Dp.d, 'D(P) of S5 even - odd') * cx.h * iv.mpf([-1, 1]), 'S5 even - odd')
        except (ArithmeticError, ValueError, ZeroDivisionError):           # a kink or a non-finite D(P): the naive enclosure (N-d)
            cx.cache['fallbacks'] = cx.cache.get('fallbacks', 0) + 1
            cen = None
        if cen is not None:
            Dd = isect(nv['Dd'], cen)                                        # both are true two-sided enclosures here
    mh, g00 = nv['mh'], nv['g00']
    er, s = V['eps_r'], V['s']
    c = iv.sqrt(1 - s * s)
    sp = s * iv.sqrt(2 / (1 + c))
    Bu2 = (2 * cx.entry('B5', 'Ia') / mh - cx.entry('B5', 'Na')) / g00 + iv.mpf([0, (V['eps_a'] ** 2).b])
    alpha = cx.entry('B5', 'A,0') / (mh * g00)
    vtr = iv.sqrt(nn(Bu2 - alpha ** 2, 'Bu2 - alpha^2'))
    Dm = cx.TRB() - alpha
    beta = pt(((alpha + Dm) / 2 + iv.sqrt(((Dm - alpha) / 2) ** 2 + vtr ** 2)).b)
    den3 = (1 - er) if cx.sc.get('author_forms') else (c - er)                                  # RV13_1 N3
    Dlt = sp * (beta + alpha + 2 * iv.sqrt(Bu2) + beta * sp) / (1 - er) + vtr * er / den3
    vacT = Dlt * (2 * vtr + Dlt)
    low = (Dd - vacT).a
    return dict(c5=pt(low), even=nv['even'], odd=nv['odd'], vacT=vacT, beta=beta, Dd=Dd, Dd_naive=nv['Dd'], Dlt=Dlt)   # Dlt: v2_2 export


# ------------------------------------------------------------------ one piece: S5, S6 and S7, and the verdicts of the scans
def piece_eval(inp, Jlo, Jhi, sc, use_centered=True, Ub=None, Jvac=None, order=None, C1=None, full=False, pairs=None):
    """S5, S6 and S7 on one piece. Ub, Jvac and order let C-PIECE reuse the parent piece's preconditioner, vacuum point and index order.
    C1 = None takes the piece's own c5 for S7's m = 1 Jensen test (ADD1 sect. 1); a number takes that constant (path A's Cov_1, for
    C-REPRO). full = True runs the full coverage search (Jensen to its first failure) instead of the claim check."""
    cx = Ctx(inp, Jlo, Jhi, sc)
    if order is not None:
        cx.cache['order'] = order
    V = vac_float(inp, Jlo if Jvac is None else Jvac, sc)
    S5 = s5_bound(cx, V, use_centered)
    Ub = ritz_basis(cx) if Ub is None else Ub
    Q = quantities(cx, Ub, V, use_centered)
    Mq = mode(cx, Ub, Q, V, use_centered)
    c1 = (S5['c5'] if C1 is None else pt(C1)) / sc.get('cov1_div', 1.0)
    prs = CLAIM[inp['N']] if pairs is None else pairs
    cv = (coverage if full else coverage_claim)(Q, Mq, sc, c1, prs)
    return dict(cx=cx, V=V, S5=S5, Ub=Ub, Q=Q, Mq=Mq, cv=cv)


def verdict_one(inp, Jlo, Jhi, sc, which, use_centered=False, claim=None):
    """S5: c5 > 0; S6: R+/rho > 1; S7: the claimed coverage (CLAIM, or the pairs in claim: D1's FLIP170_CLAIM, D2's flip d = 3 pair), with
    C_1 = the piece's c5 (path A's Cov_1 under the hook 'C1_const'). A numeric breakdown under a large hook counts as a failed verdict;
    programming errors and empty intersections are not caught."""
    try:
        cx = Ctx(inp, Jlo, Jhi, sc)
        V = vac_float(inp, Jlo, sc)
        if which == 'S5':
            return (s5_bound(cx, V, use_centered)['c5'] > 0) is True
        Ub = ritz_basis(cx)
        Q = quantities(cx, Ub, V, use_centered)
        if which == 'S6':
            return ((Q['Rp'] / Q['rho']).a > 1) is True
        Mq = mode(cx, Ub, Q, V, use_centered)
        c1 = pt(inp['P']['cov1']) if sc.get('C1_const') else s5_bound(cx, V, use_centered)['c5']
        prs = CLAIM[inp['N']] if claim is None else claim                  # D1, D2
        cv = coverage_claim(Q, Mq, sc, c1 / sc.get('cov1_div', 1.0), prs)
        return all(claim_holds(cv, p) for p in prs)
    except (ValueError, ZeroDivisionError, ArithmeticError):
        return False


def flip_search(fn, kind, cap):
    """smallest hook value at which fn is False: 'mul' (k >= 1), 'add' (delta >= 0), 'rel' (r in [0, 1)); None if never below cap; 0.0 if
    the baseline fails. Bisection to 0.4 per cent (INFO for the targets)."""
    if not fn(1.0 if kind == 'mul' else 0.0):
        return 0.0
    if kind == 'mul':
        lo, hi = 1.0, 2.0
        while fn(hi):
            lo, hi = hi, hi * 2
            if hi > cap:
                return None
        while hi / lo > 1.004:
            mid = math.sqrt(lo * hi)
            lo, hi = (mid, hi) if fn(mid) else (lo, mid)
        return hi
    if kind == 'add':
        lo, hi = 0.0, 1e-4
        while fn(hi):
            lo, hi = hi, hi * 2
            if hi > cap:
                return None
        while hi - lo > 0.004 * hi:
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if fn(mid) else (lo, mid)
        return hi
    lo, hi = 0.0, 0.01
    while fn(hi):
        lo, hi = hi, min(hi * 2, cap)
        if lo >= cap:
            return None
    while hi - lo > 2e-4:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if fn(mid) else (lo, mid)
    return hi


def fmt_f(v):
    return 'never (cap)' if v is None else ('baseline fails' if v == 0.0 else '%.4g' % v)


JOINT = 'joint: bars, vacuum, eps_w, rem'
GROUPS = [  # (label, hook maker, kind, cap, part, verdicts it can move)
    ('19.1c bars, all', lambda x: {'bar_all': x}, 'mul', MCAP, 'M3', 'S5 S6 S7'),
    ('19.1c bars, Ritz (B5 Gram, CT)', lambda x: {'bar_ritz': x}, 'mul', MCAP, 'M3', 'S5 S6 S7'),
    ('19.1c bars, amplitudes A_a', lambda x: {'bar_amp': x}, 'mul', MCAP, 'M3', 'S5 S6 S7'),
    ('19.1c bar I3p', lambda x: {'bar_I3p': x}, 'mul', MCAP, 'M3', 'S6 S7'),
    ('19.1c bar Ip3', lambda x: {'bar_Ip3': x}, 'mul', MCAP, 'M3', 'S6 S7'),
    ('19.1c bar N_w', lambda x: {'bar_Nw': x}, 'mul', MCAP, 'M3', 'S6 S7'),
    ('19.1c bar N_delta', lambda x: {'bar_Ndel': x}, 'mul', MCAP, 'M3', 'S5 S7'),
    ('19.1c bar I_N', lambda x: {'bar_I_N': x}, 'mul', MCAP, 'M3', 'S5 S7'),
    ('19.1c bars endw (I_mix, I_free)', lambda x: {'bar_endw': x}, 'mul', MCAP, 'M3', 'S7'),
    ('central I3p lowered (relative)', lambda x: {'I3p_c': x}, 'rel', 0.99, 'M3', 'S6 S7'),
    ('central Ip3 raised (relative)', lambda x: {'Ip3_c': x}, 'rel', 0.99, 'M3', 'S6 S7'),
    ('central N_w lowered (relative)', lambda x: {'Nw_c': x}, 'rel', 0.99, 'M3', 'S6 S7'),
    ('vacuum, all', lambda x: {'vac_all': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),
    ('vacuum D5', lambda x: {'D5': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),
    ('vacuum gB', lambda x: {'gB': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),
    ('eps_delta of S5 (wres c_xi J/2, J)', lambda x: {'eps_ds5': x}, 'mul', MCAP, 'M2', 'S5 S7'),
    ('eps_a (wres c_xi J, 2J)', lambda x: {'eps_a': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),
    ('Lemma 19.5w eps_w, eps_d', lambda x: {'eps_w': x}, 'mul', MCAP, 'P3', 'S6 S7'),
    ('Lemma 19.4 rem', lambda x: {'remT': x}, 'mul', MCAP, 'S4', 'S6 S7'),
    ('U raised by (absolute)', lambda x: {'U_add': x}, 'add', 1.0, 'S4', 'S6 S7'),
    ('TRB (beta)', lambda x: {'TRB': x}, 'mul', MCAP, 'S4', 'S5 S6 S7'),
    (JOINT, lambda x: {'bar_all': x, 'vac_all': x, 'eps_w': x, 'remT': x}, 'mul', MCAP, 'all', 'S5 S6 S7'),
    ('R_w', lambda x: {'Rw': x}, 'mul', MCAP, 'S7', 'S7'),
    ('||B+-||', lambda x: {'nB': x}, 'mul', MCAP, 'S7', 'S7'),
    ('c_x (divided by)', lambda x: {'cx_div': x}, 'mul', MCAP, 'S7', 'S7'),
    ('C_1 = c5 (divided by)', lambda x: {'cov1_div': x}, 'mul', MCAP, 'S5', 'S7'),
]
GMAP = {g[0]: g for g in GROUPS}
LAST_GROUPS = ((JOINT, 'S5'), (JOINT, 'S6'), (JOINT, 'S7'), ('19.1c bars, all', 'S6'), ('U raised by (absolute)', 'S6'), ('TRB (beta)', 'S6'))

REVMAP = {  # the review label -> (hook maker, kind, cap), as P0
    'eps_w x': (lambda x: {'eps_w': x}, 'mul', MCAP), 'D5 (eps_r, s) x': (lambda x: {'D5': x}, 'mul', MCAP),
    'gB (eps_r and eps_w bad-bond part) x': (lambda x: {'gB': x}, 'mul', MCAP),
    'all Lemma 19.1c error bars (M2, B5, CT) x': (lambda x: {'bar_all': x}, 'mul', MCAP),
    'Ritz error bars (B5 Gram + CT T) x': (lambda x: {'bar_ritz': x}, 'mul', MCAP),
    'I3p error bar x': (lambda x: {'bar_I3p': x}, 'mul', MCAP), 'Ip3 error bar x': (lambda x: {'bar_Ip3': x}, 'mul', MCAP),
    'Nw error bar x': (lambda x: {'bar_Nw': x}, 'mul', MCAP), 'Lemma 19.4 remainder rem x': (lambda x: {'remT': x}, 'mul', MCAP),
    'TRB x': (lambda x: {'TRB': x}, 'mul', MCAP), 'U raised by (absolute)': (lambda x: {'U_add': x}, 'add', 1.0),
    'I3p central lowered by (relative)': (lambda x: {'I3p_c': x}, 'rel', 0.99),
    'Ip3 central raised by (relative)': (lambda x: {'Ip3_c': x}, 'rel', 0.99),
    'Nw central lowered by (relative)': (lambda x: {'Nw_c': x}, 'rel', 0.99),
    'R_w x': (lambda x: {'Rw': x}, 'mul', MCAP), '||B+||, ||B-|| x': (lambda x: {'nB': x}, 'mul', MCAP),
    'c_x /': (lambda x: {'cx_div': x}, 'mul', MCAP), 'Cov_1 /': (lambda x: {'cov1_div': x}, 'mul', MCAP),
    'U raised by': (lambda x: {'U_add': x}, 'add', 1.0),
}


# ------------------------------------------------------------------ C-REPRO: path B against path A
ALLPAIRS = [(kd, d) for kd in ('flip', 'same') for d in DS]
QKEYS = ('rho1', 'rho', 'Rp', 'vSv_p', 'vp', 'vSv_m', 'vm', 'nBp', 'nBm', 'Rw')
MKEYS = ('cx', 'r2', 'ro', 'al2', 'L2', 'mux', 'qx', 'ax', 'Dlt')
TOL_ONE = 1e-12


def rel(b, a):
    return abs(b - a) / max(abs(a), 1e-300)


def fnum(x):
    """a point interval (or a float) as a float, for the comparisons with path A."""
    return float(x.mid) if isinstance(x, IVT) else float(x)


def nf(x, n=6):
    """a short decimal of an interval's midpoint or a float (prints only)."""
    return '%.*g' % (n, fnum(x))


def cover_a(ns, Qa, Ma, pairs):
    """the author's coverage search (endpairs4 passes_jensen, passes_mode, with its Cov_1)."""
    res = {}
    for kd, d in pairs:
        m = 1
        while m <= MMAX and ns['passes_jensen'](Qa, d, m, kd):
            m += 1
        k = 1
        while k <= KMAX and not ns['passes_mode'](Qa, Ma, d, k, kd):
            k += 1
        res[(kd, d)] = (m - 1, k)
    return res


def never_better(rows):
    """names whose production bound beats path A's beyond TOL_ONE (a lower bound higher, an upper bound lower)."""
    bad = []
    for name, side, b, a in rows:
        b, a = fnum(b), fnum(a)
        if (side == 'lo' and b > a + TOL_ONE * abs(a)) or (side == 'hi' and b < a - TOL_ONE * abs(a)):
            bad.append(name)
    return bad


def repro_compare(inp, nsm, nse, nsb, Jlo, Jhi, sc=None, pairs=None):
    """C-REPRO on one piece (SPEC v1_1 sect. 4, ADD1 sect. 5). Path B with the naive enclosures and the author's forms against path A
    on every S5, S6 and S7 quantity (two-sided, relative TOL_B) and on the coverage tables (C_1 = path A's Cov_1); then path B with the
    production forms (RV13_1 N3), which must never beat path A beyond TOL_ONE. Returns (worst, its key, the violations, tables equal).
    Path B takes path A's FLOAT U and TRB here (float_s4): the comparison is of the arithmetic, on the same inputs (F2, v2_1)."""
    sc = {} if sc is None else sc
    inp = float_s4(inp)
    pairs = CLAIM[inp['N']] if pairs is None else pairs
    Rp_a, rho_a, er_a, ew_a, L1e_a, be_a, cr_a = nsm['check'](Jlo, Jhi)
    Qa = nse['quantities'](Jlo, Jhi)
    Ma = nse['mode_data'](Jlo, Jhi, Qa)
    cA, evA, odA, vtA, erA, svA, beA = nsb['cov_lower'](Jlo, Jhi)
    B = piece_eval(inp, Jlo, Jhi, dict(sc, author_forms=True), use_centered=False, C1=inp['P']['cov1'], full=True, pairs=pairs)
    Qb, Mb, Sb, Vb = B['Q'], B['Mq'], B['S5'], B['V']
    rows = [('S6 R+', Qb['Rp'], Rp_a), ('S6 rho', Qb['rho'], rho_a), ('S6 L1e', Qb['L1'], L1e_a), ('S6 beta', Qb['beta'], be_a),
            ('S6 eps_r', Vb['eps_r'], er_a), ('S6 eps_w', Vb['eps_w'], ew_a), ('S7 eps_w', Vb['eps_w'], Qa['eps_w']),
            ('S7 eps_d', Vb['eps_d'], Qa['eps_d'])]
    rows += [('S7 ' + k, Qb[k], Qa[k]) for k in QKEYS] + [('S7 ' + k, Mb[k], Ma[k]) for k in MKEYS]
    rows += [('S5 c5', Sb['c5'], cA.a), ('S5 even', Sb['even'].a, evA.a), ('S5 odd', Sb['odd'].b, odA.b), ('S5 vacT', Sb['vacT'].b, vtA.b),
             ('S5 beta', Sb['beta'], beA.b), ('S5 eps_r', Vb['eps_r'], erA), ('S5 s', Vb['s'], svA)]
    worst, wk = 0.0, ''
    for name, b, a in rows:
        r_ = rel(fnum(b), fnum(a))
        if r_ > worst:
            worst, wk = r_, name
    cov_same = B['cv'] == cover_a(nse, Qa, Ma, pairs)
    P_ = piece_eval(inp, Jlo, Jhi, dict(sc), use_centered=False, C1=inp['P']['cov1'], pairs=pairs)
    viol = never_better([('R+', 'lo', P_['Q']['Rp'], Rp_a), ('rho', 'hi', P_['Q']['rho'], rho_a), ('rho1', 'hi', P_['Q']['rho1'], Qa['rho1']),
                         ('c_x', 'lo', P_['Mq']['cx'], Ma['cx']), ('c5', 'lo', P_['S5']['c5'], cA.a)])
    return worst, wk, viol, cov_same


# ------------------------------------------------------------------ C-PIECE, C-UNIF, C-PARITY, C-MODULE, C-TAG
LOWER_KEYS = ('Rp', 'vSv_p', 'mux', 'qx', 'ax', 'al2', 'cx', 'c5', 'even')
UPPER_KEYS = ('rho1', 'rho', 'L1', 'beta', 'vp', 'vSv_m', 'vm', 'nBp', 'nBm', 'Rw', 'L2', 'r2', 'ro', 'Dlt', 'odd', 'vacT')


def piece_str(Jlo, Jhi):
    return '%.2f, %s' % (Jlo, 'inf' if Jhi is None else '%.2f' % Jhi)


def bounds_of(E):
    """a piece evaluation's one-sided bounds: lower ends of the lower bounds, upper ends of the upper bounds."""
    src = dict(E['Q'])
    src.update(E['Mq'])
    src.update(c5=E['S5']['c5'], even=E['S5']['even'], odd=E['S5']['odd'], vacT=E['S5']['vacT'])
    b = {k: ('lo', pt(src[k]).a) for k in LOWER_KEYS}
    b.update({k: ('hi', pt(src[k]).b) for k in UPPER_KEYS})
    return b


def outward(fb, hb):
    """the largest relative outward move of a half piece's bounds against the piece's own (> 0: moved outward), and its key."""
    worst, wk = -1.0, ''
    for k, (side, fv) in fb.items():
        hv = hb[k][1]
        d = (fv - hv) if side == 'lo' else (hv - fv)
        den = abs(fv) if (abs(fv) > 0) is True else pt(1e-300)
        r_ = float((d / den).b)
        if r_ > worst:
            worst, wk = r_, k
    return worst, wk


def entry_names(inp):
    return ([('M2', n) for n in sorted(inp['M2']['items'])] + [('B5', n) for n in sorted(inp['B5']['items'])]
            + [('CT', n) for n in sorted(inp['CT']['items'])] + [('B4', 'I_N')] + [('EW', n) for n in sorted(inp['EW']['items'])])


def piece_terms(cx, Ub, V, kind):
    """the terms C-PIECE compares (S3): every stored entry, U, m-hat, the even and odd Ritz matrices and S5's parts, in one kind ('naive'
    over the piece, or 'point' at cx.tm, both with bars). The naive differences of rho^2, L1 and L2 are left out: only their upper ends
    are bounds, and those enter the final bounds, which are compared separately."""
    T = {'%s %s' % nm: cx.entry(nm[0], nm[1], kind) for nm in entry_names(cx.inp)}
    T['U'], T['m-hat'] = cx.U(kind), cx.mhat(kind)
    Ae, Ao = ritz_matrix(cx, Ub, 'even', kind), ritz_matrix(cx, Ub, 'odd', kind)
    T.update(('Ritz even %d%d' % (i, j), Ae[i][j]) for i in range(3) for j in range(3))
    T['Ritz odd'] = Ao[0][0]
    S5 = s5_parts(cx, V, kind)
    T.update({'S5 even': S5['even'], 'S5 odd': S5['odd'], 'S5 even - odd': S5['Dd']})
    return T


def piece_check(inp, Jlo, Jhi, sc=None):
    """C-PIECE (S3, N-f), on the naive enclosures. Every term of each half piece (with the piece's preconditioner, vacuum point and index
    order) lies in the piece's own enclosure, and no final bound moves outward beyond 1e-15. The piece's enclosure contains the point
    evaluations, with bars, at its two ends and its midpoint (computed without the PLANT-RIGHTEND hook). Returns (the failing terms, the
    largest relative outward move of a final bound, its key)."""
    sc = {} if sc is None else sc
    full = piece_eval(inp, Jlo, Jhi, sc, use_centered=False)
    cx, Ub, V = full['cx'], full['Ub'], full['V']
    Tf = piece_terms(cx, Ub, V, 'naive')
    fb = bounds_of(full)
    order = order_from_central(cx, Ub)
    Jm = 2 * Jlo if Jhi is None else math.sqrt(Jlo * Jhi)
    bad, worst, wk = set(), -1.0, ''
    for a, b in ((Jlo, Jm), (Jm, Jhi)):
        h = piece_eval(inp, a, b, sc, use_centered=False, Ub=Ub, Jvac=Jlo, order=order)
        Th = piece_terms(h['cx'], Ub, h['V'], 'naive')
        bad.update('half [%s] %s' % (piece_str(a, b), k) for k in Tf if not contains(Tf[k], Th[k]))
        w, k = outward(fb, bounds_of(h))
        if w > worst:
            worst, wk = w, k
    clean = {k: v for k, v in sc.items() if k != 'right_end'}
    for tv in (cx.tI.a, cx.tm, cx.tI.b):
        sub = Ctx(inp, Jlo, Jhi, clean)
        sub.tm = iv.mpf([pt(tv).a, pt(tv).a])
        sub.cache['order'] = order
        Tp = piece_terms(sub, Ub, V, 'point')
        bad.update('point t = %s %s' % (nf(tv, 8), k) for k in Tp if not contains(Tf[k], Tp[k]))
    return sorted(bad), worst, wk


MVB_ENTRIES = ([('B5', 'g,%d,%d' % ab) for ab in ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3), (2, 2))]
               + [('CT', 'T,%d,%d' % ab) for ab in ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3), (2, 2))]
               + [('B5', 'A,0'), ('B5', 'A,1'), ('B5', 'A,3'), ('B4', 'I_N'), ('B5', 'Ndel')])


def mvb_values(cx, Ub, V, tval, offsets):
    """the four smooth functions at the point inputs c(tval) + delta, delta = offsets x bars (kind 'offset'), with the piece's fixed index
    order and constant radius."""
    sub = Ctx(cx.inp, cx.Jlo, cx.Jhi, dict(cx.sc, offsets=offsets))
    sub.tm = tval
    sub.cache['order'] = order_from_central(cx, Ub)
    sub.cache['R_iy'] = radius_const(cx, Ub)
    r = dict(udiffs(sub, Ub, 'offset'))
    r['S5 Dd'] = s5_parts(sub, V, 'offset')['Dd']
    return r


def mvb_check(cx, Ub, V, bar_free=False):
    """C-MV-B (S4): at 9 equispaced points t_j, f(c(t_j) + delta) with point inputs, for delta = 0 and delta = +-(bar x sign of the
    gradient of f at c(t_m)) per function, lies in F(t_m) + D(P)[-h, h]. The signs come from symmetric differences of one bar per entry.
    bar_free is the plant (F(t_m) evaluated with B = 0). Returns the failing functions."""
    kindF = 'central' if bar_free else 'point'
    Fm = dict(udiffs(cx, Ub, kindF))
    Fm['S5 Dd'] = s5_parts(cx, V, kindF)['Dd']
    Dp = dict(ud_kind(cx, Ub, 'dual'))
    Dp['S5 Dd'] = s5_parts(cx, V, 'dual')['Dd']
    enc = {k: Fm[k] + Dp[k].d * cx.h * iv.mpf([-1, 1]) for k in MV_KEYS}
    sg = {k: {} for k in MV_KEYS}
    for e in MVB_ENTRIES:
        vp, vm = mvb_values(cx, Ub, V, cx.tm, {e: 1}), mvb_values(cx, Ub, V, cx.tm, {e: -1})
        for k in MV_KEYS:
            d = fnum(vp[k]) - fnum(vm[k])
            sg[k][e] = 1 if d > 0 else (-1 if d < 0 else 0)
    bad = set()
    for j in range(9):
        tj = cx.tI.a + (cx.tI.b - cx.tI.a) * j / 8
        tval = iv.mpf([tj.a, tj.a])
        v0 = mvb_values(cx, Ub, V, tval, {})
        bad.update(k for k in MV_KEYS if not contains(enc[k], v0[k]))
        for k in MV_KEYS:
            for s_ in (1, -1):
                if not contains(enc[k], mvb_values(cx, Ub, V, tval, {e: s_ * sg[k][e] for e in MVB_ENTRIES})[k]):
                    bad.add(k)
    return sorted(bad)


def unif_check(cx):
    """C-UNIF: on the piece, the bar-free interval enclosures ('cnaive') of every stored entry, of U and of m-hat contain their values at
    9 equispaced t (computed without the PLANT-RIGHTEND hook). Returns the names that fail."""
    inp = cx.inp
    names = entry_names(inp)
    enc = {'%s %s' % nm: cx.entry(nm[0], nm[1], 'cnaive') for nm in names}
    enc['U'], enc['m-hat'] = cx.U('cnaive'), cx.mhat('cnaive')
    clean = {k: v for k, v in cx.sc.items() if k != 'right_end'}
    bad = set()
    for j in range(9):
        sub = Ctx(inp, cx.Jlo, cx.Jhi, clean)
        tj = cx.tI.a + (cx.tI.b - cx.tI.a) * j / 8
        sub.tm = iv.mpf([tj.a, tj.a])
        val = {'%s %s' % nm: sub.entry(nm[0], nm[1], 'central') for nm in names}
        val['U'], val['m-hat'] = sub.U('central'), sub.mhat('central')
        bad.update(k for k in enc if not contains(enc[k], val[k]))
    return sorted(bad)


PARITY_KEYS = ('g,0,2', 'g,1,2', 'g,2,3')


def parity_max(B5):
    """C-PARITY: the largest |a_k| of the cross-parity Gram entries; exactly 0 for symmetrized trial vectors (v1_1 sect. 4)."""
    return max(abs(a) for k in PARITY_KEYS for a in B5['items'][k]['ak'])


VERDICT_FUNCS = ('Ctx', 'D', 'lift', 'dsum', 'nn', 'sqrt_any', 'chol', 'lsolve', 'congruent', 'pieces', 't_interval', 'ritz_matrix',
                 'gersh_lo', 'radius_const', 'udiffs', 'ud_kind', 'centered', 'quantities', 'mode', 'pj', 'pm', 's7mono_hyp', 'coverage',
                 'coverage_claim', 'claim_holds', 's5_parts', 's5_bound', 'piece_eval', 'isect', 'pmax', 'pmin', 'finite',
                 'pt', 'dec_frac', 'dec_iv', 's4u_read_port', 's4u_ball', 's4u_src_check', 's4u_pos', 'provide_s4u', 'tag_certified',
                 'verdict_word', 'u_minus_float', 'ceil_sig', 's4_kr34',    # N-a: pt(), the S4-U provider, its readers, the tag functions
                 's4t_src_check', 'provide_s4trb',                         # v2_1: the S4-TRB provider and its source check
                 'r_main_iv', 'det_iv')                                    # v2_2 (1): r_main in mp.iv
FORBIDDEN = (r'\bnp\.linalg', r'\bsla\.', r'\bmath\.', r'\berfc\b', r'(?<![\w.])float\(', r'\*\* *0?\.5', r'(?<![\w.])pow\(',
             r'\bnumpy\b', r'\bscipy\b', r'\bflint\b')


def module_scan(srcs):
    """C-MODULE: no libm, numpy, scipy, erfc, python-flint, float conversion or fractional power in a verdict-path function or class.
    The allowed float uses sit outside: the eigh preconditioner (ritz_basis, an exact matrix afterwards), the index order
    (order_from_central, any fixed choice is valid) and the FLOAT providers (vac_float), which the certified item replaces."""
    return [(name, pat) for name, src in sorted(srcs.items()) for pat in FORBIDDEN if re.search(pat, src)]


def tag_certified(name, tag, pins=None):
    """F1, the allowlist: a tag is certified only if it equals 'CERTIFIED <producer> <sha8>' exactly, with that input's pinned producer
    and sha8 (TAG_PINS, or the control's pins). Anything else reads not certified: 'FLOAT ...', 'S4-TRB, pending', 'PENDING', a typo,
    another producer or sha8, an input without a pin."""
    pins = TAG_PINS if pins is None else pins
    return name in pins and tag == 'CERTIFIED %s %s' % pins[name]


def verdict_word(tags, passed, pins=None):
    """C-TAG: FAIL if the verdict fails; CERTIFIED only when every input tag is certified (tag_certified); FLOAT-PASS otherwise, which
    covers P4's partial flips. (v1_2's 'declared' argument is gone: the tags alone decide, through the allowlist.)"""
    if not passed:
        return 'FAIL'
    return 'CERTIFIED' if (len(tags) > 0 and all(tag_certified(k, v, pins) for k, v in tags.items())) else 'FLOAT-PASS'


class BudgetShort(Exception):
    pass


def budget(need, what):
    """stop cleanly (INCOMPLETE) when fewer than need CPU seconds remain before the soft cap."""
    if cpu() + need > LIM - 2:
        raise BudgetShort('%s at cpu %.1f s' % (what, cpu()))


# ------------------------------------------------------------------ the S4-U provider (F1, F2, S3) and the margin plants (S1, D2)
S4U_BALLS = ('LEAD', 'C1', 'C2', 'C3')
S4U_HEADER = dict(FORMAT=S4U['fmt'], RECORD=S4U['record'], END=S4U['record'], AUTHOR=S4U['producer'], J_MIN='300',
                  TARGET_U_MINUS_FLOAT='7.8e-4', TARGET_QUAD='3.9e-4')
# D-1: R_CERT's pieces, each with its record keys for the output and the code, and the READING line of that asm output (N filled in)
S4U_PIECES = (('PREF2_RE', 'PREF2_RE_OUTPUT', 'PREF2_RE_CODE',
               r'READING N=%d \(t = 1/300, every J >= 300\): pref\^2 R_E <= ([0-9.e+-]+); .*'),
              ('PREF2_RHO4', 'PREF2_RHO4_OUTPUT', 'PREF2_RHO4_CODE',
               r'READING N=%d \(t = 1/300, every J >= 300; S4_M2C_DESIGN_v1\): pref\^2 rho4 <= ([0-9.e+-]+); .*'),
              ('M3_SUM', 'M3_OUTPUT', 'M3_CODE',
               r'READING N=%d \(t = 1/300, every J >= 300\): pref\^2 \(tail \+ annulus\) \+ far \+ equator <= ([0-9.e+-]+)'))
S4U_PER_N = (tuple(b + e for b in S4U_BALLS for e in ('', '_LO', '_HI')) + tuple(k for pc in S4U_PIECES for k in pc[:3])
             + ('R_CERT', 'QUAD_TW_PART', 'QUAD_TW_PART_EXACT', 'U_MINUS_FLOAT', 'U_EXACT', 'COEF_OUTPUT', 'U3_CODE'))
S4U_USED = tuple(S4U_HEADER) + tuple('N%d_%s' % (N, k) for N in (4, 3) for k in S4U_PER_N)


def dec_frac(s):
    """an S4U_KV_v1 number (a decimal with optional sign, fraction and exponent) as an exact rational; anything else is an error."""
    if not isinstance(s, str) or re.fullmatch(r'-?[0-9]+(\.[0-9]+)?(e[+-]?[0-9]+)?', s) is None:
        raise ValueError('not a decimal number: %r' % (s,))
    return Fraction(s)


def dec_iv(s):
    """the exact decimal s as an mp.iv enclosure: numerator / denominator in outward interval arithmetic (no decimal string rounding)."""
    q = dec_frac(s)
    return pt(q.numerator) / pt(q.denominator)


def s4u_read_port(text):
    """the port's reader of format S4U_KV_v1 (S3): the text split at newlines; a line starting with # is a comment and a blank line
    carries nothing; every other line is KEY = value with KEY of [A-Z][A-Z0-9_]*, cut at its first ' = ', the value kept as it stands;
    any other line or a repeated KEY is an error. It shares no code with the reference parser (S4U_REF), which C-FMT holds it against."""
    rec = {}
    for no, ln in enumerate(text.split('\n'), 1):
        if ln.startswith('#') or ln.strip() == '':
            continue
        key, sep, val = ln.partition(' = ')
        if sep != ' = ' or re.fullmatch(r'[A-Z][A-Z0-9_]*', key) is None or key in rec:
            raise ValueError('S4U_KV_v1, port reader: line %d is not a new KEY = value' % no)
        rec[key] = val
    return rec


def s4u_ball(s):
    """a printed ball '[mid +/- rad]' of s4c_m2ba as the exact pair (mid, rad)."""
    m = re.fullmatch(r'\[([0-9.e+-]+) \+/- ([0-9.e+-]+)\]', s) if isinstance(s, str) else None
    if m is None:
        raise ValueError('not a ball: %r' % (s,))
    return dec_frac(m.group(1)), dec_frac(m.group(2))


def ceil_sig(x, n):
    """the smallest decimal with n significant digits that is >= x, for x > 0, exactly (the record's 'rounded up at 3 digits')."""
    e = 0
    while x >= Fraction(10) ** (e + n):
        e += 1
    while x < Fraction(10) ** (e + n - 1):
        e -= 1
    q = x / Fraction(10) ** e
    return -((-q.numerator) // q.denominator) * Fraction(10) ** e


def s4u_src_check(rec, srcs, asm):
    """C-SRC (S3, D-1), per N, against sha-pinned producing outputs. (a) The balls N*_LEAD and N*_C1..C3 equal, as strings, those of
    s4c_m2ba's C-NORM and C-C123 lines (srcs[N]: each line found once and reading PASS; its C-POS line PASS, its verdict VALID, its
    header ITEM n<N>); N*_COEF_OUTPUT names that output and N*_U3_CODE the code sha8 of its header; every *_LO and *_HI equals
    mid - rad and mid + rad exactly. (b) D-1: N*_PREF2_RE, N*_PREF2_RHO4 and N*_M3_SUM equal, as strings, the READING lines of their asm
    outputs (asm[(N, key)]: each line found once, with CHECKS all PASS, VERDICT VALID and the header ITEM=n<N> asm); the record's
    _OUTPUT token names that output and its first _CODE token the program and code sha8 of that header; N*_R_CERT is their exact sum
    (R_CERT_RULE); N*_QUAD_TW_PART_EXACT is 0.071 (PREF2_RE + PREF2_RHO4) + M3_SUM + 1e-11 exactly and N*_QUAD_TW_PART is it rounded up
    at 3 significant digits (QUAD_TW_PART_RULE). Returns the failures."""
    bad = []
    for N in (4, 3):
        p = 'N%d_' % N
        lines = srcs[N].split('\n')
        pats = dict(norm=r'C-NORM N=%d: pref\^2 J0 = (\[[^\]]*\]): PASS' % N,
                    c123=r'C-C123 N=%d: c1 = (\[[^\]]*\]), c2 = (\[[^\]]*\]), c3 = (\[[^\]]*\]) \(twrig6z [^)]*\), window 1e-6: PASS' % N,
                    pos=r'C-POS N=%d: c1, c2, c3 > 0: PASS' % N, verdict=r'VERDICT VALID',
                    head=r's4c_m2ba sha256 ([0-9a-f]{64}) ITEM=n%d LIM=[0-9]+' % N)
        hit = {}
        for k, pat in pats.items():
            ms = [m for m in (re.fullmatch(pat, ln) for ln in lines) if m is not None]
            if len(ms) == 1:
                hit[k] = ms[0]
            else:
                bad.append('%ss4c line %s found %d times' % (p, k, len(ms)))
        if 'norm' in hit and rec.get(p + 'LEAD') != hit['norm'].group(1):
            bad.append(p + 'LEAD against C-NORM')
        for i in (1, 2, 3):
            if 'c123' in hit and rec.get(p + 'C%d' % i) != hit['c123'].group(i):
                bad.append(p + 'C%d against C-C123' % i)
        if rec.get(p + 'COEF_OUTPUT') != '%s:%s' % (S4U_SRC[N][0], S4U_SRC[N][1][:8]):
            bad.append(p + 'COEF_OUTPUT')
        if 'head' in hit and rec.get(p + 'U3_CODE') != 'pk05/s4c_m2ba.py:%s' % hit['head'].group(1)[:8]:
            bad.append(p + 'U3_CODE against the header')
        for b in S4U_BALLS:
            try:
                mid, rad = s4u_ball(rec.get(p + b))
                if dec_frac(rec.get(p + b + '_LO')) != mid - rad:
                    bad.append(p + b + '_LO')
                if dec_frac(rec.get(p + b + '_HI')) != mid + rad:
                    bad.append(p + b + '_HI')
            except ValueError:
                bad.append(p + b + ' unreadable')
        for key, okey, ckey, rpat in S4U_PIECES:                         # D-1
            lines = asm[(N, key)].split('\n')
            pats = dict(reading=rpat % N, checks=r'CHECKS all PASS', verdict=r'VERDICT VALID',
                        head=r'(px08_[a-z0-9_]+) sha256 ([0-9a-f]{64}) ITEM=n%d asm LIM=[0-9]+.*' % N)
            hit = {}
            for k, pat in pats.items():
                ms = [m for m in (re.fullmatch(pat, ln) for ln in lines) if m is not None]
                if len(ms) == 1:
                    hit[k] = ms[0]
                else:
                    bad.append('%s%s: asm line %s found %d times' % (p, key, k, len(ms)))
            if 'reading' in hit and rec.get(p + key) != hit['reading'].group(1):
                bad.append(p + key + ' against its READING')
            if rec.get(p + okey) != '%s:%s' % (S4U_ASM[(N, key)][0], S4U_ASM[(N, key)][1][:8]):
                bad.append(p + okey)
            if 'head' in hit and str(rec.get(p + ckey)).split(' ; ')[0] != 'pk08/%s.py:%s' % (hit['head'].group(1),
                                                                                                hit['head'].group(2)[:8]):
                bad.append(p + ckey + ' against the header')
        try:
            r_e, r_h, m_3 = (dec_frac(rec.get(p + k)) for k in ('PREF2_RE', 'PREF2_RHO4', 'M3_SUM'))
            if dec_frac(rec.get(p + 'R_CERT')) != r_e + r_h + m_3:
                bad.append(p + 'R_CERT (R_CERT_RULE)')
            qx = dec_frac(rec.get(p + 'QUAD_TW_PART_EXACT'))
            if qx != dec_frac('0.071') * (r_e + r_h) + m_3 + dec_frac('1e-11'):
                bad.append(p + 'QUAD_TW_PART_EXACT (QUAD_TW_PART_RULE)')
            if qx <= 0 or dec_frac(rec.get(p + 'QUAD_TW_PART')) != ceil_sig(qx, 3):
                bad.append(p + 'QUAD_TW_PART (rounded up at 3 digits)')
        except ValueError:
            bad.append(p + 'R_CERT or QUAD_TW_PART unreadable')
    return bad


def s4u_pos(rec):
    """C-POS (F2): N*_LEAD_LO, N*_C1_LO, N*_C2_LO, N*_C3_LO > 0 exactly. With lead in [LEAD_LO, LEAD_HI] and c_i in [C_i_LO, C_i_HI]
    this gives lead (1 + c1 t + c2 t^2 + c3 t^3) <= LEAD_HI (1 + C1_HI t + C2_HI t^2 + C3_HI t^3) for every t > 0. Returns the failing
    keys; an unreadable value fails."""
    bad = []
    for N in (4, 3):
        for b in S4U_BALLS:
            k = 'N%d_%s_LO' % (N, b)
            try:
                if not dec_frac(rec.get(k)) > 0:
                    bad.append(k)
            except ValueError:
                bad.append(k)
    return bad


def s4u_swap(text, k1, k2):
    """a copy of the record's text with the values of the keys k1 and k2 exchanged (PLANT-FMT-S4U, PLANT-KEYSWAP)."""
    lines = text.split('\n')
    i1 = [i for i, ln in enumerate(lines) if ln.startswith(k1 + ' = ')]
    i2 = [i for i, ln in enumerate(lines) if ln.startswith(k2 + ' = ')]
    assert len(i1) == 1 and len(i2) == 1, 'the keys to swap are not each on one line'
    v1, v2 = lines[i1[0]][len(k1) + 3:], lines[i2[0]][len(k2) + 3:]
    lines[i1[0]], lines[i2[0]] = k1 + ' = ' + v2, k2 + ' = ' + v1
    return '\n'.join(lines)


def s4u_bump(s):
    """the decimal string s with the last digit of its mantissa moved by one (PLANT-RSRC)."""
    m = re.fullmatch(r'([^e]*)([0-9])(e[+-]?[0-9]+)?', s)
    return m.group(1) + str((int(m.group(2)) + 1) % 10) + (m.group(3) or '')


def provide_s4u(fails, fires):
    """the S4-U provider (F1, F2, S3, D-1). It reads pk08's record once and checks the bytes it parses (C-HASH, full sha256), parses
    them with the port's reader and with the reference parser (executed only after its own sha256 matches), and requires C-FMT (the
    two readers give the same keys and values, every key the port uses is present, the header keys are as pinned), C-SRC (s4c_m2ba's
    outputs and the three asm outputs per N, all sha-pinned) and C-POS, and that PLANT-FMT-S4U, PLANT-KEYSWAP, PLANT-RSRC and PLANT-POS
    fire. Only then does it set TAGS['S4 U'] to 'CERTIFIED <producer> <sha8>'. Returns, per N, the port's U tuple (LEAD_HI, C1_HI,
    C2_HI, C3_HI, R_CERT as exact-decimal enclosures) and the record's N*_QUAD_TW_PART and N*_U_MINUS_FLOAT strings."""
    with open(os.path.join(CODEDIR, S4U['path']), 'rb') as fh:
        raw = fh.read()
    with open(os.path.join(CODEDIR, S4U_REF[0]), 'rb') as fh:
        refb = fh.read()
    srcb, asmb = {}, {}
    for N in (4, 3):
        with open(os.path.join(CODEDIR, S4U_SRC[N][0]), 'rb') as fh:
            srcb[N] = fh.read()
    for nk, (path, _) in S4U_ASM.items():
        with open(os.path.join(CODEDIR, path), 'rb') as fh:
            asmb[nk] = fh.read()
    ok_h = (sha_bytes(raw) == S4U['sha256'], sha_bytes(refb) == S4U_REF[1], all(sha_bytes(srcb[N]) == S4U_SRC[N][1] for N in (4, 3)),
            all(sha_bytes(asmb[nk]) == S4U_ASM[nk][1] for nk in S4U_ASM))
    out('C-HASH S4-U (full sha256 of the bytes read here): record %s %s, reference parser %s %s, s4c_m2ba outputs %s, the %d asm '
        'outputs %s -> %s' % (S4U['path'], 'matches' if ok_h[0] else 'DIFFERS', S4U_REF[0], 'matches' if ok_h[1] else 'DIFFERS',
                              'match' if ok_h[2] else 'DIFFER', len(S4U_ASM), 'match' if ok_h[3] else 'DIFFER',
                              'PASS' if all(ok_h) else 'FAIL'))
    if not all(ok_h):
        fails.append('C-HASH S4-U')
        raise RuntimeError('S4-U provider: a pinned file differs from its pin; nothing is read from it')
    text = raw.decode('utf-8')
    srcs = {N: srcb[N].decode('utf-8') for N in (4, 3)}
    asm = {nk: asmb[nk].decode('utf-8') for nk in S4U_ASM}
    ns = {}
    exec(compile(refb.decode('utf-8'), S4U_REF[0], 'exec'), ns)
    ref_parse = ns['parse_s4u_kv']
    port, ref = s4u_read_port(text), ref_parse(text)
    diff = sorted(k for k in set(port) | set(ref) if port.get(k) != ref.get(k))
    miss = [k for k in S4U_USED if k not in port]
    hdr = [k for k, v in S4U_HEADER.items() if port.get(k) != v]
    ok_fmt = not diff and not miss and not hdr
    out('C-FMT S4-U (format %s): %d keys; the port\'s reader against the reference parser (%s, sha256 %s): %s; the %d keys the port uses '
        'present: %s; header keys %s as pinned: %s -> %s' % (
            S4U['fmt'], len(port), S4U_REF[0], S4U_REF[1][:8], 'identical' if not diff else 'DIFFER on %s' % ', '.join(diff[:6]),
            len(S4U_USED), 'yes' if not miss else 'NO (%s)' % ', '.join(miss[:6]), ', '.join(S4U_HEADER),
            'yes' if not hdr else 'NO (%s)' % ', '.join(hdr), 'PASS' if ok_fmt else 'FAIL'))
    if not ok_fmt:
        fails.append('C-FMT S4-U')
    src_bad = s4u_src_check(port, srcs, asm)
    out('C-SRC S4-U: N*_LEAD and N*_C1..C3 against the C-NORM and C-C123 lines of %s and %s (C-POS PASS and VERDICT VALID there), '
        'COEF_OUTPUT and U3_CODE, the 16 _LO/_HI ends as mid -+ rad exactly; D-1: N*_PREF2_RE, N*_PREF2_RHO4 and N*_M3_SUM against the '
        'READING lines of %s (CHECKS all PASS and VERDICT VALID there), their _OUTPUT and _CODE tokens, R_CERT = PREF2_RE + PREF2_RHO4 '
        '+ M3_SUM exactly, QUAD_TW_PART_EXACT = 0.071 (PREF2_RE + PREF2_RHO4) + M3_SUM + 1e-11 exactly and QUAD_TW_PART = it rounded up '
        'at 3 digits -> %s' % (S4U_SRC[4][0], S4U_SRC[3][0], ', '.join(S4U_ASM[nk][0] for nk in sorted(S4U_ASM)),
                              'PASS' if not src_bad else 'FAIL (%s)' % ', '.join(src_bad[:6])))
    if src_bad:
        fails.append('C-SRC S4-U')
    pos_bad = s4u_pos(port)
    out('C-POS S4-U: N*_LEAD_LO, N*_C1_LO, N*_C2_LO, N*_C3_LO > 0 exactly, so the HI ends bound U3 from above for t > 0 -> %s' % (
        'PASS' if not pos_bad else 'FAIL (%s)' % ', '.join(pos_bad)))
    if pos_bad:
        fails.append('C-POS S4-U')
    sw = s4u_swap(text, 'N4_C1_HI', 'N4_C2_HI')
    port_sw, ref_sw = s4u_read_port(sw), ref_parse(sw)
    fired_f = sw != text and port_sw != ref
    out('PLANT-FMT-S4U (the port reads a copy with N4_C1_HI and N4_C2_HI swapped, the reference parser reads the record): C-FMT %s -> %s'
        % ('differs' if port_sw != ref else 'agrees', 'FIRES' if fired_f else 'DOES NOT FIRE'))
    if not fired_f:
        fires.append('PLANT-FMT-S4U')
    sw_bad = s4u_src_check(port_sw, srcs, asm)
    fired_k = sw != text and port_sw == ref_sw and bool(sw_bad)
    out('PLANT-KEYSWAP (both readers read the swapped copy): they agree: %s; C-SRC fails on %s -> %s' % (
        port_sw == ref_sw, ', '.join(sw_bad) if sw_bad else 'nothing', 'FIRES' if fired_k else 'DOES NOT FIRE'))
    if not fired_k:
        fires.append('PLANT-KEYSWAP')
    bumped = s4u_bump(port.get('N4_PREF2_RE', '0'))
    rs_bad = s4u_src_check(dict(port, N4_PREF2_RE=bumped), srcs, asm)
    fired_r = bumped != port.get('N4_PREF2_RE') and 'N4_PREF2_RE against its READING' in rs_bad
    out('PLANT-RSRC (D-1: N4_PREF2_RE set to %s in a copy): C-SRC fails on %s -> %s' % (
        bumped, ', '.join(rs_bad) if rs_bad else 'nothing', 'FIRES' if fired_r else 'DOES NOT FIRE'))
    if not fired_r:
        fires.append('PLANT-RSRC')
    neg_bad = s4u_pos(dict(port, N4_C1_LO='-' + port.get('N4_C1_LO', '')))
    fired_p = 'N4_C1_LO' in neg_bad
    out('PLANT-POS (N4_C1_LO negated in a copy): C-POS flags %s -> %s' % (', '.join(neg_bad) or 'nothing',
                                                                          'FIRES' if fired_p else 'DOES NOT FIRE'))
    if not fired_p:
        fires.append('PLANT-POS')
    U5, quad, umf = {}, {}, {}
    for N in (4, 3):
        p = 'N%d_' % N
        U5[N] = tuple(dec_iv(port[p + k]) for k in ('LEAD_HI', 'C1_HI', 'C2_HI', 'C3_HI', 'R_CERT'))
        quad[N], umf[N] = port[p + 'QUAD_TW_PART'], port[p + 'U_MINUS_FLOAT']
        ld, c1, c2, c3, rc = U5[N]
        t3 = pt(1) / 300
        u300 = ld * (1 + c1 * t3 + c2 * t3 * t3 + c3 * t3 * t3 * t3) + rc
        ue = dec_iv(port[p + 'U_EXACT'])
        out('INFO S4-U N=%d: the port\'s U at t = 1/300 is %s, below the record\'s U_EXACT %s: %s; as t -> 0 it tends to LEAD_HI + '
            'R_CERT = %s' % (N, str(u300), port[p + 'U_EXACT'], (u300.b <= ue.a) is True, str(ld + rc)))
    if ok_fmt and not src_bad and not pos_bad and fired_f and fired_k and fired_r and fired_p:
        TAGS['S4 U'] = 'CERTIFIED %s %s' % (S4U['producer'], sha_bytes(raw)[:8])
    out('S4-U provider: tag %r (reads certified: %s)' % (TAGS['S4 U'], tag_certified('S4 U', TAGS['S4 U'])))
    return dict(U5=U5, quad=quad, umf=umf)


# ------------------------------------------------------------------ the S4-TRB provider (v2_1)
S4T_HEADER = dict(FORMAT=S4T['fmt'], RECORD=S4T['record'], END=S4T['record'], AUTHOR=S4T['producer'], J_MIN='300',
                  TARGET_T2='N4 1.338859 ; N3 0.961107')
S4T_READ = ('TRB', 'TRB_MAIN', 'TRB_R3', 'TRB_RCUB', 'TRB_RF', 'TRB_TAIL', 'TRB_FAR', 'PR', 'TV')   # the READING line's values, in order
S4T_USED = tuple(S4T_HEADER) + ('CODE', 'CONSTANT_PER_N') + tuple('N%d_%s' % (N, k) for N in (4, 3)
                                                                  for k in S4T_READ + ('ASM_OUTPUT', 'VERDICT', 'T2_RESULT'))
S4T_READING = (r'READING N=%d \(t = 1/300, every J >= 300; S4_TRB_DESIGN_v2 item 2\): TRB_%d <= ([0-9.e+-]+); main <= ([0-9.e+-]+), '
               r'R3 <= ([0-9.e+-]+), R_cub <= ([0-9.e+-]+), R_F <= ([0-9.e+-]+), tail <= ([0-9.e+-]+), far <= ([0-9.e+-]+); '
               r'PR <= ([0-9.e+-]+); T_v <= ([0-9.e+-]+)')


def s4t_src_check(rec, asm):
    """C-SRC S4-TRB (v2_1), per N: N*_TRB, its pieces N*_TRB_MAIN .. N*_TRB_FAR, N*_PR and N*_TV equal, as strings,
    the nine values of the READING line of the sha-pinned asm output asm[N] (found once, with CHECKS all PASS, VERDICT VALID and the
    header ITEM=n<N> asm, whose code sha8 is the record's CODE sha8); N*_ASM_OUTPUT names that output; N*_VERDICT reads VALID and
    N*_T2_RESULT PASS. Returns the failures."""
    bad = []
    for N in (4, 3):
        p = 'N%d_' % N
        lines = asm[N].split('\n')
        pats = dict(reading=S4T_READING % (N, N), checks=r'CHECKS all PASS', verdict=r'VERDICT VALID',
                    head=r'px08_trbcert_[a-z0-9_]+ sha256 ([0-9a-f]{64}) ITEM=n%d asm LIM=[0-9]+.*' % N)
        hit = {}
        for k, pat in pats.items():
            ms = [m for m in (re.fullmatch(pat, ln) for ln in lines) if m is not None]
            if len(ms) == 1:
                hit[k] = ms[0]
            else:
                bad.append('%sasm line %s found %d times' % (p, k, len(ms)))
        if 'reading' in hit:
            for i, k in enumerate(S4T_READ):
                if rec.get(p + k) != hit['reading'].group(i + 1):
                    bad.append(p + k + ' against its READING')
        if rec.get(p + 'ASM_OUTPUT') != '%s:%s' % (S4T_ASM[N][0], S4T_ASM[N][1][:8]):
            bad.append(p + 'ASM_OUTPUT')
        if 'head' in hit and str(rec.get('CODE')).split(' ; ')[0].rpartition(':')[2] != hit['head'].group(1)[:8]:
            bad.append('CODE against the %sasm header' % p)
        if rec.get(p + 'VERDICT') != 'VALID' or rec.get(p + 'T2_RESULT') != 'PASS':
            bad.append(p + 'VERDICT or T2_RESULT')
    return bad


def provide_s4trb(fails, fires):
    """the S4-TRB provider (v2_1), built like provide_s4u. It reads pk08's TRB record once (C-HASH on the bytes it parses, with the
    reference parser and both asm outputs, full sha256), parses it with the port's S4U_KV_v1 reader and with the same reference parser
    (executed only after its sha256 matches), and requires C-FMT (identical keys and values, the keys the port uses present, the header
    keys as pinned) and C-SRC (s4t_src_check), and that PLANT-FMT-S4T and PLANT-TSRC fire. Only then does it set TAGS['S4 TRB'] to
    'CERTIFIED <producer> <sha8>'. Returns per N the record's N*_TRB as an exact-decimal enclosure (TRBv) and as its string (trb)."""
    with open(os.path.join(CODEDIR, S4T['path']), 'rb') as fh:
        raw = fh.read()
    with open(os.path.join(CODEDIR, S4U_REF[0]), 'rb') as fh:
        refb = fh.read()
    asmb = {}
    for N in (4, 3):
        with open(os.path.join(CODEDIR, S4T_ASM[N][0]), 'rb') as fh:
            asmb[N] = fh.read()
    ok_h = (sha_bytes(raw) == S4T['sha256'], sha_bytes(refb) == S4U_REF[1], all(sha_bytes(asmb[N]) == S4T_ASM[N][1] for N in (4, 3)))
    out('C-HASH S4-TRB (full sha256 of the bytes read here): record %s %s, reference parser %s %s, the 2 asm outputs %s -> %s' % (
        S4T['path'], 'matches' if ok_h[0] else 'DIFFERS', S4U_REF[0], 'matches' if ok_h[1] else 'DIFFERS',
        'match' if ok_h[2] else 'DIFFER', 'PASS' if all(ok_h) else 'FAIL'))
    if not all(ok_h):
        fails.append('C-HASH S4-TRB')
        raise RuntimeError('S4-TRB provider: a pinned file differs from its pin; nothing is read from it')
    text = raw.decode('utf-8')
    asm = {N: asmb[N].decode('utf-8') for N in (4, 3)}
    ns = {}
    exec(compile(refb.decode('utf-8'), S4U_REF[0], 'exec'), ns)
    ref_parse = ns['parse_s4u_kv']
    port, ref = s4u_read_port(text), ref_parse(text)
    diff = sorted(k for k in set(port) | set(ref) if port.get(k) != ref.get(k))
    miss = [k for k in S4T_USED if k not in port]
    hdr = [k for k, v in S4T_HEADER.items() if port.get(k) != v]
    ok_fmt = not diff and not miss and not hdr
    out('C-FMT S4-TRB (format %s): %d keys; the port\'s reader against the reference parser (%s, sha256 %s): %s; the %d keys the port '
        'uses present: %s; header keys %s as pinned: %s -> %s' % (
            S4T['fmt'], len(port), S4U_REF[0], S4U_REF[1][:8], 'identical' if not diff else 'DIFFER on %s' % ', '.join(diff[:6]),
            len(S4T_USED), 'yes' if not miss else 'NO (%s)' % ', '.join(miss[:6]), ', '.join(S4T_HEADER),
            'yes' if not hdr else 'NO (%s)' % ', '.join(hdr), 'PASS' if ok_fmt else 'FAIL'))
    if not ok_fmt:
        fails.append('C-FMT S4-TRB')
    src_bad = s4t_src_check(port, asm)
    out('C-SRC S4-TRB: N*_TRB, N*_TRB_MAIN .. N*_TRB_FAR, N*_PR and N*_TV against the READING lines of %s and %s (CHECKS all PASS and '
        'VERDICT VALID there, the header\'s code sha8 = the record\'s CODE), N*_ASM_OUTPUT, N*_VERDICT VALID, N*_T2_RESULT PASS -> %s' % (
            S4T_ASM[4][0], S4T_ASM[3][0], 'PASS' if not src_bad else 'FAIL (%s)' % ', '.join(src_bad[:6])))
    if src_bad:
        fails.append('C-SRC S4-TRB')
    sw = s4u_swap(text, 'N4_TRB', 'N3_TRB')
    port_sw = s4u_read_port(sw)
    fired_f = sw != text and port_sw != ref
    out('PLANT-FMT-S4T (the port reads a copy with N4_TRB and N3_TRB swapped, the reference parser reads the record): C-FMT %s -> %s' % (
        'differs' if port_sw != ref else 'agrees', 'FIRES' if fired_f else 'DOES NOT FIRE'))
    if not fired_f:
        fires.append('PLANT-FMT-S4T')
    bumped = s4u_bump(port.get('N4_TRB', '0'))
    ts_bad = s4t_src_check(dict(port, N4_TRB=bumped), asm)
    fired_t = bumped != port.get('N4_TRB') and 'N4_TRB against its READING' in ts_bad
    out('PLANT-TSRC (N4_TRB set to %s in a copy): C-SRC fails on %s -> %s' % (
        bumped, ', '.join(ts_bad) if ts_bad else 'nothing', 'FIRES' if fired_t else 'DOES NOT FIRE'))
    if not fired_t:
        fires.append('PLANT-TSRC')
    TRBv, trb = {}, {}
    for N in (4, 3):
        trb[N] = port['N%d_TRB' % N]
        TRBv[N] = dec_iv(trb[N])
        out('INFO S4-TRB N=%d: certified TRB %s, enclosed as %s, for every J >= 300 (CONSTANT_PER_N); the FLOAT TRB of PARAMS was %s' % (
            N, trb[N], str(TRBv[N]), PARAMS[N]['TRB']))
    if ok_fmt and not src_bad and fired_f and fired_t:
        TAGS['S4 TRB'] = 'CERTIFIED %s %s' % (S4T['producer'], sha_bytes(raw)[:8])
    out('S4-TRB provider: tag %r (reads certified: %s)' % (TAGS['S4 TRB'], tag_certified('S4 TRB', TAGS['S4 TRB'])))
    return dict(TRBv=TRBv, trb=trb)


def u_minus_float(inp, Jlo, Jhi):
    """F2 INFO and KR4: an enclosure, over the piece, of the certified U(t) minus the FLOAT U(t) = lead_f (1 + c1_f t + c2_f t^2 + c3_f t^3)
    + rem(170) of PARAMS (T2's baseline, SPEC sect. 3), as one polynomial in t with the coefficient differences (the naive enclosure
    over the piece, without the dependency loss of two separate evaluations)."""
    cu = [pt(x) for x in inp['U5']]
    fu = [pt(x) for x in inp['P']['trt2']]
    cs = [cu[0] - fu[0]] + [cu[0] * cu[k] - fu[0] * fu[k] for k in (1, 2, 3)]
    return Ctx(inp, Jlo, Jhi, {}).poly(cs, 'cnaive') + (cu[4] - fu[4])


def s4_kr34(INP, fails):
    """F2, D-2, v2_1: with S4-U and S4-TRB certified, KR3 (the record's N*_QUAD_TW_PART <= U_t/2 = 3.9e-4) and KR4 (joint form: certified
    U - float U <= +7.8e-4, T2's target, on every piece, float U = PARAMS trt2 with rem(170); and certified TRB <= 1.02 x PARAMS TRB,
    T2's target, exact decimals) are gates. A failure stops the port, naming the part (SPEC sect. 3 l.204-206, sect. 5 l.291), and
    enters the run's verdict. Prints F2's INFO (the per-piece extremes, beside the record's own N*_U_MINUS_FLOAT) and both KILL lines;
    returns (kr3, kr4). Called by both items."""
    STAGE[0] = 'KR3, KR4: S4-U and S4-TRB against their targets'
    ucert, tcert = tag_certified('S4 U', TAGS['S4 U']), tag_certified('S4 TRB', TAGS['S4 TRB'])
    ext = {}
    for N in (4, 3):
        hi_, lo_ = None, None
        for (Jlo, Jhi) in pieces():
            d = u_minus_float(INP[N], Jlo, Jhi)
            if hi_ is None or (d.b > hi_[0]) is True:
                hi_ = (pt(d.b), Jlo, Jhi)
            if lo_ is None or (d.a < lo_[0]) is True:
                lo_ = (pt(d.a), Jlo, Jhi)
        ext[N] = hi_
        out('INFO S4-U N=%d (F2): certified U(t) - float U(t) (float U = lead(1 + c1 t + c2 t^2 + c3 t^3) + rem(170), T2\'s baseline) over '
            'the %d pieces: at most %s (on [%s]), at least %s (on [%s]); beside it the record\'s own key N%d_U_MINUS_FLOAT = %s (its '
            'constant U minus S4\'s float U at J = 300, rem(170) not in it)' % (
                N, len(pieces()), nf(hi_[0], 8), piece_str(hi_[1], hi_[2]), nf(lo_[0], 8), piece_str(lo_[1], lo_[2]), N, INP[N]['umf']))
    kr3 = ucert and all(dec_frac(INP[N]['quad']) <= dec_frac(TGT_DEC['U']) / 2 for N in (4, 3))
    out('KILL KR3 (v1_2 form, pk08\'s quadrature error <= U_t/2 = %s; a gate): N=4 %s, N=3 %s (%s N*_QUAD_TW_PART, exact decimals; '
        'S4-U tag certified: %s) -> %s' % (TGT_DEC['QUAD'], INP[4]['quad'], INP[3]['quad'], S4U['record'], ucert,
                                           'PASS' if kr3 else 'KILL: S4 U (part pk08)'))
    kr4u = ucert and all((ext[N][0] <= dec_iv(TGT_DEC['U']).a) is True for N in (4, 3))
    kr4t = tcert and all(dec_frac(INP[N]['trb']) <= dec_frac(TGT_DEC['TRB']) * dec_frac(INP[N]['P']['TRB']) for N in (4, 3))
    kr4 = kr4u and kr4t
    out('KILL KR4 (joint form, a gate: a certified input looser than its T2 target stops the port): S4 U (part pk08): certified U - '
        'float U <= %s on every piece: N=4 at most %s, N=3 at most %s -> %s; S4 TRB (part pk08, v2_1): certified TRB <= %s x the FLOAT '
        'TRB, exact decimals: N=4 %s against %s x %s, N=3 %s against %s x %s (S4-TRB tag certified: %s) -> %s; M3 entries, M2 vacuum: '
        'FLOAT, not applicable -> %s' % (
            TGT_DEC['U'], nf(ext[4][0], 8), nf(ext[3][0], 8), 'PASS' if kr4u else 'KILL: S4 U looser than its target (part pk08)',
            TGT_DEC['TRB'], INP[4]['trb'], TGT_DEC['TRB'], INP[4]['P']['TRB'], INP[3]['trb'], TGT_DEC['TRB'], INP[3]['P']['TRB'], tcert,
            'PASS' if kr4t else 'KILL: S4 TRB looser than its target (part pk08)', 'PASS' if kr4 else 'KILL'))
    if not kr3:
        fails.append('KR3 (S4 U, part pk08)')
    if not kr4u:
        fails.append('KR4 (S4 U, part pk08)')
    if not kr4t:
        fails.append('KR4 (S4 TRB, part pk08)')
    return kr3, kr4


# ------------------------------------------------------------------ v2_2 (3): the per-piece export for S8
def dec_dir(x, up, sig=12):
    """a decimal string of sig significant digits that bounds the interval x from above (up) or from below (not up), certified by an
    exact interval comparison of its enclosure (dec_iv) with that end of x; it steps one unit in the last place until the comparison
    holds. float() only seeds the search."""
    v = pt(x).b if up else pt(x).a
    mant, ex = ('%.*e' % (sig - 1, float(v))).split('e')
    M, E = int(mant.replace('.', '')), int(ex) - (sig - 1)
    for _ in range(8):
        digits = str(abs(M))
        txt = ('-' if M < 0 else '') + digits[0] + ('.' + digits[1:] if len(digits) > 1 else '') + 'e%d' % (E + len(digits) - 1)
        d = dec_iv(txt)
        if ((d >= v) is True) if up else ((d <= v) is True):
            return txt
        M += 1 if up else -1
    raise ArithmeticError('no directed decimal found for %s' % str(v))


def export_row(Jlo, Jhi, N, E):
    """one piece's export values (strings) in EXPORT_FIELDS order, pk11's list for S8, in P2's units; *_lo are lower ends rounded
    down and *_hi upper ends rounded up (dec_dir):
    - jlo, jhi: the grid's float J ends (repr; 'inf' for the last piece's open end);
    - c5_lo: S5's bound, the flip m = 1 bulk covariance times J^2;
    - vSv_p_lo, vSv_m_hi: <v+, S v+> and <v-, S v-> (quantities' vSv_p, vSv_m); rp_lo, rho_hi, rho1_hi: R+, rho, rho1;
    - vp2_lo: |v+|^2 >= (sqrt(even) - Dlt)_+^2, from S5's Bessel term even = a_x^2 + a_y^2 on the trial vacuum (PK10_NOTES 19.3.3
      (iii)) and |v+ - v+^tr| <= |v - v^tr| <= Dlt (19.3.3 (vi); the flip projection does not increase norms); vp2_hi = |v+|^2 <= vp^2
      and vm2_hi = |v-|^2 <= vm^2 (quantities' vp, vm);
    - Bp_hi, Bm_hi: ||B+||, ||B-|| (quantities' nBp, nBm); cx_lo, r2_hi, ro_hi: the S7 mode inputs (mode); Rw_hi: R_w;
    - c_lo, c_hi: the bulk mean c = <u, T_xi+ u> / lam0 = kbar + <u, T_w~ u> / lam0, inside kbar -+ E_w with E_w as in t1; c_lo is kept
      >= 0 since xi+ >= 0.
    Then, per claimed pair, EXPORT_PAIR_FIELDS: kind, d, Jensen checked to m, the first mode success k (Lemma S7-mono covers
    m >= k + 1), and whether the claim holds."""
    Q, Mq, S5, cv, inp = E['Q'], E['Mq'], E['S5'], E['cv'], E['cx'].inp
    ev = S5['even'].a
    vpl = (iv.sqrt(pt(ev)) - pt(S5['Dlt'].b)).a if (ev > 0) is True else pt(0)
    vpl = pt(0) if (vpl < 0) is True else pt(vpl)
    kb = pt(inp['M2']['kbar'])
    cl = (kb - Q['Ew']).a
    cl = pt(0) if (cl < 0) is True else pt(cl)
    vals = [repr(Jlo), 'inf' if Jhi is None else repr(Jhi), dec_dir(S5['c5'], False), dec_dir(Q['vSv_p'], False),
            dec_dir(Q['vSv_m'], True), dec_dir(Q['Rp'], False), dec_dir(Q['rho'], True), dec_dir(Q['rho1'], True),
            dec_dir(vpl * vpl, False), dec_dir(Q['vp'] * Q['vp'], True), dec_dir(Q['vm'] * Q['vm'], True), dec_dir(Q['nBp'], True),
            dec_dir(Q['nBm'], True), dec_dir(Mq['cx'], False), dec_dir(Mq['r2'], True), dec_dir(Mq['ro'], True), dec_dir(Q['Rw'], True),
            dec_dir(cl, False), dec_dir(kb + Q['Ew'], True)]
    if len(vals) != len(EXPORT_FIELDS.split()):
        raise AssertionError('the export row does not match EXPORT_FIELDS')
    pairs = ['%s %d %d %d %s' % (p[0], p[1], cv[p][0], cv[p][1], 'yes' if claim_holds(cv, p) else 'no') for p in CLAIM[N]]
    return ' '.join(vals) + ' | ' + ' ; '.join(pairs)


def export_text(why):
    """the EXPORT_KT_S67_v1 text of this sweep (format S4U_KV_v1; kt_s67_export_reader_v1 states it). RUN_VERDICT is the run's validity
    so far (every control and plant of the sweep), EXPORT_STATUS the verdict word of the tags (CERTIFIED only when every input is
    certified and the run is valid), and each input's tag is written with its status."""
    key = lambda k: 'TAG_' + re.sub(r'[^A-Z0-9]+', '_', k.upper())
    lines = ['# EXPORT_KT_S67_v1: the per-piece S5, S6 and S7 bounds of %s (sweep) for S8; format S4U_KV_v1 ("KEY = value", lines '
             'starting with # are comments, blank lines carry nothing); the reader is %s.' % (LABEL, EXPORT_READER[0]),
             '# Piece lines: N<N>_P<index> = FIELDS values | the claimed pairs, " ; "-separated, each the PAIR_FIELDS values. *_lo are lower',
             '# bounds rounded down, *_hi upper bounds rounded up (certified by exact interval comparisons); jlo, jhi are the grid floats.',
             'FORMAT = S4U_KV_v1', 'RECORD = EXPORT_KT_S67_v1', 'PRODUCER = pk07',
             'CODE = pk07/%s.py:%s' % (LABEL, sha_file(os.path.abspath(__file__))[:8]), 'RUN = %s' % MODE,
             'RUN_VERDICT = %s' % ('VALID' if not why else 'INVALID'), 'EXPORT_STATUS = %s' % verdict_word(TAGS, not why),
             'FIELDS = %s' % EXPORT_FIELDS, 'PAIR_FIELDS = %s' % EXPORT_PAIR_FIELDS]
    for k, v in TAGS.items():
        lines += ['%s = %s' % (key(k), v), '%s_STATUS = %s' % (key(k), 'certified' if tag_certified(k, v) else 'FLOAT')]
    for N in (4, 3):
        lines += ['CLAIM_N%d = %s' % (N, ' ; '.join('%s %d' % p for p in CLAIM[N])), 'N%d_PIECES = %d' % (N, len(EXPORT_ROWS[N]))]
    for N in (4, 3):
        lines += ['N%d_P%04d = %s' % (N, i, row) for i, row in enumerate(EXPORT_ROWS[N])]
    return '\n'.join(lines + ['END = EXPORT_KT_S67_v1']) + '\n'


def c_export(text):
    """C-EXPORT (v2_2 (3)), on the export text before it is written. C-FMT: the port's S4U_KV_v1 reader and the reference parser give
    the same keys and values. The producer's reader (kt_s67_export_reader_v1, executed only after its sha256 matches) returns, for both
    N, every piece written, each value equal to the row's decimal and each pair as written. PLANT-EXPORT: a copy with one value moved
    by one unit in its last digit must fail that comparison. Returns (the failures, whether the plant fired)."""
    srcs = {}
    for path, sha in (EXPORT_READER, S4U_REF):
        with open(os.path.join(CODEDIR, path), 'rb') as fh:
            srcs[path] = fh.read()
        if sha_bytes(srcs[path]) != sha:
            return ['%s differs from its pin' % path], False
    ns, ns2 = {}, {}
    exec(compile(srcs[EXPORT_READER[0]].decode('utf-8'), EXPORT_READER[0], 'exec'), ns)
    exec(compile(srcs[S4U_REF[0]].decode('utf-8'), S4U_REF[0], 'exec'), ns2)
    bad = [] if s4u_read_port(text) == ns2['parse_s4u_kv'](text) else ['C-FMT: the two S4U_KV_v1 readers differ']

    def compare(t):
        try:
            got = ns['parse_export'](t)
        except ValueError as e:
            return ['reader: %s' % e]
        diff = []
        for N in (4, 3):
            P = got['pieces'].get(N, {})
            if len(P) != len(EXPORT_ROWS[N]):
                diff.append('N=%d: %d pieces read, %d written' % (N, len(P), len(EXPORT_ROWS[N])))
            for i, row in enumerate(EXPORT_ROWS[N]):
                left, _, right = row.partition(' | ')
                want = {nm: (None if tk == 'inf' else Fraction(tk)) for nm, tk in zip(EXPORT_FIELDS.split(), left.split(' '))}
                want['pairs'] = [dict(kind=g[0], d=int(g[1]), m_checked=int(g[2]), k_mode=int(g[3]), holds=g[4])
                                 for g in (grp.split(' ') for grp in right.split(' ; '))]
                if P.get(i) != want:
                    diff.append('N%d_P%04d' % (N, i))
        return diff
    bad += compare(text)
    row0 = EXPORT_ROWS[4][0]
    toks = row0.split(' ')
    planted = text.replace('N4_P0000 = ' + row0, 'N4_P0000 = ' + ' '.join(toks[:2] + [s4u_bump(toks[2])] + toks[3:]), 1)
    fired = planted != text and 'N4_P0000' in compare(planted)
    return bad, fired


def write_export(text):
    """writes the export as a new file in this folder's out/ (never over an existing one) and reads it back. Returns (path, the sha256 of
    the bytes read back, the line count)."""
    path = os.path.join(OUTD, 'export_%s_%s%s.kv' % (LABEL, MODE, ('_' + TAG) if TAG else ''))
    if os.path.realpath(os.path.dirname(path)) != os.path.realpath(OUTD):
        raise RuntimeError('the export path is outside out/')
    with open(path, 'x') as fh:
        fh.write(text)
    with open(path, 'rb') as fh:
        back = fh.read()
    if back != text.encode('utf-8'):
        raise RuntimeError('the export read back differs from the text written')
    return path, sha_bytes(back), text.count('\n')


def margin_plant(inp, Jlo, Jhi, mk, F, which, lose=None):
    """S1, D2 (the form of ADD1's S5 plants): F is the flip distance the scan bisected for the hook maker mk on this piece and verdict.
    The plant fires when the verdict holds at F / 1.1 and is lost at 1.1 F; with lose (D2), the loss is required of those pairs alone.
    A search that found no flip in its bracket (F None) or a failing baseline (F = 0) does not fire. The search (flip_search,
    unchanged from v1_2): 'mul' starts from the bracket [1, 2] and doubles it up to the cap MCAP = 2048, 'add' from [0, 1e-4] up to
    1.0; it then bisects until hi / lo <= 1.004 ('mul') or hi - lo <= 0.004 hi ('add'), and F = hi is the first failing value found.
    So F lies within relative 0.4% above the flip, and F / 1.1 and 1.1 F sit about 9% and 10% from it, over twenty times the
    search's resolution."""
    if not F:
        return False
    hold = verdict_one(inp, Jlo, Jhi, mk(F / 1.1), which)
    lost = not verdict_one(inp, Jlo, Jhi, mk(F * 1.1), which, claim=lose)
    return hold and lost


# ------------------------------------------------------------------ exact controls
def transfer_current_binding():
    """T(a_j, b_{j+1}) on the infinite unit-conductance 3-row strip, mode form (PK10 sect. 1); SPEC ADD1 C-C2."""
    def g(lam):
        ch = 1 + pt(lam) / 2
        sh = iv.sqrt(ch * ch - 1)
        return (ch - sh) / (2 * sh)
    return g(1) / 2 - 3 * g(3) / 2


def det_iv(A):
    """determinant of an interval matrix by Gaussian elimination (SPD here, no pivoting)."""
    n = len(A)
    M = [row[:] for row in A]
    det = pt(1)
    for i in range(n):
        det *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for c in range(i, n):
                M[r][c] = M[r][c] - f * M[i][c]
    return det


# ------------------------------------------------------------------ controls (both items)
def c_repro170(INP, NSM, NSE, NSB, fails, fires):
    """C-REPRO at [170, 171.7]: path A rebuilds the author's printed lines (m2_unif3, endpairs4, assemble_unif4) and the coverage
    lines; path B equals path A (repro_compare, all 24 coverage pairs); PLANT-S2UP and PLANT-PATHB fire."""
    J0, J0h = 170.0, 170.0 * 1.01
    for N in (4, 3):
        inp = INP[N]
        m2t = open(os.path.join(SC, 'm2_unif3_N%d.txt' % N)).read().split('\n')
        ept = open(os.path.join(SC, 'endpairs4_N%d.txt' % N)).read()
        ab4t = open(os.path.join(SC, 'assemble_unif4_N%d.txt' % N)).read().split('\n')
        rct = open(os.path.join(CODEDIR, 'pk20/rv13/c6/rc_end_sens_N%d.txt' % N)).read().split('# N = %d, J in [2e4' % N)[0]
        Rp, rho, er, ew, L1e, be, cr = NSM[N]['check'](J0, J0h)
        lineA = ('J in [%.1f, %s]: R+ >= %.5f, rho_odd <= %.5f (ratio %.4f) | eps_r %.2e eps_w %.3e L1e %.5f beta %.4f cross/H_T %.4f'
                 % (J0, '%.1f' % J0h, Rp, rho, Rp / rho, er, ew, L1e, be, cr))
        Qa = NSE[N]['quantities'](J0, J0h)
        Ma = NSE[N]['mode_data'](J0, J0h, Qa)
        lineE = ('J = %g: R_w <= %.5f, rho1 <= %.5f, rho <= %.5f, R+ >= %.5f; mode: q_x >= %.5f, L2 <= %.5f, mu_x >= %.5f, alpha^2 >= %.4f, '
                 '|a_x| >= %.5f, Dlt <= %.2e, c_x >= %.5f (|v+| <= %.5f), r2 <= %.4f, ro <= %.4f'
                 % (170.0, Qa['Rw'], Qa['rho1'], Qa['rho'], Qa['Rp'], Ma['qx'], Ma['L2'], Ma['mux'], Ma['al2'], Ma['ax'], Ma['Dlt'], Ma['cx'],
                    Qa['vp'], Ma['r2'], Ma['ro']))
        cA, evA, odA, vtA, erA, svA, beA = NSB[N]['cov_lower'](J0, J0h)
        lineB = ('J in [%.1f, %s]: Cov J^2 >= %.4e (even >= %.6f, odd <= %.6f, vac <= %.2e, eps_r %.2e, s %.2e, beta <= %.4f)'
                 % (J0, '%.1f' % J0h, float(cA.a), float(evA.a), float(odA.b), float(vtA.b), erA, svA, float(beA.b)))
        oks = (lineA == m2t[1], ('\n' + lineE + '\n') in ('\n' + ept), lineB == ab4t[1])
        rows = re.findall(r"  (flip|same) d=(\d+): own Jensen m<=(\d+), mode m>=(\d+), (?:FULL|not full) \| author's tests: Jensen m<=(\d+), "
                          r"mode m>=(\d+)", rct)
        cva = cover_a(NSE[N], Qa, Ma, [(kd, int(d)) for kd, d, _, _, _, _ in rows])
        okc = len(rows) >= 4 and all(cva[(kd, int(d))] == (int(mj), int(mm) - 1) for kd, d, _, _, mj, mm in rows)
        w, wk, viol, cs = repro_compare(inp, NSM[N], NSE[N], NSB[N], J0, J0h, pairs=ALLPAIRS)
        ok = all(oks) and okc and w <= TOL_B and not viol and cs
        wd = ['identical' if o else 'DIFFERS' for o in oks]
        out('C-REPRO N=%d [170, 171.7]: author lines m2_unif3 %s, endpairs4 J = 170 %s, assemble_unif4 %s; reference coverage lines (%d) %s; '
            'path B (naive, author forms) vs A: worst relative %.2e (%s), coverage tables (%d pairs) %s; production forms never better than '
            'A: %s -> %s' % (N, wd[0], wd[1], wd[2], len(rows), 'match' if okc else 'DIFFER', w, wk, len(ALLPAIRS),
                             'identical' if cs else 'DIFFER', 'yes' if not viol else 'NO (%s)' % ', '.join(viol), 'PASS' if ok else 'FAIL'))
        for o, mine, theirs in ((oks[0], lineA, m2t[1]), (oks[1], lineE, '(see endpairs4_N%d.txt)' % N), (oks[2], lineB, ab4t[1])):
            if not o:
                out('  mine:   %s' % mine)
                out('  author: %s' % theirs)
        if not ok:
            fails.append('C-REPRO N=%d' % N)
        out('INFO N=%d: S5 at [170, 171.7] by path A %.4e; the J >= 170 values: author (FLOAT Cov_1) %.4e, RV13_1 outward-endpoint arb %s' % (
            N, float(cA.a), inp['P']['cov1'], '1.1735e-4' if N == 4 else '2.2036e-4'))
        _, _, viol2, _ = repro_compare(inp, NSM[N], NSE[N], NSB[N], J0, J0h, sc={'s2_upper': True})
        fired = 'rho' in viol2
        out('PLANT-S2UP N=%d (S2_even from the upper ends of the diagonal): production bounds beat path A on %s -> %s' % (
            N, ', '.join(viol2) if viol2 else 'nothing', 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-S2UP N=%d' % N)
        w3, wk3, _, cs3 = repro_compare(inp, NSM[N], NSE[N], NSB[N], J0, J0h, sc={'drop_sp': True})
        fired = not (w3 <= TOL_B and cs3)
        out('PLANT-PATHB N=%d (path B with sp = 0): worst relative B-A %.2e (%s) -> %s' % (N, w3, wk3, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-PATHB N=%d' % N)


def c_c2(INP, fails, fires):
    """C-C2 (ADD1 sect. 5): the central S5 assembly at t = 0 equals c2 = (N - 1) T^2 / 2; PLANT-ODDSIGN and PLANT-T fire."""
    T = transfer_current_binding()
    V0 = dict(eps_ds5=pt(0))
    for N in (4, 3):
        c2 = (N - 1) * T * T / 2
        cx = Ctx(INP[N], 1e30, None, {})
        cx.tm = iv.mpf([0, 0])
        Dd0 = s5_parts(cx, V0, 'central')['Dd']
        rel_ = float((abs(Dd0 - c2).b / c2.a).b)
        ok = rel_ <= 1e-10
        out('C-C2 N=%d: T = %s, c2 = (N-1)T^2/2 = %s; central even - odd at t = 0: %s; relative %.1e -> %s' % (
            N, nf(T, 12), nf(c2, 10), nf(Dd0, 10), rel_, 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-C2 N=%d' % N)
        cxp = Ctx(INP[N], 1e30, None, {'odd_sign': True})
        cxp.tm = iv.mpf([0, 0])
        fired = float((abs(s5_parts(cxp, V0, 'central')['Dd'] - c2).b / c2.a).b) > 1e-10
        out('PLANT-ODDSIGN N=%d: C-C2 with the odd part added -> %s' % (N, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-ODDSIGN N=%d' % N)
    ch2 = 1 + pt(3) / 2
    Tbad = T + 3 * (ch2 - iv.sqrt(ch2 * ch2 - 1)) / (2 * iv.sqrt(ch2 * ch2 - 1))      # mode 2 weight +3/2 instead of -3/2
    cxb = Ctx(INP[4], 1e30, None, {})
    cxb.tm = iv.mpf([0, 0])
    c2bad = 3 * Tbad * Tbad / 2
    fired = float((abs(s5_parts(cxb, V0, 'central')['Dd'] - c2bad).b / c2bad.a).b) > 1e-10
    out('PLANT-T (N=4): C-C2 against the transfer current with mode 2 weight +3/2 -> %s' % ('FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-T')


def r_main_iv(N, swap=False):
    """v2_2 (1): endw's r_main by the matrix-tree theorem in mp.iv, (sqrt(det L_D det L_free) / det L_mix)^(N - 1), with
    the reduced Laplacians of the three 2-column graphs: closed-form triangle conductances A_EX = (3 + sqrt 21)/6 and B_EX =
    (3 sqrt 5 - sqrt 21)/12 (vacmod2 l.8-9, source-checked by C-HARM), unit verticals and horizontals. q (quantities) uses it in place
    of endw's stored float, and C-HARM compares the two. swap exchanges the two conductances (PLANT-HARM)."""
    a_ = (3 + iv.sqrt(21)) / 6
    b_ = (3 * iv.sqrt(5) - iv.sqrt(21)) / 12
    if swap:
        a_, b_ = b_, a_

    def lap(edges):
        L = [[pt(0)] * 6 for _ in range(6)]
        for (u, v), cc in edges:
            L[u][u] += cc
            L[v][v] += cc
            L[u][v] -= cc
            L[v][u] -= cc
        return [row[1:] for row in L[1:]]
    tri = lambda o: [((o, o + 1), a_), ((o + 1, o + 2), a_), ((o, o + 2), b_)]
    ver = lambda o: [((o, o + 1), pt(1)), ((o + 1, o + 2), pt(1))]
    hor = [((r, 3 + r), pt(1)) for r in range(3)]
    tD, tmix, tfree = det_iv(lap(tri(0) + tri(3) + hor)), det_iv(lap(tri(0) + ver(3) + hor)), det_iv(lap(ver(0) + ver(3) + hor))
    return finite((iv.sqrt(tD * tfree) / tmix) ** (N - 1), 'r_main')


def c_harm(INP, fails, fires):
    """C-HARM (v1_1 sect. 4): r_main by the matrix-tree theorem in mp.iv (r_main_iv, which q uses since v2_2) against endw's stored
    value, and q^2(t = 0) = r_main, to 1e-10, with vacmod2's closed forms source-checked; PLANT-HARM (v2_2): the two conductances
    swapped must fail the comparison."""
    vm2 = open(os.path.join(SCR, 'vacmod2.py')).read().split('\n')
    okf = (vm2[7].strip() == 'A_EX = (3 + math.sqrt(21)) / 6' and vm2[8].strip() == 'B_EX = (3 * math.sqrt(5) - math.sqrt(21)) / 12')
    for N in (4, 3):
        inp = INP[N]
        r_iv = r_main_iv(N)
        r_st = inp['EW']['r_main']
        d1 = float(abs(r_iv - r_st).b) / r_st
        a0 = lambda d: d['ak'][0]
        q0 = a0(inp['EW']['items']['I_mix']) ** 2 * r_st / (a0(inp['M2']['items']['g00']) * a0(inp['EW']['items']['I_free']))
        d2 = abs(q0 - r_st) / r_st
        ok = okf and d1 <= 1e-10 and d2 <= 1e-10
        out('C-HARM N=%d: r_main by matrix-tree %s vs stored %.12f (relative %.1e); q^2(t=0) %.12f (relative %.1e); vacmod2 closed forms %s '
            '-> %s' % (N, nf(r_iv, 13), r_st, d1, q0, d2, 'match' if okf else 'DIFFER', 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-HARM N=%d' % N)
        d3 = float(abs(r_main_iv(N, swap=True) - r_st).b) / r_st
        out('PLANT-HARM N=%d (v2_2: the conductances A_EX and B_EX swapped in the matrix-tree value): relative %.1e against the stored '
            'r_main -> %s' % (N, d3, 'FIRES' if d3 > 1e-10 else 'DOES NOT FIRE'))
        if not d3 > 1e-10:
            fires.append('PLANT-HARM N=%d' % N)
        it = inp['M2']['items']
        out('INFO-HARM N=%d: trial R+ at t = 0, I3p_0/N_w_0 = %.5f (harmonic 0.61 x 0.146 + 0.39 x 0.044 = %.4f)' % (
            N, it['I3p']['ak'][0] / it['Nw']['ak'][0], 0.61 * 0.146 + 0.39 * 0.044))


def c_ip3(INP, fails):
    """C-IP3 (v1_1 sect. 4): I_p3 = m-hat N_w (the eigen trick) at a_0, a_1 and a_2, to 1e-12 max(1, |a|); INFO a_3, J = 170."""
    for N in (4, 3):
        inp = INP[N]
        it, ms = inp['M2']['items'], inp['mser']
        mh = [1.0, ms['m1'], ms['m2'], ms['m3']]
        ip, nw = it['Ip3']['ak'], it['Nw']['ak']
        mn = [sum(mh[i] * nw[k - i] for i in range(k + 1)) for k in range(4)]
        dk = [ip[k] - mn[k] for k in range(4)]
        ok = all(abs(dk[k]) <= 1e-12 * max(1.0, abs(ip[k])) for k in (0, 1, 2))
        tt = 1.0 / 170
        dv = sum(ip[k] * tt ** k for k in range(4)) - sum(mn[k] * tt ** k for k in range(4))
        out('C-IP3 N=%d: I_p3 - m-hat N_w a_0 %.2e, a_1 %.2e, a_2 %.2e (tolerance 1e-12) -> %s; INFO a_3 %.3e; at J = 170 %.3e' % (
            N, dk[0], dk[1], dk[2], 'PASS' if ok else 'FAIL', dk[3], dv))
        if not ok:
            fails.append('C-IP3 N=%d' % N)


def c_kbar(INP, fails, fires):
    """C-KBAR (v2_2 (2), the argument is in FREEZE_NOTE_kt_s67_cert_v2_2 sect. 2). k-bar is a free centering constant
    of the construction, not an input to certify: v+ = Q0 T_{xi+ - kbar} u / lam0 for every constant kbar (PK10_NOTES 19.5.1). The
    bounds that use it hold for every kbar >= 0: B_op = max(beta, kbar (1 + eps_r)) rests on -kbar T <= T_w~, that is kbar >= 0
    (19.5.4); the mismatch between kbar and the exact centering enters S6 through u_h's |k_n - kbar g00| / g00, and S7 through E_w in
    t1 = (kbar + E_w)(1 + eps_r), since the exact bulk mean is kbar + <u, T_w~ u> / lam0 (19.6.2-3); both carry the entries' bars. So
    it needs kbar >= 0 and the same kbar as m2's w~ integrals N_w, I3p, I_p3 and A_0w, which come from the same m2 file. Gate: kbar >= 0
    exactly, and on [300, 303] u_h >= its centering term and t1 >= kbar (1 + eps_r). PLANT-KBAR: kbar negated must fail the sign gate."""
    for N in (4, 3):
        inp = INP[N]
        kb = pt(inp['M2']['kbar'])
        cx = Ctx(inp, 300.0, 303.0, {})
        g00, kn = cx.entry('M2', 'g00'), cx.entry('M2', 'kn')
        mm = abs(kn - kb * g00) / g00
        Q = piece_eval(inp, 300.0, 303.0, {})['Q']
        sign_ok = (kb >= 0) is True
        cover_u = (Q['uh'].b >= mm.b) is True
        cover_t = (Q['t1'] >= kb * (1 + Q['er'])) is True
        ok = sign_ok and cover_u and cover_t
        fired = not ((pt(-inp['M2']['kbar']) >= 0) is True)
        out('C-KBAR N=%d (v2_2: k-bar a free centering constant): kbar = %r, m2\'s own (pk10/scratch/m2_N%d_J170.json.b, the constant its '
            'N_w, I3p, I_p3 and A_0w integrate w~ = xi+ - kbar with); kbar >= 0: %s; on [300, 303] the S6 centering term |k_n - kbar g00|/g00 '
            '<= %s lies inside u_h <= %s: %s; S7: E_w <= %s and t1 = (kbar + E_w)(1 + eps_r) <= %s, >= kbar (1 + eps_r): %s -> %s; '
            'PLANT-KBAR (kbar negated) must fail the sign gate -> %s' % (
                N, inp['M2']['kbar'], N, sign_ok, nf(mm.b, 6), nf(Q['uh'].b, 6), cover_u, nf(Q['Ew'], 6), nf(Q['t1'], 6), cover_t,
                'PASS' if ok else 'FAIL', 'FIRES' if fired else 'DOES NOT FIRE'))
        if not ok:
            fails.append('C-KBAR N=%d' % N)
        if not fired:
            fires.append('PLANT-KBAR N=%d' % N)


def c_guards(INP, fails, fires):
    """C-PARITY (INFO while M3's tag is FLOAT, a gate once it is certified; its control and plant gate), C-MODULE and C-TAG, with
    their plants."""
    px03 = tag_certified('M3 entries', TAGS['M3 entries'])
    for N in (4, 3):
        pmx = parity_max(INP[N]['B5'])
        sym = json.loads(json.dumps(INP[N]['B5']))
        for k in PARITY_KEYS:
            sym['items'][k]['ak'] = [0.0] * len(sym['items'][k]['ak'])
        ok_sym = parity_max(sym) == 0.0
        pl = json.loads(json.dumps(sym))
        pl['items'][PARITY_KEYS[0]]['ak'][0] = 1e-12                      # S2: one explicit cross-parity coefficient in the copy
        fired = parity_max(pl) != 0.0
        out('C-PARITY N=%d: cross-parity Gram entries %s: stored coefficients max |a_k| = %.2e (%s); control, a symmetrized copy -> %s; '
            'PLANT-PARITY, that copy with %s a_0 = 1e-12 -> %s' % (
                N, ', '.join(PARITY_KEYS), pmx, 'a gate, M3\'s tag is certified' if px03 else 'INFO while M3\'s tag is FLOAT: today\'s '
                'files are unsymmetrized; the certified item gates exact zeros in M3\'s files', 'PASS' if ok_sym else 'FAIL', PARITY_KEYS[0],
                'FIRES' if fired else 'DOES NOT FIRE'))
        if px03 and pmx != 0.0:
            fails.append('C-PARITY N=%d' % N)
        if not ok_sym:
            fails.append('C-PARITY control N=%d' % N)
        if not fired:
            fires.append('PLANT-PARITY N=%d' % N)
    srcs = {n: inspect.getsource(globals()[n]) for n in VERDICT_FUNCS}
    hits = module_scan(srcs)
    out('C-MODULE: %d verdict-path functions and classes against %d forbidden patterns: %s -> %s' % (
        len(srcs), len(FORBIDDEN), 'none' if not hits else '; '.join('%s: %s' % h for h in hits), 'PASS' if not hits else 'FAIL'))
    if hits:
        fails.append('C-MODULE')
    qs = srcs['quantities']
    planted = qs.replace('iv.sqrt(1 - s * s)', 'math.sqrt(1 - s * s)', 1)
    fired = planted != qs and bool(module_scan({'quantities, planted': planted}))
    out('PLANT-MODULE: a libm sqrt planted in quantities -> %s' % ('FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-MODULE')
    ctl = {k: ('ctl%d' % i, '%08x' % (0x5eed0000 + i)) for i, k in enumerate(sorted(TAGS))}      # control pins, one per input
    cert = {k: 'CERTIFIED %s %s' % ctl[k] for k in TAGS}
    full = all(k in TAG_PINS for k in TAGS)                             # N-a (v2_1): every input has a provider and a pin
    ok = (verdict_word(cert, True, ctl) == 'CERTIFIED' and verdict_word(cert, False, ctl) == 'FAIL'
          and verdict_word({**cert, 'M3 entries': 'FLOAT (control)'}, True, ctl) == 'FLOAT-PASS'
          and verdict_word(TAGS, True) == ('CERTIFIED' if full else 'FLOAT-PASS'))
    wrong = ctl['S4 U'][1][:7] + ('1' if ctl['S4 U'][1][7] == '0' else '0')
    cases = (('FLOAT tags', {k: 'FLOAT (plant)' for k in TAGS}),
             ('S4 TRB = "S4-TRB, pending"', {**cert, 'S4 TRB': 'S4-TRB, pending'}),
             ('S4 U = CERTIFIED with a wrong sha8', {**cert, 'S4 U': 'CERTIFIED %s %s' % (ctl['S4 U'][0], wrong)}))
    res = [(lab, verdict_word(tg, True, ctl)) for lab, tg in cases]
    out('C-TAG: wording control (control pins: all certified -> CERTIFIED, a failed verdict -> FAIL, one FLOAT tag -> FLOAT-PASS; this '
        'run\'s tags -> CERTIFIED exactly when every input has a pin, here %s: %s) -> %s; PLANT-TAG (F1), each with every other tag '
        'certified, must not read CERTIFIED: %s' % (
            'CERTIFIED' if full else 'FLOAT-PASS', 'every input has a pin' if full else 'no pin for %s' % ', '.join(
                sorted(k for k in TAGS if k not in TAG_PINS)),
            'PASS' if ok else 'FAIL', '; '.join('%s -> %s -> %s' % (lab, w, 'FIRES' if w != 'CERTIFIED' else 'DOES NOT FIRE')
                                                for lab, w in res)))
    if not ok:
        fails.append('C-TAG')
    for i, (lab, w) in enumerate(res):
        if w == 'CERTIFIED':
            fires.append('PLANT-TAG case %d (%s)' % (i + 1, lab))


def c_fmt(INP, NSB, fails, fires):
    """C-FMT (S2), FLOAT form: the port's reader (Ctx.entry, naive, over [300, 303]) against the author's reader (assemble_binding_unif4's
    item(), the convention m2_unif3 and endpairs4 share) on every stored entry of every file. PLANT-FMT: the port reading a copy with two
    entries' coefficient lists swapped must fail."""
    def worst_diff(inp_port, inp_prod, item):
        cx = Ctx(inp_port, 300.0, 303.0, {})
        w, wk, n = 0.0, '', 0
        for src, name in entry_names(inp_prod):
            a = item(name, {'I_N': inp_prod['B4']['I_N']} if src == 'B4' else inp_prod[src]['items'], cx.tI)
            b = cx.entry(src, name, 'naive')
            r_ = float((abs(a.a - b.a) + abs(a.b - b.b)).b) / max(1.0, abs(fnum(a)))
            n += 1
            if r_ > w:
                w, wk = r_, '%s %s' % (src, name)
        return w, wk, n
    for N in (4, 3):
        w, wk, n = worst_diff(INP[N], INP[N], NSB[N]['item'])
        ok = w <= 1e-15
        out('C-FMT N=%d: %d stored entries, the port\'s reader against the author\'s item() over [300, 303]: worst difference %.1e (%s) -> %s' % (
            N, n, w, wk or 'none', 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-FMT N=%d' % N)
        sw = json.loads(json.dumps({k: v for k, v in INP[N].items() if k not in ('U5', 'TRBv', 'r_iv')}))   # mp.iv values left out
        it_ = sw['B5']['items']
        it_['g,0,1']['ak'], it_['g,1,1']['ak'] = it_['g,1,1']['ak'], it_['g,0,1']['ak']
        w, wk, _ = worst_diff(sw, INP[N], NSB[N]['item'])
        fired = w > 1e-15
        out('PLANT-FMT N=%d (the port reads a copy with the g,0,1 and g,1,1 coefficient lists swapped): worst difference %.1e (%s) -> %s' % (
            N, w, wk, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-FMT N=%d' % N)


TGT = dict(err=1.186, U=7.8e-4, TRB=1.02)     # SPEC v1_2 sect. 3, the set T2: errors = bars, vacuum, eps_w. "float U" is today's
                                              # U = lead(1 + c1 t + c2 t^2 + c3 t^3) + rem(170), and T2 raises it, rem included, by +7.8e-4
TGT_DEC = dict(U='7.8e-4', QUAD='3.9e-4', TRB='1.02')    # the same targets as exact decimals, for KR3 and KR4; S4U_HEADER pins the
                                                          # record's copies of the first two, S4T_HEADER the TRB target's decimals


def certified_inputs():
    """the inputs whose tags read certified (F1)."""
    return {k for k, v in TAGS.items() if tag_certified(k, v)}


def tgt_hooks(lam, cert=()):
    """every input at lambda times its target excess (lambda = 1: the v1_2 targets). A certified input enters with its certified value
    instead of its target (SPEC sect. 4): S4 U drops U_add, S4 TRB drops TRB, M3 drops bar_all, M2 drops vac_all and eps_w."""
    x = 1 + lam * (TGT['err'] - 1)
    h = {}
    if 'M3 entries' not in cert:
        h['bar_all'] = x
    if 'M2 vacuum' not in cert:
        h.update(vac_all=x, eps_w=x)
    if 'S4 U' not in cert:
        h['U_add'] = lam * TGT['U']
    if 'S4 TRB' not in cert:
        h['TRB'] = 1 + lam * (TGT['TRB'] - 1)
    return h


def tgt_text(lam, cert):
    """the C-TARGETS line's statement of the inputs at lambda."""
    x, s = 1 + lam * (TGT['err'] - 1), []
    s.append('bars %s' % ('certified (M3)' if 'M3 entries' in cert else 'x%.4g' % x))
    s.append('vacuum and eps_w %s' % ('certified (M2)' if 'M2 vacuum' in cert else 'x%.4g' % x))
    s.append('U %s' % ('certified (S4-U, U3(t) + R_CERT, no target added)' if 'S4 U' in cert else
                       '+ %.3g on today\'s U, rem(170) included' % (lam * TGT['U'])))
    s.append('TRB %s' % ('certified (S4-TRB)' if 'S4 TRB' in cert else 'x%.4g' % (1 + lam * (TGT['TRB'] - 1))))
    return ', '.join(s)


def tgt_piece(inp, Jlo, Jhi, sc, use_centered):
    """S5, S6 and S7 with the Lemma S7-mono hypotheses and lambda_1^e simple on one piece: (verdict, c5, R+/rho lower end)."""
    try:
        E = piece_eval(inp, Jlo, Jhi, sc, use_centered=use_centered)
        c5, r6 = E['S5']['c5'], (E['Q']['Rp'] / E['Q']['rho']).a
        hold = ((c5 > 0) is True and (r6 > 1) is True and E['Mq']['simple']
                and all(claim_holds(E['cv'], p) and s7mono_hyp(E['Q'], E['Mq'], p[1], E['cv'][p][1], sc) for p in CLAIM[inp['N']]))
        return hold, c5, r6
    except (ValueError, ZeroDivisionError, ArithmeticError):
        return False, None, None


def c_targets(INP):
    """C-TARGETS (F1): every input at its v1_2 target at once (lambda = 1), then at lambda = 1.25, on every piece of the grid, S5, S6 and
    S7 at both N, with the naive enclosures; a piece that fails naive is re-evaluated with the production forms (centered), and
    the production result decides. Returns {(lam, N): (all hold in production form, worst c5 (value, piece), worst R+/rho, pieces failing
    naive, pieces failing in production form)}. Certified inputs enter with their certified values (tgt_hooks; F2: S4-U)."""
    res = {}
    cert = certified_inputs()
    for lam in (1.0, 1.25):
        sc = tgt_hooks(lam, cert)
        for N in (4, 3):
            STAGE[0] = 'C-TARGETS lambda=%.2f N=%d' % (lam, N)
            w5, w6, badn, badp = None, None, [], []
            for (Jlo, Jhi) in pieces():
                budget(1.0, STAGE[0])
                hold, c5, r6 = tgt_piece(INP[N], Jlo, Jhi, sc, False)
                if not hold:
                    badn.append(Jlo)
                    hold, c5p, r6p = tgt_piece(INP[N], Jlo, Jhi, sc, True)
                    c5, r6 = (c5p, r6p) if c5p is not None else (c5, r6)
                    if not hold:
                        badp.append(Jlo)
                if c5 is not None and (w5 is None or (c5 < w5[0]) is True):
                    w5 = (c5, Jlo, Jhi)
                if r6 is not None and (w6 is None or (r6 < w6[0]) is True):
                    w6 = (r6, Jlo, Jhi)
            res[(lam, N)] = (not badp, w5, w6, badn, badp)
    return res


# ------------------------------------------------------------------ item sweep: every piece of [300, inf), both N
def item_sweep(INP, NSM, NSE, NSB, fails, fires):
    PCS = pieces()
    res = {}
    for N in (4, 3):
        STAGE[0] = 'sweep N=%d' % N
        inp = INP[N]
        R = dict(n=0, w5=None, w6=None, holds=True, simple=True, mono=True, mvbad=0, mvkeys=set(), ofb=0, cov={}, rep=(0.0, ''), viol=[],
                 covsame=True, nrep=0)
        for i, (Jlo, Jhi) in enumerate(PCS):
            budget(1.0, 'sweep N=%d piece %d' % (N, i))
            E = piece_eval(inp, Jlo, Jhi, {})
            Q, Mq, S5, cv = E['Q'], E['Mq'], E['S5'], E['cv']
            EXPORT_ROWS[N].append(export_row(Jlo, Jhi, N, E))                 # v2_2 (3): the piece's export line
            r6 = (Q['Rp'] / Q['rho']).a
            if R['w6'] is None or (r6 < R['w6'][0]) is True:
                R['w6'] = (r6, Jlo, Jhi)
            if R['w5'] is None or (S5['c5'] < R['w5'][0]) is True:
                R['w5'] = (S5['c5'], Jlo, Jhi)
            for p in CLAIM[N]:
                mj, km = R['cov'].get(p, (MMAX, 0))
                R['cov'][p] = (min(mj, cv[p][0]), max(km, cv[p][1]))
                R['holds'] = R['holds'] and claim_holds(cv, p)
                R['mono'] = R['mono'] and s7mono_hyp(Q, Mq, p[1], cv[p][1], {})
            R['simple'] = R['simple'] and Mq['simple']
            R['ofb'] += 0 if Q['order_ok'] else 1
            R['kink'] = R.get('kink', 0) + E['cx'].cache.get('fallbacks', 0)
            bad = mv_check(E['cx'], E['Ub'])
            if bad:
                R['mvbad'] += 1
                R['mvkeys'].update(bad)
            if i % 100 == 0 or Jhi is None:
                out('  sweep N=%d: piece %d [%s] at cpu %.1f s' % (N, i, piece_str(Jlo, Jhi), cpu()))
                w, wk, viol, cs = repro_compare(inp, NSM[N], NSE[N], NSB[N], Jlo, Jhi)
                R['nrep'] += 1
                if w > R['rep'][0]:
                    R['rep'] = (w, '%s at J = %.1f' % (wk, Jlo))
                R['viol'] += ['%s at J = %.1f' % (v, Jlo) for v in viol]
                R['covsame'] = R['covsame'] and cs
            R['n'] += 1
        R['last_rho'] = E['Q']['rho']
        res[N] = R
        ok5 = (R['w5'][0] > 0) is True
        ok6 = (R['w6'][0] > 1) is True and ok5
        ok7 = R['holds'] and R['simple'] and R['mono'] and R['mvbad'] == 0
        out('S5 N=%d: c5 = min over %d pieces of [even_lo - odd_up - vacT_up] = %s on [%s] -> %s' % (
            N, R['n'], nf(R['w5'][0]), piece_str(R['w5'][1], R['w5'][2]), verdict_word(TAGS, ok5)))        # F1: the tags decide
        out('S6 N=%d: min R+/rho (lower end) %s on [%s]; sign condition c5 > 0 (S5) %s -> %s' % (
            N, nf(R['w6'][0]), piece_str(R['w6'][1], R['w6'][2]), ok5, verdict_word(TAGS, ok6)))
        out('S7 N=%d: claimed coverage %s on every piece %s (worst over pieces: %s); lambda_1^e simple on all pieces %s; Lemma S7-mono (a) '
            'hypotheses %s; C-MV clean %s -> %s' % (
                N, ', '.join('%s d>=%d' % p for p in CLAIM[N]), 'HOLDS' if R['holds'] else 'FAILS',
                '; '.join('%s d=%d: Jensen checked to m=%d, mode from m=%d' % (p[0], p[1], R['cov'][p][0], R['cov'][p][1] + 1) for p in CLAIM[N]),
                R['simple'], R['mono'], R['mvbad'] == 0, verdict_word(TAGS, ok7)))
        okmv = R['mvbad'] == 0
        out('C-MV N=%d: %d pieces x 4 smooth forms x 9 points: failures on %d pieces (%s) -> %s' % (
            N, R['n'], R['mvbad'], ', '.join(sorted(R['mvkeys'])) or 'none', 'PASS' if okmv else 'FAIL'))
        if not okmv:
            fails.append('C-MV N=%d' % N)
        out('INFO C-ORDER N=%d: the L1 centered form fell back to the naive bound (minimizing row or positivity not certified) on %d of %d '
            'pieces; centered forms that met a kink or a non-finite D(P) and kept the naive bound: %d' % (N, R['ofb'], R['n'], R.get('kink', 0)))
        out('INFO-HARM N=%d: rho on the last piece [%s] %s (harmonic odd 2-phonon lambda_z/lambda_0 = 0.0797)' % (
            N, piece_str(*PCS[-1]), nf(R['last_rho'])))
        okr = R['rep'][0] <= TOL_B and not R['viol'] and R['covsame']
        out('C-REPRO300 N=%d: path A on %d sampled pieces: worst relative B-A %.2e (%s); production forms never better than A: %s; claimed-pair '
            'coverage %s -> %s' % (N, R['nrep'], R['rep'][0], R['rep'][1], 'yes' if not R['viol'] else 'NO (%s)' % ', '.join(R['viol'][:6]),
                                   'identical' if R['covsame'] else 'DIFFERS', 'PASS' if okr else 'FAIL'))
        if not okr:
            fails.append('C-REPRO300 N=%d' % N)
        for (Jlo, Jhi) in (PCS[0], PCS[-1]):
            E = piece_eval(inp, Jlo, Jhi, {}, full=True)
            Q, Mq, S5 = E['Q'], E['Mq'], E['S5']
            g6 = nf
            out('INFO N=%d [%s]: c5 %s (even %s, odd %s, vacT %s); R+ %s, rho %s, rho1 %s, R_w %s, |v+| %s, |v-| %s, ||B+|| %s, ||B-|| %s; '
                'q_x %s, L2 %s, mu_x %s, alpha^2 %s, |a_x| %s, c_x %s, r2 %s, ro %s; full coverage: %s' % (
                    N, piece_str(Jlo, Jhi), g6(S5['c5']), g6(S5['even'].a), g6(S5['odd'].b), g6(S5['vacT'].b), g6(Q['Rp']), g6(Q['rho']),
                    g6(Q['rho1']), g6(Q['Rw']), g6(Q['vp']), g6(Q['vm']), g6(Q['nBp']), g6(Q['nBm']), g6(Mq['qx']), g6(Mq['L2']), g6(Mq['mux']),
                    g6(Mq['al2']), g6(Mq['ax']), g6(Mq['cx']), g6(Mq['r2']), g6(Mq['ro']),
                    '; '.join('%s d=%d: Jensen m<=%d, mode m>=%d' % (p[0], p[1], E['cv'][p][0], E['cv'][p][1] + 1) for p in CLAIM[N])))

    STAGE[0] = 'C-PIECE, C-UNIF'
    for N in (4, 3):
        R = res[N]
        binding = []
        for pc in (PCS[0], (R['w5'][1], R['w5'][2]), (R['w6'][1], R['w6'][2]), PCS[-1]):
            if pc not in binding:
                binding.append(pc)
        tbad, wn, ubad, mbad = [], (-1.0, ''), [], []
        for (Jlo, Jhi) in binding:
            budget(5.0, 'C-PIECE, C-UNIF, C-MV-B N=%d' % N)
            b_, w, k = piece_check(INP[N], Jlo, Jhi)
            tbad += ['%s on [%s]' % (x, piece_str(Jlo, Jhi)) for x in b_]
            if w > wn[0]:
                wn = (w, '%s on [%s]' % (k, piece_str(Jlo, Jhi)))
            ubad += ['%s on [%s]' % (x, piece_str(Jlo, Jhi)) for x in unif_check(Ctx(INP[N], Jlo, Jhi, {}))]
            E = piece_eval(INP[N], Jlo, Jhi, {})
            mbad += ['%s on [%s]' % (x, piece_str(Jlo, Jhi)) for x in mvb_check(E['cx'], E['Ub'], E['V'])]
        ok = not tbad and wn[0] <= 1e-15
        out('C-PIECE N=%d: %d binding pieces halved, naive enclosures (the piece\'s preconditioner, vacuum point and index order): terms '
            'outside the parent %d%s; parent against its end and midpoint values included; largest outward move of a final bound %.2e (%s) '
            '-> %s' % (N, len(binding), len(tbad), (' (%s)' % ', '.join(tbad[:4])) if tbad else '', wn[0], wn[1], 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-PIECE N=%d' % N)
        out('C-UNIF N=%d: the same pieces, every stored entry, U and m-hat against 9 points each -> %s' % (
            N, 'PASS' if not ubad else 'FAIL (%s)' % ', '.join(ubad[:6])))
        if ubad:
            fails.append('C-UNIF N=%d' % N)
        out('C-MV-B N=%d: the same pieces, 4 smooth forms at 9 points, delta = 0 and the two gradient-sign corners of B -> %s' % (
            N, 'PASS' if not mbad else 'FAIL (%s)' % ', '.join(mbad[:6])))
        if mbad:
            fails.append('C-MV-B N=%d' % N)

    STAGE[0] = 'PLANT-RIGHTEND, PLANT-MV, PLANT-MVB'
    Jlo, Jhi = PCS[0]
    bad = unif_check(Ctx(INP[4], Jlo, Jhi, {'right_end': True}))
    tb, _, _ = piece_check(INP[4], Jlo, Jhi, {'right_end': True})
    fired = bool(bad) and bool(tb)
    out('PLANT-RIGHTEND (N=4, [%s]): the piece\'s t replaced by its right end in J -> C-UNIF fails on %d names, C-PIECE on %d terms -> %s' % (
        piece_str(Jlo, Jhi), len(bad), len(tb), 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-RIGHTEND')
    E = piece_eval(INP[4], Jlo, Jhi, {})
    bad = mv_check(E['cx'], E['Ub'], zero_derivative=True)
    out('PLANT-MV (N=4, [%s]): D_c(P) replaced by 0 -> C-MV fails on %s -> %s' % (
        piece_str(Jlo, Jhi), ', '.join(bad) if bad else 'nothing', 'FIRES' if bad else 'DOES NOT FIRE'))
    if not bad:
        fires.append('PLANT-MV')
    bad = mvb_check(E['cx'], E['Ub'], E['V'], bar_free=True)
    fired = 'S5 Dd' in bad                                  # N-b: judged on S5 Dd, where the bars enter at full weight
    out('PLANT-MVB (N=4, [%s]): F(t_m) evaluated with B = 0 -> C-MV-B fails on %s; S5 Dd among them: %s -> %s' % (
        piece_str(Jlo, Jhi), ', '.join(bad) if bad else 'nothing', fired, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-MVB')

    STAGE[0] = 'KILL (sweep part)'
    kr1 = all((res[N]['w6'][0] >= 1.05) is True for N in (4, 3))
    out('KILL KR1 (S6 R+/rho >= 1.05 on every piece): N=4 %s, N=3 %s -> %s' % (
        nf(res[4]['w6'][0]), nf(res[3]['w6'][0]), 'PASS' if kr1 else 'KILL'))
    kr3, kr4 = s4_kr34(INP, fails)              # F2, D-2: KR3 and KR4 are gates in this item too (its U and TRB are the certified ones)
    STAGE[0] = 'KILL (sweep part)'
    kr5a = all((res[N]['w5'][0] > 0) is True for N in (4, 3))
    out('KILL KR5a, sweep part (c5 > 0 on every piece): N=4 %s, N=3 %s -> %s (the joint-headroom part is in the scan item)' % (
        nf(res[4]['w5'][0]), nf(res[3]['w5'][0]), 'PASS' if kr5a else 'KILL'))
    tg = {N: pt(INP[N]['P']['cov1']) / 1.51 for N in (4, 3)}
    kr5b = all((res[N]['w5'][0] >= tg[N]) is True for N in (4, 3))
    out('KILL KR5b (c5 >= v1_1\'s S5 target Cov_1/1.51 = %s at N=4, %s at N=3) -> %s' % (
        nf(tg[4], 4), nf(tg[3], 4), 'PASS' if kr5b else 'FAIL: nothing claimed for S7 until it is re-run with C_1 = c5'))
    out('KILL RULE, sweep part: %s' % ('no kill (KR1, KR3, KR4, KR5a part, KR5b pass)' if (kr1 and kr3 and kr4 and kr5a and kr5b)
                                       else 'KILL: stop and report'))


# ------------------------------------------------------------------ item scan: plants at [300, 303], distances to flip, targets
def item_scan(INP, fails, fires):
    J3, J3h = 300.0, 303.0                      # S1: E6's fixed plants (U + 1.3e-3, R_w x 1.30, TRB x 1.50) give way to margin_plant
    STAGE[0] = 'SCAN [300, 303]'
    scan = {}
    for N in (4, 3):
        for lab, mk, kind, cap, lane, app in GROUPS:
            for which in app.split():
                budget(4.0, 'SCAN N=%d %s %s' % (N, which, lab))
                scan[(N, which, lab)] = flip_search(lambda x: verdict_one(INP[N], J3, J3h, mk(x), which), kind, cap)
    for lab, mk, kind, cap, lane, app in GROUPS:
        out('SCAN [300, 303] %-36s part %-3s: %s' % (lab, lane, '; '.join(
            '%s N%d %s' % (w, N, fmt_f(scan[(N, w, lab)])) for N in (4, 3) for w in app.split())))
    out('INFO SCAN base: these distances, here and on the last piece, are measured from the certified S4 values: '
        '\'Lemma 19.4 rem\' and the joint group scale R_CERT (not rem(170)), \'U raised by (absolute)\' adds to the certified U(t), '
        '\'TRB (beta)\' scales the certified TRB; the M3 and M2 inputs are FLOAT. They read as headroom over the certified values.')
    STAGE[0] = 'SCAN last piece'
    PL = pieces()[-1]
    scanL = {}
    for N in (4, 3):
        for lab, which in LAST_GROUPS:
            budget(4.0, 'SCAN last N=%d %s %s' % (N, which, lab))
            _, mk, kind, cap, _, _ = GMAP[lab]
            scanL[(N, which, lab)] = flip_search(lambda x: verdict_one(INP[N], PL[0], PL[1], mk(x), which), kind, cap)
    out('SCAN last piece [%s]: %s' % (piece_str(*PL), '; '.join(
        '%s %s N%d %s' % (lab, w, N, fmt_f(scanL[(N, w, lab)])) for lab, w in LAST_GROUPS for N in (4, 3))))

    STAGE[0] = 'margin plants (S1, D2)'
    out('INFO margin plants (S1, D2): F is the scan\'s flip on [300, 303]: bracket [1, 2] doubled up to %g (factors) or [0, 1e-4] '
        'doubled up to 1.0 (U, additive), then bisection to relative 0.4%% (hi/lo <= 1.004, or hi - lo <= 0.004 hi); each plant needs a '
        'hold at F / 1.1 and a loss at 1.1 F' % MCAP)
    for N in (4, 3):                                            # S1: E6's margins, self-calibrating, on the scan's binding piece per N
        for lab, key in (('U raised by (absolute)', 'U'), ('R_w', 'RW'), ('TRB (beta)', 'TRB')):
            budget(2.0, 'PLANT-%s N=%d' % (key, N))
            F = scan[(N, 'S7', lab)]
            fired = margin_plant(INP[N], J3, J3h, GMAP[lab][1], F, 'S7')
            out('PLANT-%s N=%d ([300, 303], S7 claimed coverage, %s): flip F = %s; holds at F / 1.1 and is lost at 1.1 F -> %s' % (
                key, N, lab, fmt_f(F), 'FIRES' if fired else 'DOES NOT FIRE'))
            if not fired:
                fires.append('PLANT-%s N=%d' % (key, N))
    d3 = ('flip', 3)                                            # D2: the d = 3 binding direction at N = 4
    for lab, key in (('C_1 = c5 (divided by)', 'C1'), ('19.1c bars, all', 'BARS')):
        budget(2.0, 'PLANT-D3-%s' % key)
        F = scan[(4, 'S7', lab)]
        fired = d3 in CLAIM[4] and margin_plant(INP[4], J3, J3h, GMAP[lab][1], F, 'S7', lose=(d3,))
        out('PLANT-D3-%s (N=4, [300, 303], %s): flip F = %s of the claim %s; the claim holds at F / 1.1 and the pair flip d=3 is lost at '
            '1.1 F -> %s' % (key, lab, fmt_f(F), ', '.join('%s d>=%d' % p for p in CLAIM[4]), 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-D3-%s' % key)

    STAGE[0] = 'ADD1 plants'
    for N in (4, 3):
        for lab, key in (('19.1c bar N_delta', 'bar_Ndel'), ('TRB (beta)', 'TRB')):
            F = scan[(N, 'S5', lab)]
            fired = margin_plant(INP[N], J3, J3h, GMAP[lab][1], F, 'S5')       # shared with S1 (a missing flip does not fire)
            out('PLANT-S5 %s N=%d ([300, 303]): S5 holds at %s / 1.1 and fails at x 1.1 -> %s' % (
                key, N, fmt_f(F), 'FIRES' if fired else 'DOES NOT FIRE'))
            if not fired:
                fires.append('PLANT-S5 %s N=%d' % (key, N))

    STAGE[0] = 'C-FLIP170'
    J0, J0h = 170.0, 170.0 * 1.01
    for N in (4, 3):                                            # D1: the own claim and C_1 = Cov_1, path A's FLOAT U and TRB
        inf_ = float_s4(INP[N])
        okall, n_ = True, 0
        for fname, which in (('pk20/rv13/c5/rc_m2_sens_N%d.txt' % N, 'S6'), ('pk20/rv13/c6/rc_end_sens_N%d.txt' % N, 'S7')):
            txt = open(os.path.join(CODEDIR, fname)).read()
            if which == 'S6':
                rows = re.findall(r'^(.+?) +flips at (> )?([0-9.e+-]+)\s*$', txt, re.M)
            else:
                rows = [(lab.strip(), '', v) for lab, v in re.findall(
                    r'^  ((?:R_w|\|\|B\+\|\|, \|\|B-\|\||c_x|Cov_1) [x/]|U raised by) +([0-9.e+-]+)', txt, re.M)]
            for lab, gt, val in rows:
                lab = lab.strip()
                if lab not in REVMAP:
                    okall = False
                    out('  C-FLIP170 N=%d: unmapped label %r' % (N, lab))
                    continue
                budget(4.0, 'C-FLIP170 N=%d %s' % (N, lab))
                mk, kind, cap = REVMAP[lab]
                f = flip_search(lambda x: verdict_one(inf_, J0, J0h, dict(mk(x), author_forms=True, C1_const=True), which,
                                                      claim=FLIP170_CLAIM[N]), kind, cap)
                v = float(val)
                ok = (f is None or f > v) if gt else (f is not None and abs(f / v - 1) <= 0.01)
                okall = okall and ok
                n_ += 1
                out('  C-FLIP170 N=%d %s %-45s reference %s%s, mine %s -> %s' % (N, which, lab, gt, val, fmt_f(f), 'ok' if ok else 'DIFFERS'))
        out('C-FLIP170 N=%d (the claim %s, C_1 = Cov_1): %d distances to flip against the reference values -> %s' % (
            N, ', '.join('%s d>=%d' % p for p in FLIP170_CLAIM[N]), n_, 'PASS' if okall else 'FAIL'))
        if not okall:
            fails.append('C-FLIP170 N=%d' % N)
    d3txt = open(os.path.join(CODEDIR, D3_REF)).read().split('\n')       # D1, INFO: the d = 3 distances against NOTE1_d3's recorded run
    reg = []
    for lab in ('19.1c bars, all', JOINT, 'C_1 = c5 (divided by)', 'vacuum, all', 'U raised by (absolute)', 'TRB (beta)', 'R_w', '||B+-||',
                'c_x (divided by)'):
        ms = [m for m in (re.fullmatch(r'SCAN \[300, 303\] %s +part [^:]*: (.*)' % re.escape(lab), ln) for ln in d3txt) if m is not None]
        rv = re.search(r'(?:^|; )S7 N4 ([^;]+)', ms[0].group(1)) if len(ms) == 1 else None
        reg.append('%s %s (recorded %s)' % (lab, fmt_f(scan[(4, 'S7', lab)]), rv.group(1) if rv else 'not found'))
    ms = [m for m in (re.search(r'%s S7 N4 ([^;]+)' % re.escape(JOINT), ln) for ln in d3txt if ln.startswith('SCAN last piece')) if m]
    reg.append('last piece %s %s (recorded %s)' % (JOINT, fmt_f(scanL[(4, 'S7', JOINT)]), ms[0].group(1) if len(ms) == 1 else 'not found'))
    out('INFO C-FLIP170 d=3 (D1): S7 N=4 under the production claim %s, distances to flip now, measured from the certified S4 values '
        '(N-d), against NOTE1_d3\'s recorded run (%s, sha8 %s, all inputs FLOAT then; differences from this change of base are expected '
        'and are not a C-FLIP170 failure): %s' % (', '.join('%s d>=%d' % p for p in CLAIM[4]), D3_REF, FILES[D3_REF], '; '.join(reg)))

    STAGE[0] = 'C-TARGETS'
    ct = c_targets(INP)
    cert = certified_inputs()
    for (lam, N), (okt, w5, w6, badn, badp) in sorted(ct.items()):
        out('C-TARGETS lambda=%.2f N=%d (every FLOAT input at lambda x its v1_2 target excess, every certified input at its certified '
            'value: %s; every piece): naive enclosures fail on %d pieces%s; with the production forms there %s; min c5 %s on '
            '[%s], min R+/rho %s on [%s]' % (
                lam, N, tgt_text(lam, cert), len(badn),
                (' (J from %s)' % ', '.join('%.1f' % x for x in badn[:6])) if badn else '',
                'ALL HOLD' if okt else 'FAIL on %d pieces (J from %s)' % (len(badp), ', '.join('%.1f' % x for x in badp[:6])),
                nf(w5[0]) if w5 else 'n/a', piece_str(w5[1], w5[2]) if w5 else '-', nf(w6[0]) if w6 else 'n/a',
                piece_str(w6[1], w6[2]) if w6 else '-'))

    STAGE[0] = 'TARGETS'
    out('TARGETS v1_2 (SPEC sect. 3, the set T2, every input at its target at once): M3 bars, M2 vacuum and P3 eps_w <= x%.3f; S4 U: '
        'certified U - float U <= %.2g (rem included; S4-U from its provider here, see KR4); S4-TRB: certified TRB <= x%.2f (N=4 %.6f, '
        'N=3 %.6f; S4-TRB from its provider here, see KR4); S5: computed here' % (                # N-c (v2_1): "pending" dropped
            TGT['err'], TGT['U'], TGT['TRB'], float(INP[4]['P']['TRB']) * TGT['TRB'], float(INP[3]['P']['TRB']) * TGT['TRB']))

    def fmin(lab):
        v = [x for d_ in (scan, scanL) for (N, w, l_), x in d_.items() if l_ == lab and x is not None]
        return min(v) if v else None
    for lab, mk, kind, cap, lane, app in GROUPS:
        out('INFO headroom (single input, smallest over the scanned verdicts and pieces) %-36s part %-4s: %s' % (lab, lane, fmt_f(fmin(lab))))

    STAGE[0] = 'KILL (scan part)'
    hR, hB = scan[(4, 'S7', 'R_w')], scan[(4, 'S7', '||B+-||')]
    kr2 = (hR is None or hR >= 1.05) and (hB is None or hB >= 1.05)
    out('KILL KR2 (N = 4 headroom in R_w and ||B+-|| >= 1.05 at [300, 303]): %s, %s -> %s' % (fmt_f(hR), fmt_f(hB), 'PASS' if kr2 else 'KILL'))
    kr3, kr4 = s4_kr34(INP, fails)              # F2, D-2: KR3 and KR4 are gates once S4-U (and S4-TRB) are certified
    STAGE[0] = 'KILL (scan part)'
    j5 = {N: scan[(N, 'S5', JOINT)] for N in (4, 3)}
    kr5a = all(v is None or v >= 1.5 for v in j5.values())
    out('KILL KR5a, scan part (S5 joint headroom >= 1.5 at [300, 303]): N=4 %s, N=3 %s -> %s (the c5 > 0 part is in the sweep item)' % (
        fmt_f(j5[4]), fmt_f(j5[3]), 'PASS' if kr5a else 'KILL'))
    krj = all(ct[key][0] for key in ct)
    out('KILL KR-J (C-TARGETS holds at lambda = 1 and 1.25 on every piece, both N): %s' % ('PASS' if krj else 'FAIL: re-split the targets'))
    out('KILL RULE, scan part: %s' % ('no kill (KR2, KR3, KR4, KR5a part, KR-J pass)' if (kr2 and kr3 and kr4 and kr5a and krj)
                                      else 'KILL or FAIL: stop and report'))


# ------------------------------------------------------------------ main
def main():
    fails, fires = [], []
    complete = False
    try:
        STAGE[0] = 'S4-U provider'
        S4 = provide_s4u(fails, fires)          # F1, F2, S3: with provide_s4trb, the only places a tag can become certified
        STAGE[0] = 'S4-TRB provider'
        ST = provide_s4trb(fails, fires)        # v2_1
        INP = {N: load(N, S4, ST) for N in (4, 3)}
        NSM = {N: path_a(INP[N], 'm2u3') for N in (4, 3)}
        NSE = {N: path_a(INP[N], 'ep4') for N in (4, 3)}
        NSB = {N: path_a(INP[N], 'ab4') for N in (4, 3)}
        STAGE[0] = 'C-REPRO at [170, 171.7]'
        c_repro170(INP, NSM, NSE, NSB, fails, fires)
        STAGE[0] = 'C-C2'
        c_c2(INP, fails, fires)
        STAGE[0] = 'C-HARM, C-IP3, C-KBAR'
        c_harm(INP, fails, fires)               # v2_2 (1): with PLANT-HARM
        c_ip3(INP, fails)
        c_kbar(INP, fails, fires)               # v2_2 (2)
        STAGE[0] = 'C-PARITY, C-MODULE, C-TAG'
        c_guards(INP, fails, fires)
        STAGE[0] = 'C-FMT'
        c_fmt(INP, NSB, fails, fires)
        out('controls done at cpu %.1f s' % cpu())
        if MODE == 'sweep':
            item_sweep(INP, NSM, NSE, NSB, fails, fires)
        else:
            item_scan(INP, fails, fires)
        STAGE[0] = 'C-ENV end'
        _env1 = env_probe()
        out('C-ENV end: %s' % ('PASS' if _env1 else 'FAIL'))
        if not _env1:
            fails.append('C-ENV end')
        out('TAGS: %s' % '; '.join('%s = %s (%s)' % (k, v, 'certified' if tag_certified(k, v) else 'not certified')     # F1
                                   for k, v in TAGS.items()))
        complete = True
    except BudgetShort as e:
        out('INCOMPLETE: the CPU budget ran short in stage %s (%s)' % (STAGE[0], e))
    except Exception as e:
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        for ln in traceback.format_exc().splitlines()[-14:]:
            out('TRACE ' + ln)
        out('VERDICT INVALID (ERROR)')
        return 1
    why = fails + ['%s did not fire' % x for x in fires] + ([] if complete else ['INCOMPLETE'])
    if MODE == 'sweep' and complete:                                    # v2_2 (3): the per-piece export for S8, checked before it is written
        STAGE[0] = 'export (v2_2)'
        try:
            text = export_text(why)
            bad, fired = c_export(text)
            out('C-EXPORT: the export text (%d piece lines) read back before writing: the two S4U_KV_v1 readers and the producer\'s reader %s '
                '(sha256 %s) against the rows -> %s; PLANT-EXPORT (N4_P0000\'s c5_lo moved one unit in its last digit) -> %s' % (
                    sum(len(r) for r in EXPORT_ROWS.values()), EXPORT_READER[0], EXPORT_READER[1][:8],
                    'PASS' if not bad else 'FAIL (%s)' % ', '.join(bad[:6]), 'FIRES' if fired else 'DOES NOT FIRE'))
            if bad:
                why.append('C-EXPORT')
            if not fired:
                why.append('PLANT-EXPORT did not fire')
            if not bad and fired:
                path, sh, nl = write_export(text)
                out('EXPORT %s sha256 %s (%d lines; RUN_VERDICT %s, EXPORT_STATUS %s)' % (
                    os.path.relpath(path, CODEDIR), sh, nl, 'VALID' if not why else 'INVALID', verdict_word(TAGS, not why)))
            else:
                out('EXPORT not written (C-EXPORT or its plant failed)')
        except Exception as e:
            out('ERROR in the export at cpu %.1f s: %r' % (cpu(), e))
            why.append('EXPORT ERROR')
    out('ITEM %s cpu %.1f s, peak resident memory %.0f MiB' % (MODE, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
    out('VERDICT %s%s (run validity: controls, plants and completeness; results read CERTIFIED only when every input tag is certified, '
        'FLOAT-PASS otherwise)' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))     # F1
    return 0


if __name__ == '__main__':
    sys.exit(main())
