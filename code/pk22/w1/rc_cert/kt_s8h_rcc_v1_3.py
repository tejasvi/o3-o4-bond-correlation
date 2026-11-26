#!/usr/bin/env python3
"""kt_s8h_rcc_v1_3.py -- pk22 (code/pk22/w1/rc_cert/). DRAFT. NE's certified RC engine (phase (iii), the approval to build from
pk24's spec pk24/NE_RC_CERT_SPEC_v1_1.md, 23d87650; the review e2153860 with the delta check 08e35758). It certifies Cov(s_e, s_f) > 0
for NE's rows on the horizontal chain, the FLIP/SAME and MIXED classes of a top-row or bottom-row edge with a horizontal or vertical
partner, every two-sided class with n >= 5 (so the 58 separated D0 pairs of P_3 x P_5, W1a's UP pairs, and NE's classes at larger n) and
every inf and far class, at N = 4 for J >= 350 (pieces 61..903) and N = 3 for J >= 300 (pieces 0..903), the last piece to t = 0. Nothing
is claimed before the review of this engine, the check of its record and the user's word.
v1_3 (the pins-only revision of v1_2, 1a04598f, by make_rcc_v1_3.py): CERT_PINS holds runner c3_1's records and asm outputs of
both N by full sha256; nothing else changes. v1_2 (the revision of v1_1, 26e64080: C-FMT on runner c3's records in cert mode, with PLANT-C3-KEYSWAP and PLANT-C3-N; the kill
rule's top-mode bound S8's m0 <= 8; C-TARGET-H also holds each row's certified [lo, hi] against its centres' value at the thin
chains) adds, with v1_1, the controls of spec sects. 2, 6, 8 and 9 that v1 (kt_s8h_rcc_v1.py, 9cb433d6) lacked; its forms and
rows are v1's, except that the pair form's C1 = t1 + ddet + lin is kept as a ball (s8core's sf_pair keeps t1 + ddet so; a ball and its
upper end bound the same) and the pair form also runs without a dual pair (thin chains: the plain bound only).
- Kept from the float engine rcm6, in the smoke item (sect. 8): rcm6's control block at t = 0 and the first piece, copied verbatim with its float
  machinery and the n lists of N5-1 (n = 5..8): C-HARM-H with PLANT-RES-H and PLANT-END-H, C-REPRO-H, C-HARM-H P2, C-HARM-H-M (A, P2)
  with PLANT-RES-M, C-HARM-RC with PLANT-RC, C-P2-REG, C-REPRO-M, RCXW and RCIN (INFO), on pk11's float tables (pinned).
- C-HARM-RCC (new; the same check on this engine's own certified chain): at the last piece with t = 0 (the harmonic limit; the entries'
  bars and the piece's vacuum kept), the harmonic value (N - 1) T^2 / 2 of every MIXED class (HV two-sided at n = 5..8, HV and VH at
  infinity, m = 1..8) and every FLIP/SAME class (two-sided at n = 5..8 over DN, inf, m = 1..8) lies in the certified [lo, hi];
  PLANT-RCC (tau' = 0) must break it.
- C-REPRO-RC5 with PLANT-REPRO-RC5 (sect. 6): at the first piece, P2-13's exact float value of each of the 18 n = 5 keys at the box's
  ends and centre lies in the certified [lo, hi]; with each exact value at hi + |hi| / 100 every key must fail.
- C-MIXED-REG with PLANT-MIXED-REG (sect. 8), at the first and last piece: the certified pair form with the vertical chain on both
  sides (RC's balls empty, the vertical dual pair) against s8core's sf_pair (parity off), ball for ball over every S8 class; dk_class2
  against dk_class; far_lo2 on both bases. The plant: the right chain's slot-0 insertion vector + 1e-9.
- CONS (the consistency gate, M1CONS's place): every row's centre value lies in its [lo, hi], each piece.
- Sect. 2's checks on the horizontal chain: C-UNIF-H (the ten entries' enclosures over the box against thin entry values at 9 t,
  END_MODES) with PLANT-UNIF-SLACK-H; C-MV-H (the centred horizontal chain with zero bars and delta 0 against thin point chains at 9 t
  in END_MODES, leaf by leaf, 2^-20 rule) with PLANT-MV-H (t-gradients 0); C-MV-BAR-H (the piece's own centred chain against thin
  points with every bar offset, coefficient, wrapped allowance and delta at a corner) with PLANT-MV-BAR-H; C-TARGET-H (the box's C1 and
  dz of the pair-form rows of smallest headroom against their values on the thin chains at 3 t x END_MODES) with PLANT-TARGET-H, and
  C-MV-SF-H (the class-level balls against the thin chains' Num and Z); C-PIECE-H (each half of a piece with the parent's basis,
  vacuum and U: no row's lower end below the parent's, no m0 larger) with PLANT-PIECE-H (the parent collapsed to its right end).
  Places: the smoke (first and last piece, every plant), each chunk (C-UNIF-H and C-MV-H on its first and last piece and every 100th,
  C-MV-BAR-H and C-TARGET-H on its first), the final (all of them, with C-PIECE-H, at each family's binding piece and the first and
  last covered piece).
- The final and the record carry the coverage list (sect. 7: every class key with its pieces, its largest top-mode threshold m0 and
  its smallest headroom) and the pair-to-class map of the 80 D0 pairs (sect. 9, Q5: class, orbit and the image that reaches the pair,
  from pk24/n5/out/n5map_v1.out, pinned), with each separated pair's smallest headroom at both N.
Forms (spec sects. 1-7): Lemma RC on S8's chain: slots 0 and 1 from the exact one-vac entries fT (E3T) and hT (H4T),
slot 0's norms from the 4-strip entries S4,x,0,HT and S4,xy,0,HT,2,HT (runner c3's CS4 keys x and xx), slots 2..7 and the bulk vector at
infinity as RC's centres with Euclidean W'-balls (rc_chain_m's radii; |v_i| capped by R_w), the bottom row as the parity mirror (F-a),
every slot of DN (F-b); the two-chain pair form sf_pair2_rc with S8's class-level branch; the top-mode covers dk_class, dk_class_h and
dk_class2; the far bounds far_lo2 and far_lo2_h (routes A and B).
C-1, the mean-value form: one entry box per piece, [t] then S8's W3 entries' bar slots then the ten horizontal entries' bar slots
(comb_duals; every key list sorted by str). S8's W3 chain is rerun on this box (s8core's chain() in duals and at the midpoints, with
piece_eval_RB's basis C0 and vacuum; its centred leaves are compared with piece_eval_RB's, C-VRERUN), so every dual of both chains has
one slot list. The horizontal chain runs in the same two passes (chain_h_c), RC's centres in both, RC's radii once from the centred
chain (upper ends over the box, S8's upper-end rule), and the two runs are joined leaf by leaf by s8core's _cen. The pair form's Num_c and Z_c are
duals of both sides' centres chains joined by _cen, with C1 = t1 + ddet + lin and dz fixed upper ends (sf_pair2_rc_cert).
C-2: the ten entries per N from runner c3_1's records (cert mode: m3_c3_<CE3|H4T|CS4>_N<N>_J300_c3.json through m3_reader_v6_3.load with
c3's asm output; pinned by a pins-only revision after production) or, in dev mode, from c3's float twins (KEYJSON a_k with their own err;
never a claim). Bar targets at N = 4: fT/hT <= 1e-4, S4 HT <= 5e-5 (printed against the entries' bars).
C-3: tau' = eps_H rho_1^2 + TRB_H / (1 - delta)^2 - alpha_lo with S8's delta for the piece (vac), alpha_lo at the c box's upper end and
t_max = 1/J_lo (gates J1, J2), eps_H = c_N / J_lo, TRB_H the rule's J-uniform row-T value; beta_H = max((N-1)/2 - ce_lo, TRB_H / (1 -
delta)^2) (the review 19f74c2b (b) with B-1); C-MHAT cited from pk02/out/out_m2b_asm_v1.out (l.7 N = 4, l.19 N = 3), whose RECORD line
names the M2(b) record S8 pins (CERT_M2B) with its sha256. Per piece: delta < 1, tau' > 0, J1, J2, B3, TR, T0, c_fix in the c box.
C-4: no horizontal chain carries a 'dual' key; each side of a pair carries its own dual pair (chd, chm, rad, keys) beside it.
C-DUAL-OWN (each piece) with PLANT-DUAL-SWAP; C-DUAL-KEYS (each piece and before each pair's _cen) with PLANT-DUAL-KEYS-SWAP and
PLANT-DUAL-KEYS-DROP.
n = 5 (spec sect. 6): the four filters at n >= 5; N5ABSENT = 0 (every n = 5 key a computed row on every piece) as a gate.
Kill rule per piece: every row's certified lower end > 0; every class covered (top-mode m0 not None and m0 <= M0MAX = 8, S8's KILL
rule, which spec sect. 7 cites; v1 and v1_1 allowed m0 <= MM + 1 = 17, also complete since the rows run to MM = 16, and their dev
grids met at most m0 = 7; so the rows m = 1..m0 - 1 and the cover from m0 on leave no m out); every gate above, CONS included;
s8core's C5 and C6 errors fail the piece. RISK lines for headroom below 2.
Items: smoke N (S8's first piece of N and the last piece: rows, gates, every control and plant of the list above), chunk N a b (pieces
a..b-1, every row, the sampled checks), final N (coverage of [RSTART, 904) by valid chunks of this script, minima per class, the n = 5
keys, the coverage list, the pair map, C-PIECE-H and the other checks at the binding pieces, PLANT-PIECE-H), record (both smokes and both
finals of this script VALID; cert mode writes the record).
Usage: kt_s8h_rcc_v1_3.py cert|dev smoke|chunk|final LIM N [a b] | cert|dev record LIM."""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import sys, re, json, math, hashlib, resource, importlib.util, traceback, time
from fractions import Fraction

USAGE = 'usage: kt_s8h_rcc_v1_3.py cert|dev smoke|final LIM N | cert|dev chunk LIM N a b | cert|dev record LIM   (LIM 10..540)'
_a = sys.argv[1:]
if len(_a) < 3 or _a[0] not in ('cert', 'dev') or _a[1] not in ('smoke', 'chunk', 'final', 'record'):
    print(USAGE)
    sys.exit(2)
MODE, ITEM = _a[0], _a[1]
LIM = int(_a[2]) if re.fullmatch(r'[0-9]{1,3}', _a[2]) else -1
if not (10 <= LIM <= 540):
    print('bad LIM %r' % _a[2])
    sys.exit(2)
_need_n = {'smoke': 1, 'final': 1, 'chunk': 3, 'record': 0}[ITEM]
if len(_a) != 3 + _need_n or not all(re.fullmatch(r'[0-9]{1,3}', x) for x in _a[3:]):
    print(USAGE)
    sys.exit(2)
NAB = tuple(int(x) for x in _a[3:])
if NAB and NAB[0] not in (3, 4):
    print('bad N %r' % (NAB[0],))
    sys.exit(2)
if ITEM == 'chunk' and not (0 <= NAB[1] < NAB[2] <= 904):
    print('bad piece range %r' % (NAB,))
    sys.exit(2)
N = NAB[0] if NAB else 4   # the record item evaluates nothing; N only sets the ported constants
CODEDIR = '/mnt/g2/release/root/code'
TOP = CODEDIR + '/pk22/w1/rc_cert'
OUTD = TOP + '/out'
LABEL = 'kt_s8h_rcc_v1_3'
SFX ={'smoke': lambda: 'smoke_n%d' % N, 'final': lambda: 'final_n%d' % N, 'chunk': lambda: 'c%d_%04d_%04d' % NAB,
       'record': lambda: 'record'}[ITEM]()
OUT_PATH = os.path.join(OUTD, 'out_%s_%s_%s.out' % (LABEL, MODE, SFX))
REC_PATH = os.path.join(OUTD, 'ne_rc_record_%s_%s.kv' % (MODE, LABEL))
if not (os.path.isdir(OUTD) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUTD)
        and os.path.realpath(OUTD).startswith(os.path.realpath(TOP) + os.sep)):
    print('output directory check failed')
    sys.exit(2)
FH = open(OUT_PATH, 'x')
T_START = time.time()


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


FAILS, NOFIRE = [], []
fails = FAILS   # the ported controls append to 'fails'


def gate(name, ok):
    if not ok:
        FAILS.append(name)
    return 'PASS' if ok else 'FAIL'


def plant(name, fired, line):
    if not fired:
        NOFIRE.append(name)
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))


# ---- pins
CERTCOPY = CODEDIR + '/pk22/w1/ne_cert/kt_s8_cert_v1_14_3_ne.py'   # pk22's path-only copy of pk11's kt_s8_cert_v1_14_3 (a6eea55f)
HZT = CODEDIR + '/pk15/out/export_p2_t_cert_kt_p2_assembly_v1_37_1.kv'
RUL = CODEDIR + '/rv01/RULING_P3_BETAH_TRBH_rv01.md'
M2BO = CODEDIR + '/pk02/out/out_m2b_asm_v1.out'   # C-MHAT's cited run (l.7, l.19) and its RECORD line
M3O = CODEDIR + '/pk22/m3/out'
C3G = ('CS4', 'CE3', 'H4T')
C3REC = {n: {g: M3O + '/m3_c3_%s_N%d_J300_c3.json' % (g, n) for g in C3G} for n in (4, 3)}
C3ASM = {n: M3O + '/m3_run_v1_9_3_asm.%d.out' % n for n in (4, 3)}
TWF = {4: {'CS4': M3O + '/m3ref_px22_v1_5_P16CS4.4.p5_z9sym.out', 'CE3': M3O + '/m3ref_px22_v1_5_P16CE3.4.p1_z9sym.out', 'H4T': M3O + '/m3ref_px22_v1_5_P16CH4T.4.p5_z9sym.out'}, 3: {'CS4': M3O + '/m3ref_px22_v1_5_P16CS4.3.p5_z9sym.out', 'CE3': M3O + '/m3ref_px22_v1_5_P16CE3.3.p1_z9sym.out', 'H4T': M3O + '/m3ref_px22_v1_5_P16CH4T.3.p5_z9sym.out'}}   # dev mode: runner c3's float twins (pieces with P16-DONE)
W4OUT = CODEDIR + '/pk11/out'   # the float engine's controls: pk11's float tables (HJ) and P2-13's outputs (P13O, P13L), read only
MKD = W4OUT + '/s8h_mk_v1'
# ---- input paths copied verbatim from rcm6 (sha256 b66df08dbaa72f8f3ef2b55d5a4c5bf678611cc1e9c6251a6bb48761488c0f22):
#   HJ 25852108640f8b4c8469dc3efed9e2e6f7a36d7a858b129e086b9018cef74e7a
#   P13O 71a74a9571b4c0fae9686a20b007397f2a6ffc66de6c7686037973a9ede33ebb
#   P13L 42075dbd043e9bdbea1dc2600a265a05682cf08411e601516206167f12e26473
HJ = {(4, 'small'): MKD + '/s8h_float_v1.4.small.json', (3, 'small'): MKD + '/s8h_float_v1.3.small.json',
      (4, 'h4'): MKD + '/s8h_float_v1.4.h4.json', (3, 'h4'): MKD + '/s8h_float_v1.3.h4.json',
      (4, 'n2t'): MKD + '/s8h_float_v1_1.4.n2t.json', (3, 'n2t'): MKD + '/s8h_float_v1_1.3.n2t.json',
      (4, 'l'): MKD + '/s8h_float_v1_2.4.l.json', (3, 'l'): MKD + '/s8h_float_v1_2.3.l.json',
      (4, 's4h'): MKD + '/s8h_float_v1_3.4.s4h.json', (3, 's4h'): MKD + '/s8h_float_v1_3.3.s4h.json'}
P13O = {4: [W4OUT + '/out_kt_s8f1_v1_3_n5a.4.out', W4OUT + '/out_kt_s8f1_v1_3_n5b.4.out'],
        3: [W4OUT + '/out_kt_s8f1_v1_3_n5a.3.out', W4OUT + '/out_kt_s8f1_v1_3_n5b.3.out']}
P13L = W4OUT + '/S8F2_ENTRY_LIST_v1.json'
HZX = HZT   # the ported hz_rows reads this name
N5MAP = CODEDIR + '/pk24/n5/out/n5map_v1.out'   # the pair-to-class map of the 80 D0 pairs (pk24/n5/n5map_v1.py; spec v1_1 sect. 6)
PINS = {CERTCOPY: 'e5c291e801bd4aa5016e3a3eae44f5235f4a7316cf6136c200258d955aeeaf3e', HZT: 'ad7e863d44d48bd59946f48c1de261f51751cd064f6129fc56d85cad9c7ee844', RUL: '7147e76610b6c8ebc5aae056cb9fc88641924c98921b13d74d5ce0b75db476ba', M2BO: 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391'}
PINS.update({HJ[(3, 'h4')]: '32057a2fef03c7de3d799ce5f73806bc6f68a25ca35b05f4a5072679e10c06f1', HJ[(3, 'l')]: 'd229b036cdda9391ac3cdf74d32e99aad8e2b6a405f78f160f45f7c42725d96e', HJ[(3, 'n2t')]: 'cdbd310b629a9279e223a2e4d20907af78dd5d511029e69edbb4e9af458fa5ba', HJ[(3, 's4h')]: 'f1a9bd1c75ef92d526aa98bfc100a365b2144a0eb93195acefaf1045abe9da0c', HJ[(3, 'small')]: '2f1604d6693fa9eebcd3e27c236ec47f4cc29b862fa7e252ec731ccea24d9f4c', HJ[(4, 'h4')]: '9eec7646eb9233754a1877cb3d4950c4c88b31a43b8140712ce19aef7e2a839a', HJ[(4, 'l')]: '9e9cc80de83a683840edc2ec2877ca0dfda2b09089d5065f828ef65bf988e63e', HJ[(4, 'n2t')]: '0b7c7c969032d4ae8fa763e1da7049846333b30745cf270c2f8d948f9adcc310', HJ[(4, 's4h')]: '260435f5cbfefa41ef7b30283ab2491e36f46d34910df01768615175a614e65e', HJ[(4, 'small')]: '562748035ce6e03031b86c0fae88d6773fc52f93d5a9bd9ca0f59c57a5c3641c', P13O[4][0]: 'f89b307744fafefdf3978880afbbec633f5fc4918bcbf9f77886ecd7c8f866c7', P13O[4][1]: 'ce8be6246184bfc34b84644ed5470f22be703ecfb55317a01b2483b777d86e7f', P13O[3][0]: '2b0633395e747093c88ce1caf8b9417d6f882d4e89633142ca06b34816f78e29', P13O[3][1]: '3990ee22cb6e7f291cbad1be1f687b8534eda8dffea1696288e9780cd6283f0b', P13L: 'adaf07438f867232310c5a9f521461a9447b148b6895ed278bba3f7ecd1b03ff', N5MAP: '359c33418a268abcb4d8bc698573ea3fa5ce347c4a5ee49c30b2c3ff7ea7e144'})   # HJ and P13O at both N, P13L (each = rcm6's pin) and N5MAP (= spec v1_1's file list)
DEV_PINS = {TWF[4]['CS4']: '4a9062ac459aba26b1605d7036a738b6a7248b7a71e92b87bc46927963f18390', TWF[4]['CE3']: 'e2f900acac3839b80d51dfbfab73d82a417741e2619775d0b5af901e1c62ca39', TWF[4]['H4T']: '713d8003141091bb7c5b952eb56d9899a49a5a303baad9172ba2b1e2da344dc7', TWF[3]['CS4']: 'f77f725eafa9cbbb6722ad61b978d719cfbf5a8f40bd46c5ac40ac930953b8e7', TWF[3]['CE3']: 'e129d24fd4a122c0ff6cb22114b98ba08c792cfc3f2808a1fc426a122581033e', TWF[3]['H4T']: '4601813b86e626242d47ceca3ac868bb3f52079a358ae05538c816261568a16e'}
CERT_PINS = {C3REC[4]['CS4']: 'c0614f924bedd3a68bd11cd5976e479b31a86a0e85b5ec91133f70e02ee78230', C3REC[4]['CE3']: 'ab64935d7ba4857f089d91bac27a36f76fe1d35ae228af2bc20003a8e5e3eb18', C3REC[4]['H4T']: '20922bae66b79573f0442d351bf610d10bed89330b53f945a6adfc36c2caca25', C3ASM[4]: '788d8559c18c568e0212e2d46bfb37b485f4988a89cc0fbc8530b5ffcb1957b8', C3REC[3]['CS4']: '95f54466e52a79d8540041da90385f6683d79d5363ee2728877ba92065e88d01', C3REC[3]['CE3']: '3bedff291ef056d4664217752da3bf668fd74f8bea6a6d1696102b24aea90fa8', C3REC[3]['H4T']: '4a8297efd90554d2330bd7f40a6b60d99fda52b7511c53f78142b37f99572466', C3ASM[3]: '6baf16dd5bde7f6d7df2455b8b9f590eea6a25ee0074042aeea1459ed924a983'}   # runner c3_1's records and asm outputs by full sha256 (make_rcc_v1_3.py)
out('%s sha256 %s MODE=%s ITEM=%s LIM=%d %s; python %s' % (LABEL, sha_file(os.path.abspath(__file__)), MODE, ITEM, LIM, SFX,
                                                          sys.version.split()[0]))
_need = dict(PINS)
_need.update(DEV_PINS if MODE == 'dev' else CERT_PINS)
_bad = ['%s %s' % (os.path.basename(p), sha_file(p)[:8]) for p in sorted(_need) if sha_file(p) != _need[p]]
out('C-HASH (%d pinned files: the S8 module copy, pk15\'s certified t export, the TRB_H rule, the M2(b) asm output, the float engine\'s '
    'tables and P2-13\'s outputs and list, the pair map, and the %s) -> %s%s' % (
        len(_need), 'c3 float twins (dev)' if MODE == 'dev' else 'c3 records and asm outputs (cert)', gate('C-HASH', not _bad),
        (': ' + '; '.join(_bad)) if _bad else ''))
if MODE == 'cert' and not CERT_PINS:
    out('C-CERT-PINS: runner c3\'s records are not pinned in this version (cert mode waits for the pins-only revision) -> %s' %
        gate('C-CERT-PINS', False))
if FAILS:
    out('VERDICT INVALID (%s)' % ', '.join(FAILS))
    sys.exit(2)

# ---- the certified S8 module (stage A, the vertical chain, its core) through its path-only copy, in its cert chunk namespace
_nn, _ia, _ib = (N, NAB[1], NAB[2]) if ITEM == 'chunk' else (N, 0, 1)
STRAY = CODEDIR + '/pk22/w1/ne_cert/cert_out/out_kt_s8_cert_v1_14_3_ne_cert_c%d_%04d_%04d_r%d.out'
_free = [k for k in range(1, 100) if not os.path.exists(STRAY % (_nn, _ia, _ib, k))]
if not _free:
    out('VERDICT INVALID (no free stray tag r1..r99 for the S8 module copy\'s import)')
    sys.exit(2)
out('IMPORT: the S8 module copy in its cert chunk namespace c%d_%04d_%04d with tag r%d (a stray output in ne_cert/cert_out, not counted)'
    % (_nn, _ia, _ib, _free[0]))
sys.argv = [CERTCOPY, 'cert', 'chunk', str(LIM), str(_nn), str(_ia), str(_ib), 'r%d' % _free[0]]
_spec = importlib.util.spec_from_file_location('kt_s8_cert_v1_14_3_ne', CERTCOPY)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)
CM = mod.CM
arb = mod.arb
D = CM.D
ZERO, ONE = CM.ZERO, CM.ONE
HENT = {}   # the float engine's tables for the ported controls (filled by the smoke item; no row of this engine reads them)

# ---- copied verbatim from pk24/ne/kt_s8hf_rcm6.py (sha256 b66df08dbaa72f8f3ef2b55d5a4c5bf678611cc1e9c6251a6bb48761488c0f22) by make_rcc_v1_2.py (N5-1 lists amended in harm_check_rc, harm_check_m and m1_controls); each segment's sha256 as written here:
#   DN e7dce8a2f807ef2ef06cfd7d0382ed9baa68d2c7ae85477ef6a4db8a6aaa445f
#   DF b4da5e9bee1f8fe070b66dbbe1dbd6d22fd7b234cf52f55045b44e5e17ed2ebd
#   T_M 1ea3e23e1a8ffe236f1a7d76b4f1d20905086c09f864286e5ddd96fb1f26eb3b
#   NEAR_H 7565104d6a6e220047b0e858e7916c8c112729b1f0bcc53182cb2c0d1efdc0db
#   NEAR_V f728506903cedfa531ed81ba351b73e60fabf55bc908a5a93baf9b1f267a97b9
#   DF_V, DF_H 9928d8f46ed56592df6dee25508f251f1832b3bfc840248a645095c6691d898d
#   N5HV 9d63934133295cc1f03c6848d7c3adc8104af80585d3c99aaa1a87cd8ec7f931
#   N5H2 f2b5999e082775fdcba958f51299f2e902d80e48bc7ebfb732728c6718a3e3fd
#   N5KEYS 00c5fe9b94c287b14fdf73715b26974dbd1ef7b454a776821adc2a26eb58d62a
#   CN d5302bf8ede77d5a88e0f9a9a1f912387488b334fede89fb4888f47c6088720b
#   setup_h c2be0def172a1587745b8bd292843e4a32fe94a598699453d538b1eb0c3bb7b3
#   dk_class_h 57b007927c867ee4fd12df13d78ad3f6549d19a1be58b97b955a80a937bc4b3f
#   far_lo2_h 7be1210f73a41f95aea89d25def6e8e8727f2085c33191c1a17d97299a8bff52
#   vecs2 b2c051de31f34223705e191e6ad5c7d153799d573b1491f1dfa131afb007d60b
#   cov2_2 20be96a91a0efad1a8419cbdbfdcd49bec0832a53743233b0c7c624dc6fd2d06
#   dk_class2 969b98598e799f91b47ea9358c898438f459c6d0d53c14cb6944f117e534565a
#   frob_up 8b1e420a96fba6c61d227e8d09a61ed1c5c5cd3eea21e3f91a9d71e0edb71b92
#   rc_setup_m ebd86611d074c26825ece259002830e2fa368b5e30151228d1b9b1467095cd95
#   n5key 5a3e5f3dcf3600d7999381b79e2dde546e975ccb931b5b07afbaea12aeb99452
#   ser 2698076c62a66d2423edb112476804db966a3a9161c3edfceb532297b27a1a24
#   chain_h 04bdcc3c5ae90a4b32192fef2d3380888ef2438b9bb77ce053e547656188d243
#   vpair 47538b9fe64506f6e6c9c01a335d2d554da28e0ac8ee91bad8510215d61f2599
#   strip_T 56a9d655d14999384ebde53047450a6dbd43e51d364a1f97ba32613ac2097711
#   harm dce10afad8b2d6339b2d8268f981830ed992bdc98dd1587955c23e81fce0f818
#   piece c2bb80c2ce5ac8df781d29a10ebe64bb2020c6f65c587c16be26f398d131d5b1
#   zero_vac ff1d97ada08f804522a0d798ac3c7c5ad8babd1d610aa446a415295697818b18
#   jacobi_eig 320a29635252908b4e9255b3910880893959d4af6b0121befd18c0d2efe1977d
#   bperp 8c30c6d29d5d03ccde63eb316b3b797ae3aa8d373d3eb95fcdc42030b6bb3fae
#   setup_p a53ae2da2adc5f4a4dd7f8dc2d48cc050792330438ad21ce2a150d1bfbb8affe
#   setup_p2 a7d10e5345d97299c3c7e298186dfcd6911e45916650089efc76379eb4c6a9a5
#   bp_piece 7c2a1b86881256dfaf5c109b7937648cce2afec57d08886c8e036956c880dfbb
#   sf_pair2 5926ea9eea19c944d2c584bb3f529631da9823b3b6cc3f2bbb6bd91f0f704c70
#   sf_pair2_rc 10a30e003cc1cf20cca5c10c766915a063cd062da197b4f7b57f3c9a1c66329d
#   rc_chain 6028a4c273b5389639a416bb65dd6f1aa33cac7a204b3c7f7fb089c4172ae0d4
#   rc_setup 586c0716e6e3f1766da112904df669c9e0082629145f3d614f2f7bef2769d7c3
#   harm_check_rc 20847f8a7b4940c2e373b7d330fcbe0f1a546e06b023276f4fb350bedb5ca402
#   rc_xw 632dcb4bb02df31c70d5be33d24318014596a0fb6d7a77caa2e7cf9de3faa78b
#   rc_contain bce3b90d47aabaa915314d68b22f1330176c99e6758512be93f06bfa350812c5
#   same_val 8db753eca3b79e95dc50a34cb415b42bd48dc366b5a10e015574c583545bdee6
#   harm_m 1434cae3a09af13ccb21241c54437b360e33f1dcbd9dc0e0a6078d1f627188c5
#   harm_check_m 35f30b3d76e8197ad8a7309c0c327c594300caf545b2dad4b0837b4fa28eb12f
#   zero_res 4ae121563abfd1377dc04c5aa47f46d097028adca6098b17573050a829767b9d
#   load_json_entries a075d0d017af8b20eb9f6b964a0e4da6b17184359ae27c6cbca6133c745fd314
#   beta_h 22ffd7328c025fb552b5226d7c031bcd2ff59e9a1d5083a59aff90914c096228
#   hz_rows a51c609da4b5779eb19fcbea8c9468574c56f32ad458153321f09ad0804453cc
#   m1_controls (block) 22ef070e6a2dd2416cde9cbad1ce326cf97933b102065b9d33cc307f9e7db71f
DN = {'flip': (0, 1, 2), 'same': (0, 1)}
DF = {'flip': 3, 'same': 2}
T_M = {4: 3, 3: 2}[N]
NEAR_H = tuple(range(0, T_M + 1))
NEAR_V = tuple(range(-1, T_M))
DF_V, DF_H = T_M, T_M + 1
N5HV = ((0, 1, 1), (1, 0, 1), (2, -1, 1), (0, 0, 2), (1, -1, 2), (0, -1, 3))
N5H2 = ((0, 0, 2), (0, 1, 1), (1, 0, 1))
N5KEYS = ([('M2', ('HV', a_, b_, k_, m_)) for k_ in ('same', 'flip') for (a_, b_, m_) in N5HV]
          + [('H2', (a_, b_, k_, m_)) for k_ in ('flip', 'same') for (a_, b_, m_) in N5H2])
CN = 2.0 + (N - 1) * (N - 3) / 8.0


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


def frob_up(M):
    return CM.sqrt_up(sum((x * x for row in M for x in row), ZERO))


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


def n5key(fam, key):
    """rcm6: the P2-13 key of an n = 5 two-sided row (H2 (dL, dR, kind, m): t at column dL, the other edge at column 3 - dR;
    HV (iH, dV, kind, m): t at column iH, the vertical edge at column 3 - dV), else None."""
    if fam == 'M2' and key[0] == 'HV' and key[1] + key[2] + key[4] + 3 == 5:
        return 'S5,xy,%d,HT,%d,%s' % (key[1], 3 - key[2], 'TM' if key[3] == 'same' else 'MB')
    if fam == 'H2' and key[0] + key[1] + key[3] + 3 == 5:
        return 'S5,xy,%d,HT,%d,%s' % (key[0], 3 - key[1], 'HB' if key[2] == 'flip' else 'HT')
    return None


def ser(a, t):
    s = ZERO
    p = ONE
    for c in a:
        s = s + arb(c) * p
        p = p * t
    return s


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


def bp_piece(chV, jlo, ce_lo, alpha, trb):
    """beta_perp(float) at a piece (kt_s8hp_v1_1's inputs): rho_1 the largest |Ritz value| of S' on W', kappa = (N-1)/2 - c_lo, eps_H =
    c_N / J_lo; returns (beta_perp, kappa rho_1^2, eps_H rho_1^2 + TRB_H - alpha, rho_1, kappa, eps_H)."""
    rho1 = max(abs(x) for x in jacobi_eig([[float(x.mid()) for x in row] for row in chV['R']]))
    kap = (N - 1) / 2.0 - float(ce_lo)
    epsH = CN / float(jlo)
    return bperp(kap, rho1, epsH, trb, alpha) + (rho1, kap, epsH)


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


def harm_check_rc(cH, prmH_, chV, prmV):
    """pk24: C-HARM-RC at t = 0 on sf_pair2_rc, for the MIXED classes of harm_check_m and the FLIP/SAME classes of harm_check (every
    slot of DN); the harmonic value must lie in [cov_lo, cov_hi] (slack 1e-12 relative). Returns (classes, failing, the largest
    lo / harmonic with its class)."""
    RkC = {}
    rows = []
    for kind in ('same', 'flip'):
        cls = []
        for iH in NEAR_H:
            cls += [('HV', iH, dV, kind, m) for dV in NEAR_V for m in range(1, 9) if iH + dV + m + 3 in (5, 6, 7, 8)]
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
            cls = [(iL, iR, kind, m) for iR in DN[kind] for m in range(1, 9) if iL + iR + m + 3 in (5, 6, 7, 8)] + \
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
    """C-HARM-H-M at t = 0: HV two-sided classes at n = 5..8, HV and VH at infinity (m = 1..8), both kinds; the harmonic value must lie
    in [cov_lo, cov_hi] (float rounding slack 1e-12 relative). Returns (classes, failing)."""
    RkC = {}
    cls = []
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            cls += [('HV', iH, dV, kind, m) for dV in NEAR_V for m in range(1, 9) if iH + dV + m + 3 in (5, 6, 7, 8)]
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


def m1_controls(A, HENT, BETA, HZ, i0):
    """rcm6's control block at t = 0 and the first piece (its l.1625-1817, copied verbatim by make_rcc_v1_2.py, with the n
    lists of N5-1): C-UMAIN (INFO), SPAN, C-HARM-H with PLANT-RES-H and PLANT-END-H, C-REPRO-H, C-HARM-H P2, C-HARM-H-M (A, P2)
    with PLANT-RES-M, C-HARM-RC with PLANT-RC, RCXW and RCIN (INFO), C-P2-REG and C-REPRO-M, on the float tables HENT (the float engine's
    float machinery). Returns (img, pv): P2-13's key map and exact float values, for C-REPRO-RC5."""
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
                cls = [(iL, iR, kind, m) for iR in DN[kind] for m in range(1, 9) if iL + iR + m + 3 in (5, 6, 7, 8)] + \
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
    return img, pv


# ---- inputs
HNAME = {'S4,x,0,HT': ('CS4', 'x'), 'S4,xy,0,HT,2,HT': ('CS4', 'xx')}
for _k_ in range(4):
    HNAME['fT,%d' % _k_] = ('CE3', 'fT,%d' % _k_)
    HNAME['hT,%d' % _k_] = ('H4T', 'hT,%d' % _k_)
BAR_TARGET = {4: {'f': Fraction(1, 10000), 's': Fraction(5, 100000)}, 3: {'f': Fraction(1, 10000), 's': Fraction(5, 100000)}}
M0MAX = 8   # the kill rule's top-mode bound: S8's KILL rule (no top-mode cover with m0 <= 8), as spec sect. 7 cites it


def c3_entries(n):
    """the ten horizontal entries {chain name: (LO, HI, err)}: cert mode from runner c3's records (m3_reader_v6_3.load with the asm
    output; entry_ball: ak -+ ak_rad exactly, err the sum of Bp); dev mode from c3's float twins (KEYJSON a_k as LO = HI, the twin's own
    err as the bar; never a claim)."""
    E = {}
    if MODE == 'cert':
        recs = {g: mod.M3R.load(C3REC[n][g], C3ASM[n], 300, n) for g in C3G}
        for nm, (g, key) in HNAME.items():
            E[nm] = mod.M3R.entry_ball(recs[g], key)
        return E
    for nm, (g, key) in HNAME.items():
        d = None
        for ln in open(TWF[n][g]):
            if ln.startswith('KEYJSON '):
                dd = json.loads(ln[len('KEYJSON '):])
                if dd.get('key') == key:
                    d = dd
        if d is None or d.get('N') != n:
            raise ValueError('%s: no KEYJSON line for %s at N %d' % (os.path.basename(TWF[n][g]), key, n))
        ak = [Fraction(repr(float(x))) for x in d['ak']]
        E[nm] = (ak, list(ak), Fraction(repr(float(d['err']))))
    return E


def fmt_c3(n):
    """C-FMT on runner c3's records (cert mode; spec sect. 8): each of the three records of N loads through the S8 module's bound reader
    (m3_reader_v6_3.loads with its asm output: VERDICT VALID and the RECORD line with the record's sha256), and each needed key reads as
    four coefficient spans with lo <= hi and a bar >= 0. Plants, per record: PLANT-C3-KEYSWAP (the record's text with the names of two of
    its needed keys swapped, read against the same asm output) and PLANT-C3-N (the record read as the other N) must be refused. Returns
    (failures, {plant: [fired per record]})."""
    bad, fired = [], {'PLANT-C3-KEYSWAP': [], 'PLANT-C3-N': []}
    for g in C3G:
        path, asm = C3REC[n][g], C3ASM[n]
        name = os.path.basename(path)
        text, atext = open(path).read(), open(asm).read()
        keys = [key for nm, (gg, key) in sorted(HNAME.items()) if gg == g]
        try:
            rec = mod.M3R.loads(text, atext, 300, n, name)
            for key in keys:
                LO, HI, err = mod.M3R.entry_ball(rec, key)
                if len(LO) != 4 or len(HI) != 4 or any(lo > hi for lo, hi in zip(LO, HI)) or err < 0:
                    bad.append('%s %s malformed' % (g, key))
        except Exception as e:
            bad.append('%s: %s' % (g, e))
        k1, k2 = '"%s"' % keys[0], '"%s"' % keys[1]
        t2 = text.replace(k1, '"KSWAP_TMP_KEY"').replace(k2, k1).replace('"KSWAP_TMP_KEY"', k2)
        try:
            mod.M3R.loads(t2, atext, 300, n, name)
            fired['PLANT-C3-KEYSWAP'].append(False)
        except Exception:
            fired['PLANT-C3-KEYSWAP'].append(t2 != text)
        try:
            mod.M3R.loads(text, atext, 300, 7 - n, name)
            fired['PLANT-C3-N'].append(False)
        except Exception:
            fired['PLANT-C3-N'].append(True)
    return bad, fired


def hz_rows_c(n):
    """pk15's certified t export: per piece jlo (float and exact), Qvt_hi, ce_lo, ce_hi (exact rationals), jhi (float); EXPORT_STATUS
    CERTIFIED, J_UNIFORMITY per piece and the FIELDS line exactly."""
    want = 'jlo jhi At_lo Vt_hi Ot_hi Pt_hi Xta_lo Xtb_lo Aa_lo dtx_hi Qvt_hi tz_hi ce_lo ce_hi'.split()
    st, unif, fields, rows = None, None, None, {}
    for ln in open(HZT).read().split('\n'):
        if ln.startswith('EXPORT_STATUS = '):
            st = ln.split(' = ', 1)[1]
        if ln.startswith('J_UNIFORMITY = '):
            unif = ln.split(' = ', 1)[1]
        if ln.startswith('FIELDS = '):
            fields = ln.split(' = ', 1)[1].split()
        mm = re.match(r'^N(\d)_P(\d{4}) = (.*)$', ln)
        if mm and int(mm.group(1)) == n:
            v = mm.group(3).split()
            if len(v) != len(want):
                raise ValueError('t export row N%s_P%s: %d values' % (mm.group(1), mm.group(2), len(v)))
            rows[int(mm.group(2))] = dict({k: Fraction(v[want.index(k)]) for k in ('Qvt_hi', 'ce_lo', 'ce_hi')},
                                          jlo=float(v[0]), jhi=float(v[1]))
    if st != 'CERTIFIED' or fields != want or unif is None or not unif.startswith('UNIFORM-J PER-PIECE'):
        raise ValueError('pk15 t export: status %r, fields %r, uniformity %r' % (st, fields, unif))
    return rows


def trb_rowT():
    """TRB_H's J-uniform row-T values (the t bond) from the rule B-2, exact rationals of its decimals."""
    txt = open(RUL).read()
    m4 = re.search(r'N4: ([0-9.]+) \(T\) and ([0-9.]+) \(M\)', txt)
    m3 = re.search(r'N3: ([0-9.]+) \(T\) and ([0-9.]+) \(M\)', txt)
    if not (m4 and m3):
        raise ValueError('TRB_H values not found in the rule')
    return {4: Fraction(m4.group(1)), 3: Fraction(m3.group(1))}


def mhat_cite():
    """C-MHAT by citation (spec v1_1 sect. 4; the approval): pk02/out/out_m2b_asm_v1.out (pinned) has VERDICT lines
    exactly [VERDICT VALID], l.7 'C-MHAT N=4: ... -> PASS', l.19 'C-MHAT N=3: ... -> PASS', and exactly one RECORD line, naming
    M2B_KV_v1.txt with the sha256 of the M2(b) record S8's engine pins (CERT_M2B[0]), whose asm output is this same file (CERT_M2B[1])."""
    ls = open(M2BO).read().split('\n')
    rec = [x.split() for x in ls if x.startswith('RECORD ')]
    m2b, asm = mod.CERT_M2B
    ok = ([x for x in ls if x.startswith('VERDICT')] == ['VERDICT VALID'] and len(ls) > 19 and
          ls[6].startswith('C-MHAT N=4:') and ls[6].endswith('-> PASS') and ls[18].startswith('C-MHAT N=3:') and ls[18].endswith('-> PASS')
          and rec == [['RECORD', 'M2B_KV_v1.txt', sha_file(m2b)]] and os.path.realpath(asm) == os.path.realpath(M2BO))
    return ok, (ls[6] if len(ls) > 6 else '', ls[18] if len(ls) > 18 else '', os.path.basename(m2b), sha_file(m2b))


# ---- C-1: the combined entry box, its duals, and the key lists (C-DUAL-KEYS)
def comb_duals(EV, EH, T, zero_bars=False, zero_tgrad=False):
    """the entries on a piece box as duals with one slot list: slot 0 t, then S8's W3 entries (sorted by str), then the ten horizontal
    entries (sorted by str), each entry's bar offset in [-err_b, err_b] as its own slot (s8core's entry_duals over the joined list).
    Returns (keys, VdV, VmV, VdH, VmH, rad): duals and midpoint values (t_m = mid(T), bar offsets 0) of both groups."""
    kv, kh = sorted(EV, key=str), sorted(EH, key=str)
    keys = ['t'] + ['V:%s' % (k,) for k in kv] + ['H:%s' % k for k in kh]
    n = len(keys)
    tm = arb(T.mid())
    tk = [ONE, T, T * T, T * T * T]
    tmk = [ONE, tm, tm * tm, tm * tm * tm]
    VdV, VmV, VdH, VmH, rad = {}, {}, {}, {}, [arb(T.rad())]
    srcs = [(EV, k, VdV, VmV) for k in kv] + [(EH, k, VdH, VmH) for k in kh]
    for j, (E, key, Vd, Vm) in enumerate(srcs):
        LO, HI, err = E[key]
        a = [CM.span(LO[k], HI[k]) for k in range(4)]
        b = ZERO if zero_bars else CM.fr(err)
        g = [ZERO] * n
        g[0] = ZERO if zero_tgrad else (a[1] + 2 * a[2] * T + 3 * a[3] * T * T)
        g[j + 1] = ONE
        Vd[key] = D(sum((a[k] * tk[k] for k in range(4)), ZERO) + CM.pm(b), g)
        Vm[key] = sum((a[k] * tmk[k] for k in range(4)), ZERO)
        rad.append(b)
    return keys, VdV, VmV, VdH, VmH, rad


def dual_leaves(q):
    if isinstance(q, D):
        yield q
    elif isinstance(q, dict):
        for k in q:
            if k not in ('allow', 'par_exact'):
                yield from dual_leaves(q[k])
    elif isinstance(q, (list, tuple)):
        for x in q:
            yield from dual_leaves(x)


def keys_ok(dual, box_keys):
    """C-DUAL-KEYS on one side's dual pair (chd, chm, rad, keys): its key list equals the box's in length and order, rad has that length,
    and every dual leaf of chd has a gradient of that length (s8core's _cen zips gradients with radii and truncates silently)."""
    chd, chm, rad, keys = dual
    if list(keys) != list(box_keys) or len(rad) != len(box_keys):
        return False
    return all(len(d.g) == len(box_keys) for d in dual_leaves(chd))


# ---- the horizontal chain in any run (duals, midpoint balls or thin points)
def chain_h_c(VV, VH, chV, mains, vac, cfix):
    """rcm's chain_h_fix on run values: slots 0 and 1 from fT and hT (place-2 allowance on every component), centred by the fixed rational
    cfix (kappa = (N-1)/2 - cfix exactly), slot 0's norms from the 4-strip entries and S8's S4,Z; the entries' bars are their own slots
    of the run (no bar is added here); slots >= 2 and the bulk vector are set by rc_apply."""
    rhoE, rmain, rho4, rhob, rhoH = mains
    K = chV['K']
    C, lam0, g00 = chV['C'], chV['lam0'], chV['g00']
    sg = g00.sqrt()
    rng = range(K + 1)
    idx = list(range(1, K + 1))
    g = [[VV[('g', min(a, b), max(a, b))] for b in rng] for a in rng]
    e = [VV[('e', a)] for a in rng]
    fT = [VH['fT,%d' % a] for a in rng]
    hT = [VH['hT,%d' % a] for a in rng]

    def comps(vec, scale):
        return [scale * sum((C[k][i] * (vec[n_] - g[n_][0] / g00 * vec[0]) for i, n_ in enumerate(idx)), ZERO) for k in range(K)]
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
    ch = dict(chV)
    ch.pop('dual', None)   # C-4: never the vertical chain's dual run
    ch['L'] = L
    ch['c'] = ZERO
    Z4 = VV[('Z4',)]
    X1H, X12H = VH['S4,x,0,HT'], VH['S4,xy,0,HT,2,HT']
    F4 = rho4 * g00 / (lam0 * lam0 * e[0] * e[0])
    n2y = F4 * (X12H - 2 * c * X1H + c * c * Z4)
    n21 = F4 * Z4
    crs = F4 * (X1H - c * Z4)
    l0, y0 = L[0]
    lu, yu = l0[0], y0[0]
    sq = lambda v: v[0] * v[0] + sum((x * x for x in v[1]), ZERO)
    ap2 = lu * lu * (n2y - yu * yu) - 2 * lu * yu * (crs - yu * lu) + yu * yu * (n21 - lu * lu) - \
        sum(((lu * y0[1][k] - yu * l0[1][k]) * (lu * y0[1][k] - yu * l0[1][k]) for k in range(K)), ZERO)
    ch['h'] = {'c': c, 'res2y0': n2y - sq(y0), 'ny0': n2y, 'Ap2y0': ap2}
    return ch


def rc_centres(chH, tau_b, kap):
    """RC's centres in one run (rc_chain_m l.1455-1461): base = y(1)_W - kappa eps(1)_W + (tau'/2) eps(-1)_W; slot i in 2..7: base +
    kappa eps(i)_W - (tau'/2) eps(i-2)_W; the bulk vector pc = base / l_u."""
    K = chH['K']
    L = chH['L']
    half = tau_b / 2
    lu = L[-1][0][0]
    lW = {d: L[d][0][1] for d in range(-1, 8)}
    y1 = L[1][1]
    base = [y1[1][k] - kap * lW[1][k] + half * lW[-1][k] for k in range(K)]
    cen = {i: [base[k] + kap * lW[i][k] - half * lW[i - 2][k] for k in range(K)] for i in range(2, 8)}
    return cen, [x / lu for x in base]


def rc_radii(chHc, prmV, tau_b, betaH, vac, w_b, pn_b, kap):
    """RC's radii as piece constants from the centred chain (upper ends over the whole box: S8's upper-end rule; rc_chain_m l.1462-1476):
    rho[i] = (tau'/2) min(|v_i|, R_w) + |kappa| cerr(i) + (tau'/2) cerr(i-2) + alw, alw = sqrt(K) s (r_u + |y(1)_u|), r_u = w |l_u(i-2)| +
    pn_SH4 e[i-1]; rho[inf] = ((tau'/2) e[0] + sqrt(K) s |y(1)_u|) / |l_u| + beta_H s'."""
    K = chHc['K']
    e, rn1, cerrV = prmV['e'], prmV['rn1'], prmV['cerr']
    dmax = max(k for k in e if isinstance(k, int))
    L = chHc['L']
    half = tau_b / 2
    sp, s_ = vac['sp'], vac['s']
    lu = L[-1][0][0]
    lW = {d: L[d][0][1] for d in range(-1, 8)}
    y1 = L[1][1]
    cer = lambda d: cerrV[min(d, dmax)][0]
    rp1 = lambda d: (rn1[min(d, dmax)] + abs(lu).upper() * sp).upper()
    sK = CM.sqrt_up(arb(K))
    rho, r_u = {}, {}
    for i in range(2, 8):
        dv = [lW[-1][k] - lW[i - 2][k] for k in range(K)]
        vW = (CM.norm_up(dv) + cer(-1) + cer(i - 2)).upper()
        vP = (rp1(-1) + rp1(i - 2)).upper()
        vn = CM.hyp(vW, vP)
        vn = vn if vn.upper() < e[0].upper() else e[0]
        ee = e[min(i - 1, dmax)]
        au = abs(L[i - 2][0][0]).upper()
        r_u[i] = (w_b * au + pn_b * ee).upper()
        alw = (sK * s_ * (r_u[i] + abs(y1[0]).upper())).upper()
        rho[i] = (half * vn + abs(kap).upper() * cer(i) + half * cer(i - 2) + alw).upper()
    rho['inf'] = ((half * e[0] + sK * s_ * abs(y1[0]).upper()) / abs(lu).lower() + CM.fr(betaH) * sp).upper()
    return rho, r_u


def rc_apply(chH, cen, pc, r_u):
    """one run's chain with RC's slots 2..7 (u-part the ball +- r_u, W'-part the centre) and the bulk vector at infinity (pc for t, its
    parity mirror for bb: F-a)."""
    K, pi = chH['K'], chH['pi']
    ch = dict(chH)
    L = dict(chH['L'])
    for i in range(2, 8):
        L[i] = (chH['L'][i][0], (CM.pm(r_u[i]), list(cen[i])))
    ch['L'] = L
    ch['B'] = {'TM': list(pc), 'MB': [pc[k] if pi[k] > 0 else -pc[k] for k in range(K)]}
    return ch


def rc_boxes(chHc, rho, w_b):
    """rc_chain_m's two chains from the centred chain: chB with every RC W'-component +- rho[i] and the bulk vector +- rho[inf] (the
    boxes, for the residual terms and the top-mode covers), chC the centres (the main term)."""
    K, pi = chHc['K'], chHc['pi']
    mir = lambda v: [v[k] if pi[k] > 0 else -v[k] for k in range(K)]
    Lb = dict(chHc['L'])
    for i in range(2, 8):
        u_, cen = chHc['L'][i][1]
        Lb[i] = (chHc['L'][i][0], (u_, [x + CM.pm(rho[i]) for x in cen]))
    pc = chHc['B']['TM']
    BHb = [x + CM.pm(rho['inf']) for x in pc]
    chB, chC = dict(chHc), dict(chHc)
    chB['L'] = Lb
    chB['B'] = {'TM': BHb, 'MB': mir(BHb)}
    hb = dict(chHc['h'])
    hb.update({'BH': BHb, 'AHm': [[ZERO] * K for _k in range(K)], 'cu': CM.pm(w_b)})
    chB['h'] = hb
    chC['h'] = dict(hb, BH=list(pc))
    return chB, chC


# ---- C-3: tau' and beta_H per piece
def tau_cert_c(n, P2row, q, vac, trb):
    """tau' (H-NORM's trace branch) as an upper end: eps_H rho_1^2 + TRB_H / (1 - delta)^2 - alpha_lo, delta S8's vac['delta'] for the
    piece, eps_H = c_N / J_lo, alpha_lo = (N-1)/2 - chi (1 + (N-1) t_max / 2) + chi^2 t_max / 2 at chi = ce_hi and t_max = 1/J_lo.
    Gates: D1 delta < 1; J1 chi < N - 1 and J2 chi < 1/t_max + (N-1)/2 (Jensen; alpha_lo's monotonicity over the piece); B3 chi < (N-1)/2
    - c_N/300; TR TRB_H/(1 - delta)^2 > alpha_lo; T0 tau' > 0."""
    tmax = CM.fr(1 / Fraction(P2row['jlo']))
    chi = CM.fr(q['ce_hi'])
    A_ = arb(n - 1) / 2
    cN = CM.fr(2 + Fraction((n - 1) * (n - 3), 8))
    rho1 = CM.fr(P2row['rho1_hi'])
    epsH = (cN * tmax).upper()
    alo = (A_ - chi * (1 + (n - 1) * tmax / 2) + chi * chi * tmax / 2).lower()
    dl = vac['delta'].upper()
    trp = (CM.fr(trb) / ((1 - dl) * (1 - dl))).upper()
    tau = (epsH * rho1 * rho1 + trp - alo).upper()
    gates = {'D1': bool(dl < 1), 'J1': bool(chi.upper() < n - 1), 'J2': bool(chi.upper() < (1 / tmax + A_).lower()),
             'B3': bool(chi.upper() < (A_ - cN / 300).lower()), 'TR': bool(trp.lower() > alo.upper()), 'T0': bool(tau.lower() > 0)}
    return tau, alo, trp, gates


def beta_h_c(n, q, trp):
    """beta_H = max((N-1)/2 - ce_lo, TRB_H / (1 - delta)^2) as an upper end (the review 19f74c2b (b), B-1)."""
    k_ = (arb(n - 1) / 2 - CM.fr(q['ce_lo'])).upper()
    return k_ if k_ > trp else trp


# ---- the two-chain pair form with S8's class-level branch (spec sect. 2)
def sf_pair2_rc_cert(cL, prmL, cR, prmR, dL, dR, kind, m, RkC, info=None):
    """sf_pair2_rc (pk24's RC pair form: boxes for the residual terms, centres for the main term, Euclidean W'-balls rho on RC's
    slots) plus S8's class-level mean-value branch: with C1 = t1 + ddet + lin and dz fixed upper ends over the box, Cov >= (Num_c - C1)/
    (|Z_c| + dz)^2 when Num_c - C1 >= 0 (|Z_c| - dz otherwise; the smaller of both when it straddles 0), Num_c and Z_c the duals of both
    sides' centres chains joined by _cen; the larger of this and the plain lower end is kept. cX = (chB, chC, rho, (chd, chm, rad, keys)).
    v1_1: C1 = t1 + ddet + lin is kept as a ball (s8core's sf_pair keeps C1 = t1 + ddet so; with lin = 0, RC's balls empty, the result
    is sf_pair's ball for ball, C-MIXED-REG); a side whose dual pair is None (thin chains: C-TARGET-H) gives the plain bound only; info
    also records k, sg and the centred balls of the class-level branch per denominator ('+dz', '-dz': C-MV-SF-H).
    Returns (v, cov_lo, num_lo, zhi, nAL, nl, nx, cov_hi, plain_lo, info)."""
    chLb, chLc, rhoL, dualL = cL
    chRb, chRc, rhoR, dualR = cR
    if (dualL is None) != (dualR is None):
        raise ValueError('C-DUAL-KEYS: one side of a pair carries a dual pair and the other none')
    if dualL is not None and (dualL[3] is not dualR[3] or len(dualL[2]) != len(dualR[2]) or len(dualL[2]) != len(dualL[3])):
        raise ValueError('C-DUAL-KEYS: the two sides of a pair carry different slot lists')
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
    zhi = (abs(Zc).upper() + dz).upper()
    zlo = (abs(Zc).lower() - dz).lower()
    if num_lo >= 0:
        cov_lo = (num_lo / (zhi * zhi)).lower()
    else:
        cov_lo = (num_lo / (zlo * zlo)).lower() if zlo > 0 else CM.NEGINF
    if num_hi >= 0:
        cov_hi = (num_hi / (zlo * zlo)).upper() if zlo > 0 else CM.POSINF
    else:
        cov_hi = (num_hi / (zhi * zhi)).upper()
    plain_lo = cov_lo
    inf_ = {'k': k, 't1': t1, 'ddet': ddet, 'lin': lin, 'dz': dz, 'C1': t1 + ddet + lin, 'Zc': Zc, 'numc': numc, 'plain_lo': plain_lo,
            'cl2': None, 'topc': None, 'sg': None, 'cen': {}}
    v = float((numc / (Zc * Zc)).mid())
    if dualL is not None:   # the class-level branch
        chLd, chLm, rad, keys = dualL
        chRd, chRm = dualR[0], dualR[1]
        if ('d', k) not in RkC:
            RkC[('d', k)] = CM.mpow(chLd['R'], k)
            RkC[('m', k)] = CM.mpow(chLm['R'], k)
        numd, Zd = cov2_2(chLd, chRd, dL, dR, kind, RkC[('d', k)])[:2]
        numm, Zm = cov2_2(chLm, chRm, dL, dR, kind, RkC[('m', k)])[:2]
        for q_ in (numd, Zd):
            if isinstance(q_, D) and len(q_.g) != len(rad):
                raise ValueError('C-DUAL-KEYS: a pair dual with %d slots on a box of %d' % (len(q_.g), len(rad)))
        C1 = inf_['C1']
        v = float((numm / (Zm * Zm)).mid())
        if Zc.lower() > 0 or Zc.upper() < 0:
            sg = ONE if Zc.lower() > 0 else -ONE
            topc = CM._cen(numd - C1, numm - C1, rad)
            inf_['topc'], inf_['sg'] = topc, sg

            def gl(dd, key):
                if not (abs(Zc).lower() + dd).lower() > 0:
                    inf_['cen'][key] = None
                    return None
                cb = CM._cen((numd - C1) / ((sg * Zd + dd) * (sg * Zd + dd)), (numm - C1) / ((sg * Zm + dd) * (sg * Zm + dd)), rad)
                inf_['cen'][key] = cb
                return cb.lower()
            if topc.lower() >= 0:
                cl2 = gl(dz, '+dz')
            elif topc.upper() <= 0:
                cl2 = gl(-dz, '-dz')
            else:
                gp, gm = gl(dz, '+dz'), gl(-dz, '-dz')
                cl2 = None if (gp is None or gm is None) else (gp if gp < gm else gm)
            inf_['cl2'] = cl2
            if cl2 is not None and cl2 > cov_lo:
                cov_lo = cl2
    nAL = CM.hyp(ALW + dAL, ALp)
    nl = CM.hyp(nL1 + e1L, rn1L[dL])
    nx = CM.hyp(nLX + eXL, rnXL[dL])
    if info is not None:
        info.update(inf_)
    return v, cov_lo, num_lo, zhi, nAL, nl, nx, cov_hi, plain_lo, inf_


def row_of(fam, key, b):
    """(family, class key, headroom, certified lower end, centre value, upper end, pair-form record)."""
    return (fam, key, CM.head(b[0], b[1]), b[1], b[0], b[7], b[9])


def s1_rows_c(cL, prmL, cR, prmR, dL, kind, RkC, ftyp, DFx, mi0, mf0, tag):
    """s1_rows_rc on the certified pair form: the inf rows (Minf) and the one-end-far rows (M1; routes A and B, the larger lower end)."""
    rows = []
    for m in range(1, CM.MM + 1):
        need_inf, need_far = (mi0 is None or m < mi0), (mf0 is None or m < mf0)
        if not (need_inf or need_far):
            continue
        base = sf_pair2_rc_cert(cL, prmL, cR, prmR, dL, 'inf', kind, m, RkC)
        if need_inf:
            rows.append(row_of('Minf', (tag, dL, 'inf', kind, m), base))
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
                b = sf_pair2_rc_cert(cL, prmL, cR, prmR, dL, DFx + j, kind, m, RkC)
                loB = b[1] if b[1] < loB else loB
            lo1 = lo1 if lo1 > loB else loB
        rows.append(('M1', (tag, dL, 'far', kind, m), CM.head(fa[0], lo1), lo1, fa[0], None, None))
    return rows


def rows_mixed_c(cH, prmH_, cV, prmV):
    """the MIXED rows on the certified pair form (rows_mixed_rc with n >= 5): HV two-sided (M2), HV and VH at infinity (Minf) and far (M1);
    m0 per class from dk_class2 on the boxes."""
    chB, chVb = cH[0], cV[0]
    RkC = {}
    dk = CM.dk_setup(chVb, prmV)
    m0 = {}
    rows = []
    mz = lambda r_: (r_[0] + 1) if r_[0] is not None else None
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            for dV in NEAR_V:
                m0[('M2', ('HV', iH, dV, kind))] = mz(dk_class2(chB, prmH_, chVb, prmV, dk, iH, dV, kind))
            m0[('Minf', ('HV', iH, 'inf', kind))] = mz(dk_class2(chB, prmH_, chVb, prmV, dk, iH, 'inf', kind))
            m0[('M1', ('HV', iH, 'far', kind))] = mz(dk_class2(chB, prmH_, chVb, prmV, dk, iH, 'far', kind, ('V', DF_V)))
        for dV in NEAR_V:
            m0[('Minf', ('VH', dV, 'inf', kind))] = mz(dk_class2(chVb, prmV, chB, prmH_, dk, dV, 'inf', kind))
            m0[('M1', ('VH', dV, 'far', kind))] = mz(dk_class2(chVb, prmV, chB, prmH_, dk, dV, 'far', kind, ('H', DF_H)))
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            for dV in NEAR_V:
                mm0 = m0[('M2', ('HV', iH, dV, kind))]
                for m in range(1, CM.MM + 1):
                    if iH + dV + m + 3 < 5 or (mm0 is not None and m >= mm0):
                        continue
                    rows.append(row_of('M2', ('HV', iH, dV, kind, m), sf_pair2_rc_cert(cH, prmH_, cV, prmV, iH, dV, kind, m, RkC)))
            rows += s1_rows_c(cH, prmH_, cV, prmV, iH, kind, RkC, 'V', DF_V, m0[('Minf', ('HV', iH, 'inf', kind))],
                              m0[('M1', ('HV', iH, 'far', kind))], 'HV')
        for dV in NEAR_V:
            rows += s1_rows_c(cV, prmV, cH, prmH_, dV, kind, RkC, 'H', DF_H, m0[('Minf', ('VH', dV, 'inf', kind))],
                              m0[('M1', ('VH', dV, 'far', kind))], 'VH')
    return rows, m0


def rows_h_c(cH, prm):
    """the FLIP/SAME rows on the certified pair form (rows_h_rc with n >= 5, every slot of DN: F-b): H2 two-sided, Hinf, H1 (routes A
    and B); m0 per class from dk_class and dk_class_h on the boxes."""
    chB = cH[0]
    RkC = {}
    dkf = CM.dk_setup(chB, prm)
    m0 = {}
    rows = []
    for kind in ('flip', 'same'):
        for dL in DN[kind]:
            r_ = CM.dk_class(chB, prm, dkf, dL, 'inf', kind)
            m0[('Hinf', (dL, 'inf', kind))] = (r_[0] + 1) if r_[0] is not None else None
            r_ = dk_class_h(chB, prm, dkf, dL, 'far', kind)
            m0[('H1', (dL, 'far', kind))] = (r_[0] + 1) if r_[0] is not None else None
            for dR in DN[kind]:
                r_ = CM.dk_class(chB, prm, dkf, dL, dR, kind)
                m0[('H2', (dL, dR, kind))] = (r_[0] + 1) if r_[0] is not None else None
    for kind in ('flip', 'same'):
        for dL in DN[kind]:
            for dR in DN[kind]:
                mm0 = m0[('H2', (dL, dR, kind))]
                for m in range(1, CM.MM + 1):
                    if dL + dR + m + 3 < 5 or (mm0 is not None and m >= mm0):
                        continue
                    rows.append(row_of('H2', (dL, dR, kind, m), sf_pair2_rc_cert(cH, prm, cH, prm, dL, dR, kind, m, RkC)))
            mm0 = m0[('Hinf', (dL, 'inf', kind))]
            mf0 = m0[('H1', (dL, 'far', kind))]
            for m in range(1, CM.MM + 1):
                need_inf, need_far = (mm0 is None or m < mm0), (mf0 is None or m < mf0)
                if not (need_inf or need_far):
                    continue
                base = sf_pair2_rc_cert(cH, prm, cH, prm, dL, 'inf', kind, m, RkC)
                if need_inf:
                    rows.append(row_of('Hinf', (dL, 'inf', kind, m), base))
                if not need_far:
                    continue
                fa = far_lo2_h(cH[0], prm, dL, kind, m, base, DF[kind])
                loA = fa[1]
                loB = far_lo2_h(cH[0], prm, dL, kind, m, base, DF[kind] + 3)[1]
                for j in (0, 1, 2):
                    b = sf_pair2_rc_cert(cH, prm, cH, prm, dL, DF[kind] + j, kind, m, RkC)
                    loB = b[1] if b[1] < loB else loB
                lo1 = loA if loA > loB else loB
                rows.append(('H1', (dL, 'far', kind, m), CM.head(fa[0], lo1), lo1, fa[0], None, None))
    return rows, m0


# ---- one piece
def dual_own(cX, other=None):
    """C-DUAL-OWN on one side cX = (chB, chC, rho, (chd, chm, rad, keys)): its dual pair's midpoint run reproduces the side's own centred
    slot-0 and slot-1 states (chm's components inside chC's, slack 2^-20 of the radius) and chd's value balls hold chC's. other: a dual
    pair in the side's place (PLANT-DUAL-SWAP)."""
    chd, chm, rad, keys = cX[3] if other is None else other
    chC = cX[1]
    ok = True
    for i in (0, 1):
        for part in (0, 1):
            cc, mm, dd = chC['L'][i][part], chm['L'][i][part], chd['L'][i][part]
            pairs = [(cc[0], mm[0], dd[0])] + list(zip(cc[1], mm[1], dd[1]))
            for c_, m_, d_ in pairs:
                dv = d_.v if isinstance(d_, D) else d_
                if not (mod.inside_r(c_, m_) and mod.inside_r(dv, c_)):
                    ok = False
    return ok


def h_build(n, A, r, HE, q, trb, T, vac, zero_bars=False, zero_tgrad=False, fixed=None, tau_ovr=None):
    """the chains of one run on the box T (v1's eval_piece body): S8's W3 chain rerun on the combined entry box (duals and midpoints,
    piece_eval_RB's basis C0 and route (b)'s leak), its setup, the piece constants (c_fix, tau' with its gates, beta_H; fixed: another
    run's, reused), pc_H and pn_SH4, the horizontal chain in both passes, RC's radii once from this run's centred chain, RC's
    centres in both passes, the centred chain, the boxes and the RC setup. vac: the vacuum of this run (C-MV-H: delta 0). tau_ovr:
    tau' replaced in the chain only, pn_SH4 kept (PLANT-RCC, as rcm6's PLANT-RC)."""
    mains, odd = A['mains'][n], A['odd'][n]
    C0, leak, Uh, P2row = r['C0'], r['leak'], r['Uh'], r['P2row']
    keys, VdV, VmV, VdH, VmH, rad = comb_duals(r['Ech'], HE, T, zero_bars, zero_tgrad)
    chd_V = CM.chain(VdV, mains, odd, vac, C0, tt=False)
    chm_V = CM.chain(VmV, mains, odd, vac, C0, allow=chd_V['allow'], par=chd_V['par_exact'], tt=False)
    chc_V = CM._cen(chd_V, chm_V, rad)
    chU = dict(chc_V, Gl=leak['Gl'])
    P2r = {k: CM.fr(P2row[k]) for k in ('Bp_hi', 'Bm_hi', 'Rw_hi', 'rho1_hi')}
    prmV = CM.setup(chU, P2r, Uh, vac, Gl=leak['Gl'], sblk=leak['sblk'])
    if fixed is None:
        cfix = Fraction(int(round(float((q['ce_lo'] + q['ce_hi']) / 2) * 10 ** 9)), 10 ** 9)
        tau_b, alo, trp, gts = tau_cert_c(n, P2row, q, vac, trb[n])
        bH = mod.up_frac(beta_h_c(n, q, trp))   # an exact rational upper end (the ported setups take beta_H through CM.fr)
    else:
        cfix, tau_b, alo, trp, gts, bH = (fixed[k_] for k_ in ('cfix', 'tau', 'alo', 'trp', 'gates0', 'bH'))
    w_b = CM.fr(q['ce_hi'] - q['ce_lo'])
    pcH = (CM.fr(q['Qvt_hi']) + w_b * vac['sp']).upper()
    kapS = (arb(n - 1) / 2 - CM.fr(q['ce_lo'])).upper()
    pn_b = CM.sqrt_up((kapS * tau_b).upper())
    if tau_ovr is not None:
        tau_b = tau_ovr
    kap = CM.fr(Fraction(n - 1, 2) - cfix)
    chHd0 = chain_h_c(VdV, VdH, chd_V, mains, vac, cfix)
    chHm0 = chain_h_c(VmV, VmH, chm_V, mains, vac, cfix)
    chHc0 = CM._cen(chHd0, chHm0, rad)
    rho, r_u = rc_radii(chHc0, prmV, tau_b, bH, vac, w_b, pn_b, kap)
    cen_d, pc_d = rc_centres(chHd0, tau_b, kap)
    cen_m, pc_m = rc_centres(chHm0, tau_b, kap)
    chHd = rc_apply(chHd0, cen_d, pc_d, r_u)
    chHm = rc_apply(chHm0, cen_m, pc_m, r_u)
    chHc = CM._cen(chHd, chHm, rad)
    chB, chC = rc_boxes(chHc, rho, w_b)
    prmH = rc_setup_m(chB, chHc, prmV, bH, tau_b, pcH, vac, pn_b)
    dualH, dualV = (chHd, chHm, rad, keys), (chd_V, chm_V, rad, keys)
    return {'keys': keys, 'rad': rad, 'chd_V': chd_V, 'chm_V': chm_V, 'chc_V': chc_V, 'chU': chU, 'prmV': prmV, 'cfix': cfix,
            'tau': tau_b, 'alo': alo, 'trp': trp, 'gates0': gts, 'bH': bH, 'w_b': w_b, 'pcH': pcH, 'pn': pn_b, 'kap': kap, 'chHd': chHd,
            'chHm': chHm, 'chHc': chHc, 'chB': chB, 'chC': chC, 'prmH': prmH, 'rho': rho, 'r_u': r_u,
            'cH': (chB, chC, rho, dualH), 'cV': (chU, chU, {}, dualV)}


def eval_piece(n, A, i, HE, HZ, trb, T=None, zero_bars=False, zero_tgrad=False, pkw=None, tau_ovr=None, rows=True):
    """piece i on its box (or on the ball T): S8's piece (route (b), first set with tau_B > 0; pkw: piece_eval_RB's C0, vac, Uh, bases
    and C0B of a parent, C-PIECE-H), the chains of h_build, the gates, and (rows) every FLIP/SAME and MIXED row with its top-mode
    thresholds. None when S8 gives no bound on the piece."""
    r = mod.piece_eval_RB(n, A, i, T=T, rows=False, **(pkw or {}))
    if r is None:
        return None
    q = HZ[i]
    hb = h_build(n, A, r, HE, q, trb, r['T'], r['vac'], zero_bars, zero_tgrad, tau_ovr=tau_ovr)
    ref = dict(CM.leaves(r['chW']))
    rerun_bad = [p for p, v in CM.leaves(hb['chc_V']) if p in ref and not (v.upper() >= ref[p].lower() and ref[p].upper() >= v.lower())]
    cH, cV, keys = hb['cH'], hb['cV'], hb['keys']
    gts = dict(hb['gates0'])
    gts.update({'CIN': bool(q['ce_lo'] <= hb['cfix'] <= q['ce_hi']),
                'PAREXACT': bool(hb['chd_V']['par_exact'] is True and r['ch']['par_exact'] is True),
                'VRERUN': not rerun_bad, 'KEYS': keys_ok(cH[3], keys) and keys_ok(cV[3], keys), 'OWN': dual_own(cH)})
    rowsH, m0H = rows_h_c(cH, hb['prmH']) if rows else ([], {})
    rowsM, m0M = rows_mixed_c(cH, hb['prmH'], cV, hb['prmV']) if rows else ([], {})
    m0 = dict(m0H)
    m0.update(m0M)
    return {'r': r, 'hb': hb, 'T': r['T'], 'vac': r['vac'], 'cH': cH, 'cV': cV, 'prmH': hb['prmH'], 'prmV': hb['prmV'],
            'rows': rowsH + rowsM, 'm0': m0, 'gates': gts, 'tau': hb['tau'], 'alo': hb['alo'], 'trp': hb['trp'], 'bH': hb['bH'],
            'cfix': hb['cfix'], 'pcH': hb['pcH'], 'pn': hb['pn'], 'rho': hb['rho'], 'keys': keys, 'rerun_bad': rerun_bad}


# ---- v1_1: sect. 2's checks on the horizontal chain (S8's family: C-UNIF, C-MV, C-MV-BAR, C-TARGET, C-MV-SF, C-PIECE)
def h_thin(n, A, r, hb, HE, t, v, emode, bars, store=None):
    """one thin point chain of the horizontal chain at t, on the run hb's allowance box and parity decision (its vertical dual run's
    allow and par_exact, as S8's on_dual) and constants (c_fix, tau', kappa, r_u): S8's W3 entries and the ten entries at t with every
    coefficient in mode emode (entry_thin) and, with bars, every bar offset at the same corner (ent_thin_bar); the vertical chain, the
    horizontal chain and RC's centres. Run inside s8core's end_chain, so every wrapped allowance (the place-2 allowance, the u-ball r_u)
    sits at a point of its ball and delta at the stand-in's point. store: (horizontal, vertical) thin chains appended."""
    ef = mod.ent_thin_bar if bars else mod.entry_thin
    EV, EH = ef(r['Ech'], t, emode), ef(HE, t, emode)
    chV = CM.chain(EV, A['mains'][n], A['odd'][n], v, r['C0'], allow=hb['chd_V']['allow'], par=hb['chd_V']['par_exact'], tt=False)
    chH0 = chain_h_c(EV, EH, chV, A['mains'][n], v, hb['cfix'])
    cen, pc = rc_centres(chH0, hb['tau'], hb['kap'])
    chH = rc_apply(chH0, cen, pc, hb['r_u'])
    if store is not None:
        store.append((chH, chV))
    return chH


def unif_h(n, A, i, HE):
    """C-UNIF-H on piece i: the ten entries' bar-free enclosures over the piece's t-box contain their thin values (every coefficient at
    its span's midpoint, upper or lower end) at the piece's 9 sample t, under S8's unif_ok. Returns the failing entry names."""
    P2row = A['pieces'][n][i]
    T = CM.tball(P2row['jlo'], P2row['jhi'])
    enc = CM.entry_points(HE, T)
    return sorted(set(k for t in CM.tpoints(P2row['jlo'], P2row['jhi']) for mode in mod.END_MODES
                      for k, v in mod.entry_thin(HE, t, mode).items() if not mod.unif_ok(enc[k], v)))


def mv_h(n, A, ev, HE, HZ, trb, zero_tgrad=False):
    """C-MV-H on an evaluated piece ev: the centred horizontal chain of a run with zero bars and delta 0 (the piece's constants; its own
    allowance box and r_u) contains the thin point chains at the piece's 9 sample t in END_MODES (zero bars, delta at the stand-in 0),
    leaf by leaf under inside_r's 2^-20 rule, as S8's mv_piece. zero_tgrad: PLANT-MV-H. Returns (leaves, failing leaf paths)."""
    r = ev['r']
    i = r['i']
    P2row = A['pieces'][n][i]
    vac0 = dict(r['vac'], delta=arb(0))
    hb0 = h_build(n, A, r, HE, HZ[i], trb, r['T'], vac0, zero_bars=True, zero_tgrad=zero_tgrad, fixed=ev['hb'])
    cl = dict(CM.leaves(hb0['chHc']))
    pt = lambda t, v, emode: h_thin(n, A, r, hb0, HE, t, v, emode, False)
    bad = set()
    for t in CM.tpoints(P2row['jlo'], P2row['jhi']):
        for mode in mod.END_MODES:
            ch, hits, nw, na = mod.end_chain(pt, t, vac0, 1, mode)
            if hits != 1:
                bad.add('(stand-in met %d times)' % hits)
            bad |= set(p for p, v in CM.leaves(ch) if p not in cl or not mod.inside_r(cl[p], v))
    return len(cl), sorted(bad)


def mvbar_h(n, A, ev, HE, HZ, trb, plant=False, keep=False):
    """C-MV-BAR-H on an evaluated piece ev: its own centred horizontal chain (with the entries' bars and the piece's vacuum) contains the
    thin point chains at the 9 sample t with every coefficient and bar offset at a corner (ent_thin_bar), delta at _corner's point and
    every wrapped allowance in the same mode (end_chain), leaf by leaf under the 2^-20 rule, as S8's mvbar_piece. plant (PLANT-MV-BAR-H):
    the same points on a zero-bar run's allowance box against that run's centred chain, which must fail in modes 1 and -1. keep: the
    thin chains are returned in res['thin'] = [(index of t, mode, horizontal, vertical)]. Returns {'leaves', 'fail', 'bym', 'hits'}."""
    r = ev['r']
    i = r['i']
    P2row = A['pieces'][n][i]
    vac = r['vac']
    hb = h_build(n, A, r, HE, HZ[i], trb, r['T'], vac, zero_bars=True, fixed=ev['hb']) if plant else ev['hb']
    cl = dict(CM.leaves(hb['chHc']))
    res = {'hits': set(), 'bym': {m: 0 for m in mod.END_MODES}, 'thin': []}
    bad = set()
    for it, t in enumerate(CM.tpoints(P2row['jlo'], P2row['jhi'])):
        for mode in mod.END_MODES:
            st = []
            vx, sg = mod._corner(vac, mode)
            ch, hits, nw, na = mod.end_chain(lambda t_, v, emode: h_thin(n, A, r, hb, HE, t_, v, emode, True, st), t, vx, sg, mode)
            res['hits'].add(hits)
            b_ = set(p for p, v in CM.leaves(ch) if p not in cl or not mod.inside_r(cl[p], v))
            bad |= b_
            res['bym'][mode] += len(b_)
            if keep:
                res['thin'].append((it, mode, st[0][0], st[0][1]))
    res['leaves'], res['fail'] = len(cl), sorted(bad)
    return res


SFH_PICK = (3, 3)   # C-TARGET-H and C-MV-SF-H: the 3 FLIP/SAME and the 3 MIXED pair-form rows of smallest headroom on the piece


def pair_args(ev, fam, key, cH=None, cV=None):
    """the pair-form call of a row (H2, Hinf, M2, Minf): (cL, prmL, cR, prmR, dL, dR, kind, m), on the sides cH, cV (default: ev's)."""
    cH = ev['cH'] if cH is None else cH
    cV = ev['cV'] if cV is None else cV
    pH, pV = ev['prmH'], ev['prmV']
    if fam in ('H2', 'Hinf'):
        return (cH, pH, cH, pH) + tuple(key)
    if key[0] == 'HV':
        return (cH, pH, cV, pV) + tuple(key[1:])
    return (cV, pV, cH, pH) + tuple(key[1:])


def target_h(ev, mb, c1_scale=None):
    """C-TARGET-H and C-MV-SF-H on the piece's SFH_PICK pair-form rows of smallest headroom, with mvbar_h's thin chains (keep=True):
    - C-MV-SF-H: where the class-level branch is active, Num_t - C1 and (Num_t - C1)/(sg Z_t + dd)^2 at each of the 27 thin chains (Num_t,
      Z_t from cov2_2 on both sides' thin centres) lie in the box's centred balls (topc; '+dz', '-dz'), under the 2^-20 rule, with the
      box's C1, dz and sg;
    - C-TARGET-H: the box's C1 and dz >= the pair form's own C1 and dz on the thin chains (both sides: RC's boxes around the thin centres
      with the box's rho, and the box's prm) at the 3 sample t (the box ends and the centre) x END_MODES, box >= target (1 - 1e-10); and
      (v1_2) each row's certified [lo, hi] holds its centres' value Num_t / Z_t^2 at each of the 27 thin chains (the rows against thin
      points; lo <= Num_t / Z_t^2 follows from num_lo <= Num_t and |Z_t| <= |Z| + dz, and from C-MV-SF-H for the class-level end).
    c1_scale: the box C1 multiplied by it in C-TARGET-H (PLANT-TARGET-H). Returns a dict of counts and failures."""
    hb = ev['hb']
    res = {'classes': 0, 'active': 0, 'points': 0, 'fail': [], 'tchecks': 0, 'tfail': [], 'tworst': 0.0, 'vchecks': 0, 'vfail': []}
    pick = []
    for fams, nn in ((('H2', 'Hinf'), SFH_PICK[0]), (('M2', 'Minf'), SFH_PICK[1])):
        rows = sorted((x for x in ev['rows'] if x[0] in fams and x[6] is not None), key=lambda x: x[2])
        pick += [(x[0], x[1]) for x in rows[:nn]]
    thin = []
    for it, mode, chHt, chVt in mb['thin']:
        bt, ct = rc_boxes(chHt, hb['rho'], hb['w_b'])
        thin.append((it, mode, (bt, ct, hb['rho'], None), (chVt, chVt, {}, None)))
    RkT = {}
    for fam, key in pick:
        a = pair_args(ev, fam, key)
        info = {}
        bb = sf_pair2_rc_cert(*a, {}, info=info)
        res['classes'] += 1
        k, C1, dz = info['k'], info['C1'], info['dz']
        dL, dR, kind, m = a[4:]
        for j, (it, mode, cHt, cVt) in enumerate(thin):
            at = pair_args(ev, fam, key, cH=cHt, cV=cVt)
            Lc, Rc = at[0][1], at[2][1]
            if (j, k) not in RkT:
                RkT[j, k] = CM.mpow(Lc['R'], k)
            numt, Zt = cov2_2(Lc, Rc, dL, dR, kind, RkT[j, k])[:2]
            vt = numt / (Zt * Zt)
            res['vchecks'] += 1
            if not (vt.upper() >= bb[1] and (bb[7] is None or vt.lower() <= bb[7])):
                res['vfail'].append('%s %s' % (fam, key))
            if info['topc'] is not None:
                res['points'] += 1
                bad = [] if mod.inside_r(info['topc'], numt - C1) else ['Num - C1']
                for dk_, dd in (('+dz', dz), ('-dz', -dz)):
                    cb = info['cen'].get(dk_)
                    if cb is not None and not mod.inside_r(cb, (numt - C1) / ((info['sg'] * Zt + dd) * (info['sg'] * Zt + dd))):
                        bad.append(dk_)
                if bad:
                    res['fail'].append(('%s %s' % (fam, key), '/'.join(bad)))
            if it not in (0, 4, 8):
                continue
            itn = {}
            sf_pair2_rc_cert(*at, {}, info=itn)
            c1b = C1 * arb(c1_scale) if c1_scale is not None else C1
            for nm, bx, tg in (('C1', c1b, itn['C1']), ('dz', dz, itn['dz'])):
                res['tchecks'] += 1
                b_, g_ = float(bx.upper()), float(tg.upper())
                res['tworst'] = max(res['tworst'], g_ / b_ if b_ > 0 else (0.0 if g_ <= 0 else float('inf')))
                if not (g_ * (1 - 1e-10) <= b_):
                    res['tfail'].append('%s %s %s' % (fam, key, nm))
        if info['topc'] is not None:
            res['active'] += 1
    return res


def halves_h(n, A, i, HE, HZ, trb, collapse=False):
    """C-PIECE-H on piece i: each half of its t-box, with the parent's basis C0, vacuum, U and trial set (piece_eval_RB's), has every
    common row's certified lower end not below the parent's (S8's lo_not_lower, slack 2^-20 |lo|), every top-mode m0 no larger, and
    every gate passing; the horizontal chain's leaves against the parent's are INFO (as S8's C-PIECE). collapse: the parent's box
    replaced by its right end in J (PLANT-PIECE-H). Returns (leaves, failing leaves, failing rows, largest excess of a failing leaf)."""
    par = eval_piece(n, A, i, HE, HZ, trb)
    r = par['r']
    T = r['T']
    pkw = {'C0': r['C0'], 'vac': r['vac'], 'Uh': r['Uh'], 'bases': (r['basis'],), 'C0B': r['C0B']}
    if collapse:
        par = eval_piece(n, A, i, HE, HZ, trb, T=arb(T.lower()), pkw=pkw)
    pl = dict(CM.leaves(par['hb']['chHc']))
    prow = {(x[0], str(x[1])): x[3] for x in par['rows']}
    pm0 = par['m0']
    mid = arb(T.mid())
    bad_l, bad_r, xl = set(), set(), 0.0
    for Th in (T.lower().union(mid), mid.union(T.upper())):
        hf = eval_piece(n, A, i, HE, HZ, trb, T=Th, pkw=pkw)
        if hf is None:
            bad_r.add('no bound on a half')
            continue
        for p, v in CM.leaves(hf['hb']['chHc']):
            if p not in pl or not mod.inside_r(pl[p], v, mod.RSLACK, arb('1e-20')):
                bad_l.add(p)
                if p in pl:
                    o = pl[p]
                    ex = max(float((v.upper() - o.upper()).mid()), float((o.lower() - v.lower()).mid()))
                    xl = max(xl, ex / float(o.rad()) if o.rad() > 0 else float('inf'))
        for x in hf['rows']:
            pv_ = prow.get((x[0], str(x[1])))
            if pv_ is not None and not mod.lo_not_lower(x[3], pv_):
                bad_r.add('%s %s' % (x[0], x[1]))
        for g_, ok_ in hf['gates'].items():
            if not ok_:
                bad_r.add('gate %s' % g_)
        for k_, v_ in hf['m0'].items():
            if pm0.get(k_) is not None and (v_ is None or v_ > pm0[k_]):
                bad_r.add('m0 %s' % (k_,))
    return len(pl), sorted(bad_l), sorted(bad_r), xl


def checks_h(n, A, ev, HE, HZ, trb, full=True, tag=''):
    """the checks of sect. 2 at one evaluated piece, as lines: C-UNIF-H and C-MV-H always; with full, C-MV-BAR-H, C-TARGET-H and
    C-MV-SF-H too. Gates through gate(). Returns mvbar_h's result (full) or None."""
    i = ev['r']['i']
    bu = unif_h(n, A, i, HE)
    nl, bm = mv_h(n, A, ev, HE, HZ, trb)
    out('C-UNIF-H N=%d piece %d%s (the ten entries\' enclosures over the box against thin values at 9 t x END_MODES): failing %s -> %s; '
        'C-MV-H (zero bars, delta 0: the centred horizontal chain against thin point chains at 9 t x END_MODES): %d leaves, failing %d%s '
        '-> %s' % (n, i, tag, bu or 'none', gate('C-UNIF-H', not bu), nl, len(bm), (' (%s)' % ', '.join(bm[:4])) if bm else '',
                   gate('C-MV-H', not bm)))
    if not full:
        return None
    mb = mvbar_h(n, A, ev, HE, HZ, trb, keep=True)
    once = mb['hits'] == {1}
    out('C-MV-BAR-H N=%d piece %d%s (the piece\'s centred horizontal chain against thin points at 9 t with every bar offset, coefficient, '
        'wrapped allowance and delta at its midpoint, upper or lower end; the stand-in met %s): %d leaves, failing %d%s -> %s' % (
            n, i, tag, 'once in every chain' if once else '%s times' % sorted(mb['hits']), mb['leaves'], len(mb['fail']),
            (' (%s)' % ', '.join(mb['fail'][:4])) if mb['fail'] else '', gate('C-MV-BAR-H', not mb['fail'] and once)))
    d = target_h(ev, mb)
    out('C-MV-SF-H N=%d piece %d%s (the class-level balls of the %d FLIP/SAME and %d MIXED pair-form rows of smallest headroom against the '
        '27 thin chains): %d classes, %d active, %d points, failing %d%s -> %s; C-TARGET-H (the box\'s C1 and dz against the pair form\'s own '
        'on the thin chains at 3 t x 3 modes: %d checks, largest target/box %.4f, failing %d%s; the rows\' certified [lo, hi] against their '
        'centres\' values at the 27 thin chains: %d checks, failing %d%s) -> %s' % (
            n, i, tag, SFH_PICK[0], SFH_PICK[1], d['classes'], d['active'], d['points'], len(d['fail']),
            (' (%s)' % ', '.join('%s: %s' % x for x in d['fail'][:3])) if d['fail'] else '', gate('C-MV-SF-H', not d['fail']),
            d['tchecks'], d['tworst'], len(d['tfail']), (' (%s)' % ', '.join(sorted(set(d['tfail']))[:3])) if d['tfail'] else '',
            d['vchecks'], len(d['vfail']), (' (%s)' % ', '.join(sorted(set(d['vfail']))[:3])) if d['vfail'] else '',
            gate('C-TARGET-H', not d['tfail'] and not d['vfail'])))
    return mb


# ---- v1_1: the harmonic limit on this engine's chain, P2-13's n = 5 values, the pair form's regression
def harm_rcc(ev0):
    """C-HARM-RCC on the certified chain evaluated at t = 0 (ev0): every MIXED class of harm_check_rc (HV two-sided at n = 5..8, HV and
    VH at infinity, m = 1..8) and every FLIP/SAME class (two-sided at n = 5..8 over DN, inf, m = 1..8): the harmonic value (harm_m,
    harm) lies in [cov_lo, cov_hi] of sf_pair2_rc_cert (slack 1e-12 relative). Returns (classes, failing, the largest lo / harmonic)."""
    cH, cV, prmH, prmV = ev0['cH'], ev0['cV'], ev0['prmH'], ev0['prmV']
    RkC, rows = {}, []
    for kind in ('same', 'flip'):
        cls = []
        for iH in NEAR_H:
            cls += [('HV', iH, dV, kind, m) for dV in NEAR_V for m in range(1, 9) if iH + dV + m + 3 in (5, 6, 7, 8)]
            cls += [('HV', iH, 'inf', kind, m) for m in range(1, 9)]
        for dV in NEAR_V:
            cls += [('VH', dV, 'inf', kind, m) for m in range(1, 9)]
        for (tg, a_, b_, k_, m_) in cls:
            if tg == 'HV':
                bb = sf_pair2_rc_cert(cH, prmH, cV, prmV, a_, b_, k_, m_, RkC)
            else:
                bb = sf_pair2_rc_cert(cV, prmV, cH, prmH, a_, b_, k_, m_, RkC)
            rows.append(((tg, a_, b_, k_, m_), bb, harm_m(tg, a_, b_, k_, m_)))
    for kind in ('flip', 'same'):
        for iL in DN[kind]:
            cls = [(iL, iR, kind, m) for iR in DN[kind] for m in range(1, 9) if iL + iR + m + 3 in (5, 6, 7, 8)] + \
                  [(iL, 'inf', kind, m) for m in range(1, 9)]
            for (a_, b_, k_, m_) in cls:
                bb = sf_pair2_rc_cert(cH, prmH, cH, prmH, a_, b_, k_, m_, RkC)
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


def repro_rc5(ev, img, pv, plant=False):
    """C-REPRO-RC5 on the first piece (ev): for each of the 18 n = 5 keys, P2-13's exact float value (its PAIR line's Cov*J^2 a_k) at
    the box's ends and centre lies in the key's certified [lo, hi]. plant (PLANT-REPRO-RC5): each exact value replaced by hi + |hi|/100.
    Returns (keys with a row, failing keys, lines)."""
    T = ev['T']
    tfs = [float(T.lower()), float(T.mid()), float(T.upper())]
    have = {(x[0], tuple(x[1])): x for x in ev['rows']}
    n5c, n5b, lines = 0, [], []
    for k5 in N5KEYS:
        kk = (k5[0], tuple(k5[1]))
        key = n5key(*kk)
        x = have.get(kk)
        if x is None:
            n5b.append('%s: no row' % key)
            continue
        ck = img.get(key)
        if ck is None or ck not in pv:
            n5b.append('%s: no P2-13 value' % key)
            continue
        lo5, hi5 = float(x[3].mid()), float(x[5].mid())
        exs = [hi5 + abs(hi5) / 100.0] if plant else [sum(c_ * tf ** j for j, c_ in enumerate(pv[ck])) for tf in tfs]
        ok5 = all(lo5 <= e_ <= hi5 for e_ in exs)
        n5c += 1
        if not ok5:
            n5b.append(key)
        lines.append('N5REPRO %s %s (P2-13 %s, class %s): exact %s, centre %.9e, certified [%.6e, %.6e] -> %s' % (
            kk[0], kk[1], key, ck, ' '.join('%.9e' % e_ for e_ in exs), x[4], lo5, hi5, 'inside' if ok5 else 'OUTSIDE'))
    return n5c, n5b, lines


def mixed_reg_c(ev, plant=False):
    """C-MIXED-REG on the certified pair form (spec sect. 8; kt_s8hf_v2's (b)-(d) on this engine's form): with the centred vertical chain
    and its prm on both sides (RC's balls empty, the vertical dual pair, copies on the right), sf_pair2_rc_cert against s8core's sf_pair
    with the same dual pair (parity off; this form has no parity branch), ball for ball over every S8 class (DNEAR, near and inf, m <=
    MM): (b); dk_class2 against dk_class (near, inf, far with S8's DFAR): (c); far_lo2 on both bases: (d). plant (PLANT-MIXED-REG): the
    right chain's slot-0 insertion vector + 1e-9, which must break (b). Returns (comparisons, mismatches)."""
    chU, prmV, dualV = ev['cV'][0], ev['prmV'], ev['cV'][3]
    chUd = dict(chU, dual=(dualV[0], dualV[1], dualV[2]))
    chR = dict(chU)
    if plant:
        L_ = dict(chU['L'])
        l0, x0 = L_[0]
        L_[0] = (l0, (x0[0] + arb('1e-9'), list(x0[1])))
        chR['L'] = L_
    cL_, cR_ = (chU, chU, {}, dualV), (chR, chR, {}, dualV)
    prmR = dict(prmV)
    dk = CM.dk_setup(chU, prmV)
    R1, R2 = {}, {}
    eq = lambda x, y: len(x) == len(y) and all(same_val(p_, q_) for p_, q_ in zip(x, y))
    ncmp, bad = 0, []
    for kind in ('flip', 'same'):
        for dL in CM.DNEAR[kind]:
            for dR in list(CM.DNEAR[kind]) + ['inf']:
                for m in range(1, CM.MM + 1):
                    s8b = CM.sf_pair(chUd, prmV, dL, dR, kind, m, R1, parity=False)
                    v2b = sf_pair2_rc_cert(cL_, prmV, cR_, prmR, dL, dR, kind, m, R2)
                    ncmp += 1
                    if not eq(tuple(s8b), tuple(v2b[:8])):
                        bad.append(('b', dL, dR, kind, m))
                    if dR == 'inf' and not plant:
                        ncmp += 1
                        if not eq(CM.far_lo2(chUd, prmV, dL, kind, m, s8b, CM.DFAR[kind]),
                                  CM.far_lo2(None, prmV, dL, kind, m, v2b, CM.DFAR[kind])):
                            bad.append(('d', dL, dR, kind, m))
            if plant:
                continue
            for dR in list(CM.DNEAR[kind]) + ['inf', 'far']:
                ncmp += 1
                if not eq(CM.dk_class(chU, prmV, dk, dL, dR, kind), dk_class2(chU, prmV, chU, prmV, dk, dL, dR, kind, ('V', CM.DFAR[kind]))):
                    bad.append(('c', dL, dR, kind))
    return ncmp, bad


def n_of(fam, key):
    """n of a two-sided row (None for inf and far rows)."""
    if fam == 'H2':
        return key[0] + key[1] + key[3] + 3
    if fam == 'M2':
        return key[1] + key[2] + key[4] + 3
    return None


def cons_ok(r):
    """CONS on one row: its centre value lies in its certified [lo, hi] (hi None: v >= lo only, the far rows)."""
    lo_, v, hi_ = float(r[3].mid()), r[4], r[5]
    return bool(lo_ <= v and (hi_ is None or v <= float(hi_.mid())))


def judge(ev):
    """the kill rule on one piece: (ok, failing rows, uncovered classes, failing gates, absent n = 5 keys, risk rows, CONS rows)."""
    rows = ev['rows']
    bad = [r for r in rows if not (r[3] > 0)]
    risk = [r for r in rows if r[3] > 0 and r[2] < 2.0]
    unc = sorted([(k, m0) for k, m0 in ev['m0'].items() if m0 is None or m0 > M0MAX], key=str)
    badg = sorted(k for k, v in ev['gates'].items() if not v)
    have = set((r[0], tuple(r[1])) for r in rows)
    absent = [k5 for k5 in N5KEYS if (k5[0], tuple(k5[1])) not in have]
    cons = [r for r in rows if not cons_ok(r)]
    return (not bad and not unc and not badg and not absent and not cons), bad, unc, badg, absent, risk, cons


def piece_line(n, i, ev, jud):
    ok, bad, unc, badg, absent, risk, cons = jud
    rows = ev['rows']
    w = min(rows, key=lambda r: r[2]) if rows else None
    return ('RPIECE %d %04d ok=%d rows=%d bad=%d unc=%d gates_failing=%s n5absent=%d cons=%d risk=%d hmin=%.6g at %s %s | tau\' %.6e '
            'alpha_lo %.9f TRB\' %.6f beta_H %.6f c_fix %s pc_H %.4e pn_SH4 %.4e rho2 %.4e rho3 %.4e rho_inf %.4e | slots %d' % (
                n, i, 1 if ok else 0, len(rows), len(bad), len(unc), badg or '-', len(absent), len(cons), len(risk),
                w[2] if w else float('nan'), w[0] if w else '-', w[1] if w else '-', float(ev['tau']), float(ev['alo']), float(ev['trp']),
                float(ev['bH']), ev['cfix'], float(ev['pcH']), float(ev['pn']), float(ev['rho'][2]), float(ev['rho'][3]),
                float(ev['rho']['inf']), len(ev['keys'])))


def row_line(n, i, r):
    f, key, h, lo, v, hi, inf = r
    tail = ''
    if inf is not None:
        tail = ' | t1 %.6e ddet %.6e lin %.6e dz %.6e C1 %.6e Num_c [%.9e, %.9e] Z_c [%.9e, %.9e] cl2 %s' % (
            float(inf['t1']), float(inf['ddet']), float(inf['lin']), float(inf['dz']), float(inf['C1']), float(inf['numc'].lower()),
            float(inf['numc'].upper()), float(inf['Zc'].lower()), float(inf['Zc'].upper()),
            ('%.9e' % float(inf['cl2'])) if inf['cl2'] is not None else '-')
    return 'ROW %d %04d %s %s m %d lo %.9e hi %s v %.9e h %.6g%s' % (
        n, i, f, key[:-1], key[-1], float(lo), ('%.9e' % float(hi)) if hi is not None else '-', v, h, tail)


# ---- items
def bars_line(n, HE):
    """the ten entries' bars (err_b) against the targets (spec sect. 3)."""
    bf = max(Fraction(HE[k][2]) for k in HE if k.startswith('fT') or k.startswith('hT'))
    bs = max(Fraction(HE[k][2]) for k in HE if k.startswith('S4'))
    tg = BAR_TARGET[n]
    out('BARS N=%d: largest fT/hT bar %.3e (target %.1e), largest S4 HT bar %.3e (target %.1e) -> %s' % (
        n, float(bf), float(tg['f']), float(bs), float(tg['s']), 'within the targets' if (bf <= tg['f'] and bs <= tg['s']) else 'ABOVE A TARGET'))


SAMPLE_EVERY = 100   # as S8's: C-UNIF-H and C-MV-H on the first and last piece of each chunk and on every piece i with i % 100 == 0


def run_pieces(n, A, a, b, HE, HZ, trb, rows_out=True, samples=False):
    """pieces a..b-1: the kill rule, RPIECE, ROW, M0, KILL and RISK lines; samples (chunk items): C-UNIF-H and C-MV-H on the first and
    last piece and every SAMPLE_EVERY-th, C-MV-BAR-H, C-TARGET-H and C-MV-SF-H on the first. Returns (killed pieces, RISK rows, minima
    per class, n = 5 minima, the largest m0 per class with its piece count)."""
    kills, nrisk, mins, n5, m0x = [], 0, {}, {}, {}
    for i in range(a, b):
        try:
            ev = eval_piece(n, A, i, HE, HZ, trb)
            why = None if ev is not None else 'the S8 module gives no bound on the piece'
        except (ValueError, ArithmeticError, ZeroDivisionError) as e:
            ev, why = None, 'the evaluation breaks down (%r)' % (e,)
        if ev is None:
            out('RPIECE %d %04d ok=0 | %s' % (n, i, why))
            out('KILL N=%d I=%04d: no bound (%s)' % (n, i, why))
            kills.append(i)
            continue
        jud = judge(ev)
        out(piece_line(n, i, ev, jud))
        ok, bad, unc, badg, absent, risk, cons = jud
        if rows_out:
            for r in ev['rows']:
                out(row_line(n, i, r))
        out('M0 %d %04d %s' % (n, i, ' '.join('%s%s:%s' % (k[0], k[1], v) for k, v in sorted(ev['m0'].items(), key=str))))
        for r in bad[:8]:
            out('KILL N=%d I=%04d %s %s: certified lower end %.6e is not > 0' % (n, i, r[0], r[1], float(r[3])))
        for k, m0 in unc[:8]:
            out('KILL N=%d I=%04d class %s: top-mode m0 %s (no cover with m0 <= %d)' % (n, i, k, m0, M0MAX))
        for gname in badg:
            out('KILL N=%d I=%04d: gate %s fails' % (n, i, gname))
        for k5 in absent[:8]:
            out('KILL N=%d I=%04d: n = 5 key %s %s has no row (N5ABSENT)' % (n, i, k5[0], k5[1]))
        for r in cons[:8]:
            out('KILL N=%d I=%04d %s %s: centre value %.9e outside the certified [%.9e, %s] (CONS)' % (
                n, i, r[0], r[1], r[4], float(r[3]), ('%.9e' % float(r[5])) if r[5] is not None else '-'))
        for r in sorted(risk, key=lambda x: x[2])[:8]:
            out('RISK N=%d I=%04d %s %s: headroom %.6g (lower end %.6e, centre %.6e)' % (n, i, r[0], r[1], r[2], float(r[3]), r[4]))
        if not ok:
            kills.append(i)
        nrisk += len(risk)
        for r in ev['rows']:
            k_ = (r[0],) + tuple(r[1][:-1])
            if k_ not in mins or r[2] < mins[k_][0]:
                mins[k_] = (r[2], i, r[1][-1], float(r[3]))
            if n_of(r[0], r[1]) == 5:
                kk = (r[0], tuple(r[1]))
                if kk not in n5 or r[2] < n5[kk][0]:
                    n5[kk] = (r[2], i, float(r[3]))
        for k_, v_ in ev['m0'].items():
            kk = (k_[0],) + tuple(k_[1])
            mx, cnt = m0x.get(kk, (None, 0))
            m0x[kk] = ((v_ if mx is None or (v_ is not None and v_ > mx) else mx) if v_ is not None else mx, cnt + 1)
        if samples and (i in (a, b - 1) or i % SAMPLE_EVERY == 0):
            checks_h(n, A, ev, HE, HZ, trb, full=(i == a), tag=' (chunk sample)')
    return kills, nrisk, mins, n5, m0x


def run_smoke(n, A, HE, HZ, trb):
    i0 = A['RSTART'][n]
    iL = mod.NPIECES - 1
    out('SMOKE N=%d: S8\'s first piece %d (J from %.6g) and the last piece %d (J from %.6g to infinity)' % (
        n, i0, float(A['pieces'][n][i0]['jlo']), iL, float(A['pieces'][n][iL]['jlo'])))
    kills, nrisk, mins, n5, m0x = run_pieces(n, A, i0, i0 + 1, HE, HZ, trb)
    out('C-SMOKE-KILL N=%d piece %d: %s -> %s' % (n, i0, 'killed' if kills else 'passes the kill rule', gate('C-SMOKE-KILL', not kills)))
    ev = eval_piece(n, A, i0, HE, HZ, trb)
    jud = judge(ev)
    out('C-DUAL-OWN N=%d piece %d: the horizontal chain\'s dual pair reproduces its own centred slot-0 and slot-1 states -> %s' % (
        n, i0, gate('C-DUAL-OWN', ev['gates']['OWN'])))
    plant('PLANT-DUAL-SWAP', not dual_own(ev['cH'], other=ev['cV'][3]), '(the vertical chain\'s dual pair in the horizontal chain\'s place)')
    out('C-DUAL-KEYS N=%d piece %d: both sides\' dual pairs carry the box\'s %d slot keys in order, every dual leaf of that length -> %s' % (
        n, i0, len(ev['keys']), gate('C-DUAL-KEYS', ev['gates']['KEYS'])))
    chd, chm, rad, keys = ev['cH'][3]
    ksw = list(keys)
    ksw[1], ksw[2] = ksw[2], ksw[1]
    plant('PLANT-DUAL-KEYS-SWAP', not keys_ok((chd, chm, rad, ksw), keys), '(a dual pair whose slot list has slots 1 and 2 swapped)')
    chd2 = dict(chd)
    L2 = dict(chd['L'])
    y0 = L2[0][1]
    d0 = y0[1][0]
    L2[0] = (L2[0][0], (y0[0], [D(d0.v, d0.g[:-1])] + list(y0[1][1:])))
    chd2['L'] = L2
    plant('PLANT-DUAL-KEYS-DROP', not keys_ok((chd2, chm, rad, keys), keys), '(a dual pair with one slot dropped from one leaf)')
    if ev['rows']:
        r0 = ev['rows'][0]
        rows2 = [(x[0], x[1], x[2], (arb(-1) if x is r0 else x[3]), x[4], x[5], x[6]) for x in ev['rows']]
        plant('PLANT-KILL', not judge(dict(ev, rows=rows2))[0], '(the first row %s %s with lower end -1)' % (r0[0], r0[1]))
    k5 = N5KEYS[0]
    rows3 = [x for x in ev['rows'] if (x[0], tuple(x[1])) != (k5[0], tuple(k5[1]))]
    plant('PLANT-N5ABSENT', not judge(dict(ev, rows=rows3))[0], '(the n = 5 key %s %s removed from the rows)' % (k5[0], k5[1]))
    # C-BOX-PT: the box's lower ends are not above the point's at t = 1/J_lo
    tp = arb(1) / CM.fr(Fraction(A['pieces'][n][i0]['jlo']))
    evp = eval_piece(n, A, i0, HE, HZ, trb, T=tp)
    lp = {(x[0], tuple(x[1])): x[3] for x in evp['rows']}
    worse = [(x[0], x[1]) for x in ev['rows'] if (x[0], tuple(x[1])) in lp and x[3] > lp[(x[0], tuple(x[1]))] + abs(lp[(x[0], tuple(x[1]))]) * 1e-12]
    out('C-BOX-PT N=%d piece %d: %d rows; the box\'s lower end above the point\'s (t = 1/J_lo) at %d %s -> %s' % (
        n, i0, len(ev['rows']), len(worse), worse[:4] or '', gate('C-BOX-PT', not worse)))
    if ev['rows']:
        r0 = ev['rows'][0]
        rows4 = [(x[0], x[1], x[2], x[3], (float(x[3].mid()) - abs(float(x[3].mid())) - 1.0) if x is r0 else x[4], x[5], x[6])
                 for x in ev['rows']]
        plant('PLANT-CONS', not judge(dict(ev, rows=rows4))[0], '(the first row %s %s with its centre value below its lower end)' % (
            r0[0], r0[1]))
    # ---- the float engine's controls, kept (spec sect. 8), on pk11's float tables: rcm6's block with the n lists of N5-1
    HENT.update(load_json_entries())
    BETA = beta_h()
    out('INPUTS float N=%d: %d float horizontal entries (pk11 s8h_mk tables, pinned); beta_H %s (the rule\'s row T)' % (
        n, len(HENT), float(BETA)))
    img, pv = m1_controls(A, HENT, BETA, hz_rows(), i0)
    # ---- C-REPRO-RC5 (spec sect. 6) on this engine's rows at the first piece, and its plant
    n5c, n5b, lines = repro_rc5(ev, img, pv)
    for ln in lines:
        out(ln)
    out('C-REPRO-RC5 N=%d piece %d: %d of %d n = 5 keys have a row; P2-13\'s exact value at the box\'s ends and centre inside the certified '
        '[lo, hi]: failing %s -> %s' % (n, i0, n5c, len(N5KEYS), n5b or 'none', gate('C-REPRO-RC5', n5c == len(N5KEYS) and not n5b)))
    n5cp, n5bp, _ = repro_rc5(ev, img, pv, plant=True)
    plant('PLANT-REPRO-RC5', n5cp == len(N5KEYS) and len(n5bp) == n5cp, '(each exact value at hi + |hi|/100: %d of %d keys fail)' % (
        len(n5bp), n5cp))
    # ---- sect. 2's checks at the first piece, and their plants
    mb = checks_h(n, A, ev, HE, HZ, trb, full=True, tag=' (first piece)')
    T0 = ev['T']
    encq = CM.entry_points(HE, T0)
    held = sorted(k for k, e in encq.items() if e.rad() > 0 and mod.unif_ok(e, arb(e.upper()) + arb(e.rad()) / (1 << 10)))
    plant('PLANT-UNIF-SLACK-H', not held, '(piece %d, every entry with a radius (%d): a point 2^-10 rad(outer) beyond the enclosure\'s upper '
          'end fails unif_ok; held %s)' % (i0, sum(1 for e in encq.values() if e.rad() > 0), held or 'none'))
    nl, bm = mv_h(n, A, ev, HE, HZ, trb, zero_tgrad=True)
    plant('PLANT-MV-H', len(bm) > 0, '(piece %d with the t-gradients set to 0: C-MV-H fails on %d of %d leaves)' % (i0, len(bm), nl))
    dpl = mvbar_h(n, A, ev, HE, HZ, trb, plant=True)
    plant('PLANT-MV-BAR-H', dpl['bym'][1] > 0 and dpl['bym'][-1] > 0 and dpl['hits'] == {1},
          '(piece %d, bar-corner thin points against the zero-bar centred chain: failing leaves by mode %s)' % (i0, dpl['bym']))
    dtp = target_h(ev, mb, c1_scale=1e-3)
    plant('PLANT-TARGET-H', len(dtp['tfail']) > 0, '(piece %d with the box C1 x 1e-3: C-TARGET-H fails %d of %d checks)' % (
        i0, len(dtp['tfail']), dtp['tchecks']))
    # ---- C-MIXED-REG at the first and the last piece, and its plant
    evL = eval_piece(n, A, iL, HE, HZ, trb)
    judL = judge(evL)
    out(piece_line(n, iL, evL, judL))
    out('C-SMOKE-KILL-LAST N=%d piece %d: %s -> %s' % (n, iL, 'passes the kill rule' if judL[0] else 'killed',
                                                      gate('C-SMOKE-KILL-LAST', judL[0])))
    for lab, e_ in (('first', ev), ('last', evL)):
        nc, bd = mixed_reg_c(e_)
        out('C-MIXED-REG N=%d piece %d (%s; the certified pair form with the vertical chain on both sides against sf_pair, dk_class2 '
            'against dk_class, far_lo2 on both bases, ball for ball): %d comparisons, mismatches %s -> %s' % (
                n, e_['r']['i'], lab, nc, bd[:6] or 'none', gate('C-MIXED-REG', not bd)))
    ncp, bdp = mixed_reg_c(ev, plant=True)
    plant('PLANT-MIXED-REG', len(bdp) > 0, '(the right chain\'s slot-0 insertion vector + 1e-9: %d of %d comparisons differ)' % (len(bdp), ncp))
    checks_h(n, A, evL, HE, HZ, trb, full=True, tag=' (last piece)')
    # ---- C-HARM-RCC: this engine's certified chain at t = 0 against the harmonic strip, and PLANT-RCC (tau' = 0)
    ev0 = eval_piece(n, A, iL, HE, HZ, trb, T=arb(0), rows=False)
    if ev0 is None:
        out('C-HARM-RCC N=%d: the S8 module gives no bound at t = 0 -> %s' % (n, gate('C-HARM-RCC', False)))
    else:
        nR, bR, wR = harm_rcc(ev0)
        out('C-HARM-RCC N=%d piece %d at t = 0 (the entries\' bars and the piece\'s vacuum kept; gates failing %s): %d MIXED and FLIP/SAME '
            'classes (n = 5..8 and inf, m = 1..8), the harmonic value in the certified [lo, hi]: failing %s -> %s; largest lo/harmonic %.6f at '
            '%s (lo %.6e, harmonic %.6e, hi %.6e)' % (n, iL, sorted(k for k, v in ev0['gates'].items() if not v) or 'none', nR, bR[:6] or 'none',
                                                    gate('C-HARM-RCC', not bR), wR[0], wR[1], wR[2], wR[3], wR[4]))
        ev0p = eval_piece(n, A, iL, HE, HZ, trb, T=arb(0), rows=False, tau_ovr=ZERO)
        nRp, bRp, _ = harm_rcc(ev0p)
        plant('PLANT-RCC', len(bRp) > 0, '(tau\' = 0 in the chain at t = 0, pn_SH4 kept: containment fails for %d of %d classes %s)' % (
            len(bRp), nRp, bRp[:4]))
    return kills


def cover_keys():
    """the coverage list's class keys (spec sect. 7), as the row builders' m0 keys: FLIP/SAME H2 (dL, dR, kind), Hinf (dL, inf, kind),
    H1 (dL, far, kind) over DN; MIXED M2 HV (iH, dV, kind), Minf HV (iH, inf, kind), M1 HV (iH, far, kind) over NEAR_H x NEAR_V, Minf
    VH (dV, inf, kind) and M1 VH (dV, far, kind) over NEAR_V; both kinds."""
    ks = []
    for kind in ('flip', 'same'):
        for dL in DN[kind]:
            ks += [('H2', dL, dR, kind) for dR in DN[kind]] + [('Hinf', dL, 'inf', kind), ('H1', dL, 'far', kind)]
    for kind in ('same', 'flip'):
        for iH in NEAR_H:
            ks += [('M2', 'HV', iH, dV, kind) for dV in NEAR_V] + [('Minf', 'HV', iH, 'inf', kind), ('M1', 'HV', iH, 'far', kind)]
        for dV in NEAR_V:
            ks += [('Minf', 'VH', dV, 'inf', kind), ('M1', 'VH', dV, 'far', kind)]
    return ks


EDGE_RE = re.compile(r'^(a|b|t|bb)([1-5])$')


def edge_img(e, refl, flip):
    """an edge of P_3 x P_5 under the left-right reflection (vertical column c -> 6 - c, horizontal bond c -> 5 - c) and the top-bottom
    flip (a <-> b, t <-> bb)."""
    m = EDGE_RE.match(e)
    f, c = m.group(1), int(m.group(2))
    if refl:
        c = (6 - c) if f in ('a', 'b') else (5 - c)
    if flip:
        f = {'a': 'b', 'b': 'a', 't': 'bb', 'bb': 't'}[f]
    return '%s%d' % (f, c)


def pair_map():
    """the 80 D0 pairs of pk24's map (N5MAP, pinned; its PAIR lines): (pair, orbit, m, box column, classes, image), the image being the
    first of direct, reflection, flip and both (reflection and flip) that takes the orbit's pair to the pair."""
    res = []
    for ln in open(N5MAP).read().split('\n'):
        if not ln.startswith('PAIR '):
            continue
        p = [x.strip() for x in ln[len('PAIR '):].split(' | ')]
        pair, orb, mm, box, cls = p[0], p[1], p[2], p[3], p[4]
        pe, oe = set(pair.split(',')), orb.split(',')
        img = [nm for nm, rf, fl in (('direct', 0, 0), ('reflection', 1, 0), ('flip', 0, 1), ('both', 1, 1))
               if set(edge_img(e, rf, fl) for e in oe) == pe]
        res.append((pair, orb, mm, box, re.findall(r"(?:H2|M2) \([^)]*\)", cls), img[0] if img else 'NONE'))
    return res


def run_final(n, A, HE, HZ, trb):
    """the chunks of this N: this script's sha256 and mode on line 1, VERDICT VALID, C-KILL PASS; coverage of [RSTART, 904); the minima
    per class and the n = 5 keys from the chunks' lines; the coverage list (every class key on every piece, its largest m0); the pair
    map; C-PIECE-H with C-UNIF-H, C-MV-H, C-MV-BAR-H, C-TARGET-H and C-MV-SF-H at each family's binding piece and at the first and last
    covered pieces; PLANT-PIECE-H at the piece of the smallest headroom."""
    own = sha_file(os.path.abspath(__file__))
    cov, chunks, mins, n5, m0x = [], [], {}, {}, {}
    for fn in sorted(os.listdir(OUTD)):
        m = re.fullmatch(r'out_%s_%s_c%d_(\d{4})_(\d{4})\.out' % (LABEL, MODE, n), fn)
        if not m:
            continue
        txt = open(os.path.join(OUTD, fn)).read().split('\n')
        okh = txt[0].startswith('%s sha256 %s MODE=%s ITEM=chunk' % (LABEL, own, MODE))
        okv = [x for x in txt if x.startswith('VERDICT')] == ['VERDICT VALID']
        okk = any(x.startswith('C-KILL') and x.endswith('PASS') for x in txt)
        a_, b_ = int(m.group(1)), int(m.group(2))
        chunks.append((fn, sha_file(os.path.join(OUTD, fn)), okh and okv and okk))
        if okh and okv and okk:
            cov.append((a_, b_))
        for x in txt:
            if x.startswith('CLASSMIN '):
                p = x.split(' | ')
                k_, h_, i_ = p[1], float(p[2]), int(p[3])
                if k_ not in mins or h_ < mins[k_][0]:
                    mins[k_] = (h_, i_, p[4])
            if x.startswith('N5MIN '):
                p = x.split(' | ')
                k_, h_, i_ = p[1], float(p[2]), int(p[3])
                if k_ not in n5 or h_ < n5[k_][0]:
                    n5[k_] = (h_, i_, p[4])
            if x.startswith('CLASSM0 ') and okh and okv and okk:
                p = x.split(' | ')
                k_, v_, c_ = p[1], (None if p[2] == 'None' else int(p[2])), int(p[3])
                mx, cnt = m0x.get(k_, (None, 0))
                m0x[k_] = ((v_ if mx is None or (v_ is not None and v_ > mx) else mx) if v_ is not None else mx, cnt + c_)
    rs = sorted(cov)
    pos, okc = A['RSTART'][n], True
    for a_, b_ in rs:
        if a_ != pos:
            okc = False
        pos = b_
    out('C-COVER N=%d: valid chunks %s cover [%d, %d) without gap or overlap -> %s' % (n, rs, A['RSTART'][n], mod.NPIECES,
                                                                                   gate('C-COVER', okc and pos == mod.NPIECES)))
    bad = [c for c in chunks if not c[2]]
    out('C-CHUNKS N=%d: %d chunk outputs, %d not valid (%s) -> %s' % (n, len(chunks), len(bad), [c[0] for c in bad][:4],
                                                                      gate('C-CHUNKS', not bad)))
    for c in chunks:
        out('CHUNK %s %s %s' % (c[0], c[1], 'valid' if c[2] else 'NOT VALID'))
    for k_ in sorted(mins):
        out('FINALCLASS N=%d | %s | %.6g | %d | %s' % (n, k_, mins[k_][0], mins[k_][1], mins[k_][2]))
    for k_ in sorted(n5):
        out('FINALN5 N=%d | %s | %.6g | %d | %s' % (n, k_, n5[k_][0], n5[k_][1], n5[k_][2]))
    keys5 = set('%s %s' % (k5[0], tuple(k5[1])) for k5 in N5KEYS)
    out('C-N5-FINAL N=%d: every n = 5 key has a row on some piece (%d of %d) -> %s' % (n, len(set(n5) & keys5), len(keys5),
                                                                                      gate('C-N5-FINAL', keys5 <= set(n5))))
    if mins:
        w = min(mins.items(), key=lambda kv: kv[1][0])
        out('MIN N=%d: smallest headroom %.6g at piece %d, %s' % (n, w[1][0], w[1][1], w[0]))
    # the coverage list (spec sect. 7): every class key on every piece of the range, with its largest top-mode threshold
    npc = mod.NPIECES - A['RSTART'][n]
    short = []
    for ck in cover_keys():
        ks = str(ck)
        mx, cnt = m0x.get(ks, (None, 0))
        mn = mins.get(ks)
        if cnt != npc or mx is None:
            short.append(ks)
        out('COVER N=%d | %s | pieces %d of %d | rows m < m0 with n >= 5, the top-mode form from m0; largest m0 over the pieces %s | smallest '
            'headroom %s' % (n, ks, cnt, npc, mx, ('%.6g at piece %d' % (mn[0], mn[1])) if mn else 'no row (every m from m0 on the '
                                                                                                   'top-mode form, or n < 5)'))
    out('C-COVER-LIST N=%d: %d class keys (DN %s, NEAR_H %s, NEAR_V %s, T_M %d, DF %s, DF_V %d, DF_H %d, MM %d), each with an m0 on every '
        'piece of [%d, %d): short %s -> %s' % (n, len(cover_keys()), DN, NEAR_H, NEAR_V, T_M, DF, DF_V, DF_H, CM.MM, A['RSTART'][n],
                                               mod.NPIECES, short[:4] or 'none', gate('C-COVER-LIST', not short)))
    # the pair map (sect. 9, Q5)
    pm = pair_map()
    for pair, orb, mm, box, cls, img in pm:
        hs = ['%s %s' % (c_, ('%.6g at piece %d' % (n5[c_][0], n5[c_][1])) if c_ in n5 else 'NO ROW') for c_ in cls]
        out('PAIRMAP N=%d | %s | orbit %s (%s) | %s | %s | %s' % (n, pair, orb, img, mm, box, '; '.join(hs) if cls else 'joint (no chain class)'))
    sep = [x for x in pm if x[4]]
    badm = [x[0] for x in pm if x[5] == 'NONE' or any(c_ not in n5 for c_ in x[4])]
    out('C-PAIRMAP N=%d: %d pairs, %d separated with an n = 5 class (each class with a row), %d joint; pairs without an image or a row %s -> %s' % (
        n, len(pm), len(sep), len(pm) - len(sep), badm[:4] or 'none', gate('C-PAIRMAP', len(pm) == 80 and len(sep) == 58 and not badm)))
    # C-PIECE-H and the thin checks at the binding pieces (S8's final)
    if not mins:
        return
    fams = ('H2', 'Hinf', 'H1', 'M2', 'Minf', 'M1')
    bind = {}
    for k_, (h_, i_, x_) in mins.items():
        f_ = re.match(r"^\('(\w+)'", k_).group(1)
        if f_ not in bind or h_ < bind[f_][0]:
            bind[f_] = (h_, i_)
    todo = sorted(set([bind[f_][1] for f_ in fams if f_ in bind] + [A['RSTART'][n], mod.NPIECES - 1]))
    out('BINDING N=%d: %s; C-PIECE-H and the thin checks at pieces %s' % (
        n, '; '.join('%s %.6g at piece %d' % (f_, bind[f_][0], bind[f_][1]) for f_ in fams if f_ in bind), todo))
    for i in todo:
        nl, bl, br, xl = halves_h(n, A, i, HE, HZ, trb)
        out('C-PIECE-H N=%d piece %d (halves with the parent\'s basis, vacuum, U and trial set): failing rows, m0 or gates %d%s -> %s; leaves '
            '(INFO): %d of %d outside the parent beyond inside_r\'s slack, up to %.2e of the parent\'s radius' % (
                n, i, len(br), (' (%s)' % ', '.join(br[:3])) if br else '', gate('C-PIECE-H', not br), len(bl), nl, xl))
        ev = eval_piece(n, A, i, HE, HZ, trb)
        jud = judge(ev)
        out(piece_line(n, i, ev, jud))
        checks_h(n, A, ev, HE, HZ, trb, full=True, tag=' (binding)')
    iw = w[1][1]
    nl, bl, br, xl = halves_h(n, A, iw, HE, HZ, trb, collapse=True)
    plant('PLANT-PIECE-H', len(br) > 0, '(N=%d piece %d with the parent\'s box collapsed to its right end in J: C-PIECE-H fails on %d rows, '
          'm0 or gates; on %d leaves, INFO)' % (n, iw, len(br), len(bl)))


def run_record():
    """both N's smoke and final outputs (this script's sha256 and mode, VERDICT VALID); cert mode writes the record: the claim, the code,
    the outputs by sha256, the chunks, per class and N the smallest headroom, the n = 5 keys, the coverage list, the pair map, the
    binding pieces' C-PIECE-H lines, the smokes' control lines, and every pin."""
    own = sha_file(os.path.abspath(__file__))
    fin, smk, lines = {}, {}, []
    for n in (4, 3):
        for it, dst in (('smoke', smk), ('final', fin)):
            p = os.path.join(OUTD, 'out_%s_%s_%s_n%d.out' % (LABEL, MODE, it, n))
            txt = open(p).read().split('\n') if os.path.exists(p) else []
            ok = bool(txt) and txt[0].startswith('%s sha256 %s MODE=%s ITEM=%s' % (LABEL, own, MODE, it)) and \
                [x for x in txt if x.startswith('VERDICT')] == ['VERDICT VALID']
            out('C-%s N=%d: %s with this script\'s sha256 and VERDICT VALID -> %s' % (it.upper(), n, os.path.basename(p),
                                                                                   gate('C-%s' % it.upper(), ok)))
            dst[n] = (p, sha_file(p), txt)
    if MODE != 'cert' or FAILS:
        return
    lines = ['# NE_RC_RECORD_v1: written by %s (cert mode; every gate passed).' % LABEL, 'FORMAT = S4U_KV_v1', 'RECORD = NE_RC_RECORD_v1',
             'EXPORT_STATUS = CERTIFIED',
             'CLAIM = for N = 4 and every J >= 350, and for N = 3 and every J >= 300: Cov(s_e, s_f) > 0 for every pair of a top-row or '
             'bottom-row edge e with a horizontal or vertical edge f in NE\'s FLIP/SAME and MIXED classes on the horizontal chain: every '
             'two-sided class with n >= 5 (the 58 separated D0 pairs of P_3 x P_5 among them) and every class at infinity and far',
             'CODE = %s:%s' % (LABEL, own),
             'COVERAGE = per N and piece, the class keys of the COVER lines: FLIP/SAME H2 (dL, dR, kind), Hinf (dL, inf, kind), H1 (dL, far, '
             'kind) for dL, dR in DN = %s; MIXED M2 HV (iH, dV, kind), Minf HV (iH, inf, kind), M1 HV (iH, far, kind) for iH in 0..T_M, dV in '
             '-1..T_M - 1, and Minf VH (dV, inf, kind), M1 VH (dV, far, kind), T_M = 3 at N = 4 and 2 at N = 3; kinds flip and same; rows '
             'for m < m0 with n >= 5 (n = dL + dR + m + 3 and iH + dV + m + 3), the top-mode form from m0 on, every m0 <= %d (S8\'s KILL '
             'rule); the far rows by routes A and B; slots 0 and 1 from the exact entries, 2..7 and inf by RC; the bottom row as the parity '
             'mirror (F-a); every slot of DN (F-b)' % (DN, M0MAX)]
    for n in (4, 3):
        p, h, txt = smk[n]
        lines.append('SMOKE_N%d = %s:%s' % (n, os.path.basename(p), h))
        for x in txt:
            if x.split(' ')[0] in ('BARS', 'C-REPRO-RC5', 'C-HARM-RCC', 'C-MIXED-REG', 'C-HARM-H', 'C-HARM-H-M', 'C-HARM-RC', 'C-REPRO-H',
                                   'C-REPRO-M', 'C-UNIF-H', 'C-MV-BAR-H', 'C-MV-SF-H'):
                lines.append('N%d_SMOKE_%s' % (n, x.replace(' = ', ' : ')))
        p, h, txt = fin[n]
        lines.append('FINAL_N%d = %s:%s' % (n, os.path.basename(p), h))
        for x in txt:
            if x.split(' ')[0] in ('CHUNK', 'FINALCLASS', 'FINALN5', 'MIN', 'COVER', 'PAIRMAP', 'BINDING', 'C-PIECE-H', 'C-COVER-LIST',
                                   'C-PAIRMAP'):
                lines.append('N%d_%s' % (n, x.replace(' = ', ' : ')))
    for p in sorted(PINS):
        lines.append('PIN = %s:%s' % (os.path.relpath(p, CODEDIR), PINS[p]))
    for p in sorted(CERT_PINS):
        lines.append('PIN = %s:%s' % (os.path.relpath(p, CODEDIR), CERT_PINS[p]))
    txt = '\n'.join(lines) + '\nEND = NE_RC_RECORD_v1\n'
    with open(REC_PATH, 'x') as fh:
        fh.write(txt)
    out('RECORD %s %s' % (os.path.basename(REC_PATH), hashlib.sha256(txt.encode()).hexdigest()))


def main():
    complete = False
    try:
        if ITEM == 'record':
            run_record()
        else:
            afails, anof = [], []
            A = mod.run_A(afails, anof, plants=False)
            out('C-STAGE-A: the S8 module\'s stage A (cert mode) with failing gates %s -> %s' % (afails or 'none', gate('C-STAGE-A', not afails)))
            okm, mh = mhat_cite()
            out('C-MHAT: cited from %s, l.7 [%s] and l.19 [%s]; its RECORD line names S8\'s pinned M2(b) record %s with its sha256 %s -> %s' % (
                os.path.basename(M2BO), mh[0], mh[1], mh[2], mh[3][:16], gate('C-MHAT', okm)))
            trb = trb_rowT()
            n = N
            HZ = hz_rows_c(n)
            badg = [i for i in range(mod.NPIECES) if HZ[i]['jlo'] != float(A['pieces'][n][i]['jlo']) or
                    HZ[i]['jhi'] != float(A['pieces'][n][i]['jhi'])]
            out('C-GRID N=%d: pk15\'s export and S8\'s pieces share every J_lo and J_hi (%d pieces): differing %s -> %s' % (
                n, mod.NPIECES, badg[:5] or 'none', gate('C-GRID', not badg)))
            if MODE == 'cert':
                fb, ff = fmt_c3(n)
                out('C-FMT N=%d: runner c3\'s records %s through the bound reader, every needed key four spans with lo <= hi and a bar >= 0: '
                    'failing %s -> %s' % (n, [os.path.basename(C3REC[n][g]) for g in C3G], fb[:4] or 'none', gate('C-FMT', not fb)))
                for pn_, fl_ in sorted(ff.items()):
                    plant(pn_, len(fl_) == len(C3G) and all(fl_), '(each record: %s)' % fl_)
            else:
                out('C-FMT N=%d (INFO): dev mode reads runner c3\'s float twins (their KEYJSON lines); C-FMT on the records runs in cert mode' % n)
            HE = c3_entries(n)
            out('INPUTS N=%d: %d horizontal entries from %s; TRB_H row T %s; c_N %s' % (
                n, len(HE), 'runner c3\'s records' if MODE == 'cert' else 'runner c3\'s float twins (DEV)', trb[n],
                2 + Fraction((n - 1) * (n - 3), 8)))
            bars_line(n, HE)
            if ITEM == 'final':
                run_final(n, A, HE, HZ, trb)
            elif ITEM == 'smoke':
                run_smoke(n, A, HE, HZ, trb)
            else:
                if NAB[1] < A['RSTART'][n]:
                    out('C-RANGE N=%d: the chunk starts below S8\'s range (%d) -> %s' % (n, A['RSTART'][n], gate('C-RANGE', False)))
                kills, nrisk, mins, n5, m0x = run_pieces(n, A, NAB[1], NAB[2], HE, HZ, trb, samples=True)
                for k_ in sorted(mins, key=str):
                    out('CLASSMIN | %s | %.6g | %d | m %s lo %.6e' % ((k_,) + mins[k_]))
                for k_ in sorted(n5, key=str):
                    out('N5MIN | %s %s | %.6g | %d | lo %.6e' % ((k_[0], k_[1]) + n5[k_]))
                for k_ in sorted(m0x, key=str):
                    out('CLASSM0 | %s | %s | %d' % (k_, m0x[k_][0], m0x[k_][1]))
                out('C-KILL N=%d pieces [%d, %d): %d pieces fail the kill rule%s; RISK rows %d -> %s' % (
                    n, NAB[1], NAB[2], len(kills), (' (%s)' % kills[:20]) if kills else '', nrisk, gate('C-KILL', not kills)))
        complete = True
    except Exception as e:
        out('ERROR %s: %s' % (type(e).__name__, e))
        for ln in traceback.format_exc().splitlines()[-16:]:
            out('TRACE ' + ln)
        FAILS.append('ERROR')
    why = FAILS + ['%s did not fire' % x for x in NOFIRE] + ([] if complete else ['INCOMPLETE'])
    out('ITEM %s %s cpu %.1f s, wall %.1f s, peak resident memory %.0f MiB' % (MODE, SFX, cpu(), time.time() - T_START,
                                                                             resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
    if MODE == 'dev':
        out('DEV MODE: runner c3\'s float twins (a_k with their err) stand in for its records; nothing here is certified')
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(sorted(set(why)))))


main()
