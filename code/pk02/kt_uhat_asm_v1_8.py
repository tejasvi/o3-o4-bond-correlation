#!/usr/bin/env python3
"""kt_uhat_asm_v1_8.py -- pk02 (code/pk02/). REVISION of kt_uhat_asm_v1_7 (d1798147) by the approval of 2026-11-09 (cap 0.15
h), a re-pin only:
- pk04's r0b records now come from m3_run_r0b_v1_4's asm (the approval 02:32:17Z), so the r0b asm_out slot of
  CERT_INPUTS is pk03/out/m3_run_r0b_v1_4_asm.<N>.out; the records keep v1_3's names and format, and the asm output keeps the
  three-field RECORD lines;
- C-CERT-LIST requires both engine entries of each r0b record by full sha256: m3_run_r0b_v1_4 (8837ee03, R0B_ENGINE4) and
  m3_run_r0b_v1_3 (9fceb247, R0B_ENGINE); PLANT-CERT-LIST also offers a D4L0 record without the v1_4 entry, which must be refused;
  the dry records carry both entries;
- the texts, the runners and the template CERT_INPUTS_UHAT_v1_TEMPLATE_v1_8_N4.json follow. The notes stay
  deferred. Everything else is v1_7's; v1_7's docstring follows.
kt_uhat_asm_v1_7.py -- pk02 (code/pk02/). REVISION of kt_uhat_asm_v1_6 (6178ea52) by the approval of 22:2xZ (cap 0.15 h):
- the W2M record now comes from pk03's m3_run_r0m_v1_2 (861f64eb, chain b9635469; the option B, 22:03:08Z), so
  R0M_ENGINE pins it and the w2m.asm_out slot is pk03/out/m3_run_r0m_v1_2_asm.<N>.out (both read from m3_run_r0m_v1_2's own text:
  engine field l.2076, stdout out/m3_run_r0m_v1_2_<ITEM>.out). Its XB,b items are exact T <-> B alias copies of XT,b (alias_of set, each
  with its own factor list, l.2041-2044): C-W2M-RULE accepts an alias only as XB,b -> XT,b with the same ball (PLANT-W2M-RULE now also
  points XB,1 at XT,2), and the dry W2M record carries the same aliases;
- (a) of the route-0 analysis (fold in at the next revision): each family's empty key over itself is 1 exactly in E_pair, as
  W2's G_00 already is (C-ZZ checks it with a bar on the empty key; PLANT-ZZ evaluates the interval ratio the old way and must see it
  refused).
Everything else is v1_6's; v1_6's docstring follows.
kt_uhat_asm_v1_6.py -- pk02 (code/pk02/). REVISION of kt_uhat_asm_v1_5 (ea857895): the
W2M record now comes from pk03's m3_run_r0m_v1_1 (df8680fc, chain 89a044bb), so R0M_ENGINE pins it and the w2m.asm_out slot of
CERT_INPUTS is pk03/out/m3_run_r0m_v1_1_asm.<N>.out (both read from m3_run_r0m_v1_1's own text: engine field l.2076, output name
out/m3_run_r0m_v1_1_<ITEM>.out); the record name m3_r0m_W2M_N<N>_J300_v1.json is unchanged. Also: a refused cert input ends with a
REFUSED line and VERDICT INVALID (REFUSED), no traceback. The certified run goes one N at a time (run_uhat_cert_v1_6.sh N TAG, N4 first).
Everything else is v1_5's; its docstring follows.
kt_uhat_asm_v1_5.py -- pk02 (code/pk02/). The u-hat assembler (DESIGN_UHAT_ASM_v1_3 faa09e23 with ADD1 03f73445, ADD2
60de6595, ADD3 5e8bce50, ADD4 22e8469f, ADD5 71aac1ed and ADD6 e6125835; after kt_uhat_asm_v1_3 dd33fbd9 and v1_4 1897de71 (frozen,
never sent); the approval 2026-11-08T18:09Z, cap 5.5 h; the certified-wiring version, the approval of 21:0xZ, cap 1.0 h; the
certified run waits for pk03's production records).
v1_5 = v1_4 with the decision of 21:24Z on pk12's catch (v1_3's N4 l0_hat.D4ML0.q_hat_hi was 3.6e-19 below the square root of the
recorded L0_hi): every value the table defines as a form of other recorded values (route 0's xu_hi, T_s, q_b_hi; each L0 window's
q_hat_hi, xu_hi, xsu_hi, T_U4, q_hi; each piece's info q_b_hi) is that form on the recorded decimals of its parts, outward, rounded up;
C-DEC-UP re-reads each one as an exact rational against its form (square roots by squaring), PLANT-DEC-UP writes two values rounded the
wrong way. Parts keep C-DEC (each decimal against its exact end).
v1_4 wired cert mode (the mock path is v1_3's, its values the same up to the derived values above):
- CERT_INPUTS.json (format CERT_INPUTS_UHAT_v1) pins, by path relative to code/ and full sha256, the six r0b v1_3 records
  pk03/out/m3_r0b_<g>_N<N>_J300_v1.json (g = W2, W3e, W3f, D4L0, D4ML0, FA) with their asm output m3_run_r0b_v1_3_asm.<N>.out, and
  the W2M record m3_r0m_W2M_N<N>_J300_v1.json with m3_run_r0m_v1_asm.<N>.out. C-INPUTS refuses cert mode unless every one is pinned
  and hashes to its pin (the template CERT_INPUTS_UHAT_v1_TEMPLATE.json is refused).
- Each record is read through pk03's m3_reader_v6_3.load (628d2059; bound to its asm output) and r0asm_lib's CertReader (the a_k
  balls and the bar without rnd, CLAIM_BALL's form). C-CERT-LIST: the producer (m3_run_r0b_v1_3 9fceb247, m3_run_r0m_v1 475e5e94),
  the graph, the entry list by name and sha256, the key set (the list's certify and check keys), and each item's role, factors and
  empty key as the list gives them.
- W2's mirror windows in cert mode come from the W2M record: the window of an end by m3_run_r0m_v1's rule (recomputed here:
  mirror_window), R[mirror] = W[window]/W[Z] over the piece. C-W2M-MAP (both modes) maps every W2 end the bars read; C-W2M-RULE (cert)
  checks the record's twelve windows against the rule's factor lists.
- FA's g in cert mode: pk12's GJJ export v1_1 (1c3ffc33), N<N>_MAX (the J-uniform upper end of g_jj/g_00 over the piece set) for
  j = 1..3 and 1 for j = 0; C-GJJ checks the export (CERTIFIED, J range, the max over the set's piece lines).
- C-V2: rule V2 on every pinned input: its writer's output names it with its full sha256 on exactly one line in that writer's form
  (RECORD <name> <sha256>: M2B, M2B_W, the r0b and W2M records; RECORD <name> sha256 <sha256>: GJJ; EXPORT <name> sha256 <sha256>:
  the means export) and ends with the single line VERDICT VALID. The record carries every input as an info.input.* src line.
- C-CERT-PATH (mock): the cert path's reader chain (m3_reader_v6_3's parser and CertReader) on PRECERT texts written from the float
  entries gives every certify and check entry back exactly.
v1_3 took the rule on the N4 piece range: every J-uniform max and hull runs over the record's piece set, at N4 P0061..P0903 only
(the GJJ export's N<N>_PIECES, the range of S8 and R6.5), N3 P0000..P0903. Below P0061, RH_MODULE_v1_4 cor:rhstrips (l.443) proves
Cov >= 0 at N4 for J in [20, 350]; C-PIECES checks that the strip covers every J of the export below the first piece.
Library: uhat_lib_v1_2.py (bars, chain, transfers) and r0asm_lib_v1_3_1.py (piece_T, dec_round, FloatReader), both pinned by sha256.
Columns are numbered from 0, as in the records (ADD1 sect. 5).

ADD1: the k table by (family, key, role) (G,a,b: gram k = 1, vcomp k = 2; G_00 = 1 exactly); centres are one certified ball per piece
from R4's means export db731c93 (G-C), never window means or points. ADD3/ADD4: every k = 3 rest by operator factors with the three-term
T2 (no four-column mirror); beta_2 by source, k and the pin RULING_22; the A4 spot (D4L0 E012, E102, E112) by
2 J_W (N*_A2/(1 - eps_r))^(1/2), the route of record (A4 cancelled, main ~20:1xZ; C-K3-A4 refuses any A4 pin); each J-uniform part its
own max over the pieces. ADD5: FA's rest by operators (Lemma T, the signed F4 form; g = g_jj/g_00). ADD6: T_v = beta-hat s'.
v1_2 also adds C-WORLD-U (with a plant run through the gate code) and four notes (the int column's couplings read from
pk03's m3_graph_v3.strip; full sha256 pins; D4ML0's far-end A2 trace gated on the pin; plants that rerun code on perturbed inputs).
The record follows INTERFACE_UHAT_R65_v1_4 (frozen): one route0b_hat block per row of pk12's ROWS_N<N> (R65_D3_ROUTE0_ROWS_v1
6afdb5dd), C-FORM checks the lines as written, and the run output carries "RECORD <file> sha256 <full sha256>" and "VERDICT VALID" last.

Modes:
  mock  MOCK entries and W2 mirrors, for smokes: entries from the float ent files (pk11 r64_ent / b4c_ent and the L0 list's
        ak_float), W2's mirrors from a deterministic mock (R[mirror] = 1, R[mirror + pair] = the harmonic model's link mean,
        out/fhc_gauss_v1.out), FA's g from S8's float chain (pk11 TABLE_S8H_FLOAT_VALUES_v1_1). The centres, the J grid and the
        constants are the certified records already (db731c93, f8e3d5e0, 417cb603, 91109301).
  cert  the certified entries and W2M windows of the records CERT_INPUTS.json pins (above), FA's g from the GJJ export. A failed
        C-INPUTS stops the run before any entry is read.
Gates: C-HASH (full sha256 pins), C-V2 (+ PLANT-V2), C-INPUTS (cert; + PLANT-INPUTS), C-CERT-LIST (cert), C-CERT-PATH (mock;
+ PLANT-CERT-PATH), C-W2M-MAP (+ PLANT-W2M-MAP), C-W2M-RULE (cert), C-GJJ (+ PLANT-GJJ), C-KTAB (+ PLANT-KTAB, PLANT-KROLE, PLANT-W2M),
G-S, G-C (+ PLANT-GC-POINT, -SHIFT, -WMEAN; thin check + PLANT-GC-THIN), C-K3-SRC (+ PLANT-K3-SRC, PLANT-MHAT), C-K3-SRC-V
(+ PLANT-K3-SRC-V), G-BAR (degree <= 2; plant G,4,4), C-R1, C-SAMEROW, C-NOX, C-R2-POS (plant), C-K3-OP (+ PLANT-K3-OP, -SRC, -ROUTE),
C-K3-DECOMP (plant), C-K3-A4 (+ PLANT-K3-A4, -A4-SET, -A4-PIN), C-K3-COUNT (plant), C-K3-MONO (+ PLANT-K3-MONO-TAIL, -FAR, -G),
C-FA-OPS (+ PLANT-FA-ER, -LAMBDA), C-JGRID, C-PIECES (+ PLANT-PIECES), C-ROWS (completeness), G-ADJ, C-L0-POST (plant), C-T-RECOMPUTE
(plant), C-WORLD-U (plant), C-BASIS-RAW, C-TGT, C-FINITE (PLANT-NAN), C-DEC, C-FORM (with the table's world column
PLANT-FORM: eleven perturbed copies of the record, each refused), C-FA-G (+ PLANT-FA-G).
C-DEC-UP (+ PLANT-DEC-UP), C-ZZ (+ PLANT-ZZ; v1_7).
Run (v1_7): run_uhat_smoke_v1_7.sh TAG under the launcher (syntax checks, n4 and n3 mock, then cert mode on the template
CERT_INPUTS_UHAT_v1_TEMPLATE_v1_7_N4.json, which must refuse); the certified run, one N at a time, N4 first: run_uhat_cert_v1_7.sh N TAG on
CERT_INPUTS_UHAT_v1_N<N>.json."""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import sys, re, json, math, hashlib, resource, time, traceback, importlib.util
from fractions import Fraction
from flint import arb, ctx

OWN = '/mnt/g2/release/root/code/pk02'
CODEDIR = '/mnt/g2/release/root/code'
W4 = CODEDIR + '/pk11'
HZ = CODEDIR + '/pk15'
S4 = CODEDIR + '/pk08'
SCR = CODEDIR + '/pk10/scratch'
RULING_22 = 'rv02/RULING_K3_INTERIOR_BONDS_REST_BOUNDS_rv02.md:ece4cded241b4e60a7f6e95abfca877ffb95f0d6c35cd26ef2664c78937b48f3'
A4_PIN = None             # A4 is cancelled (main ~20:1xZ): C-K3-A4 refuses any value here; the A4 spot keeps the 2J form
LIB_PATH, LIB_SHA = OWN + '/uhat_lib_v1_2.py', 'f0b09542a96a2ba016520fb306dcc08097107e48793add54787c223aefdc0f0e'
RLIB_PATH, RLIB_SHA = OWN + '/r0asm_lib_v1_3_1.py', 'eb59ff519db33f830a65f90f27cb94564f606df536761d587c01652da07fb8a4'
MREAD_PATH, MREAD_SHA = OWN + '/m2b_reader_v1.py', 'a9f15db48e9fa51629448181d8a83679c1b93cd2b5696c8ed1e6b41d60df8b02'
RDR_PATH, RDR_SHA = CODEDIR + '/pk03/m3_reader_v6_3.py', '539b613f6a9c07a9bef3d0cbb408c1d41de276a6a59aede8b03149204ce28661'
R0B_FAMS = ('W2', 'W3e', 'W3f', 'D4L0', 'D4ML0', 'FA')                 # the six r0b v1_3 records (m3_run_r0b_v1_3 FAMS)
R0B_ENGINE = ('m3_run_r0b_v1_3', '73e3f46870584690e10ff75cda6f47e5963cdc1a3eeb69e5aa21c6f8cb25c460')   # pk03 MANIFEST_m3_run_r0b_v1_3
R0B_ENGINE4 = ('m3_run_r0b_v1_4', '7a5fdf75dc8c9cf2574f9fc6a95d79ae908c0193c34b3da5f940da3ec45bcdfe')   # pk04's asm producer
R0M_ENGINE = ('m3_run_r0m_v1_2', '3f0636faaa0c6d23ce0383da02e4acb4773193dcb8a3fd335235c62f1741d2a7')   # pk03 MANIFEST_m3_run_r0m_v1_2


class Refused(Exception):
    """a cert input the run refuses: the run ends with a REFUSED line, no traceback."""
W2M_WINDOWS = ('Z', 'M,1', 'M,2', 'M,3') + tuple('X%s,%d' % (r_, b_) for r_ in 'TB' for b_ in range(4))   # m3_run_r0m_v1's twelve
ITEMS = {'n4': 4, 'n3': 3}
EMPTY = {'W2': 'Z', 'W3e': 'Z', 'W3f': 'Z', 'D4L0': 'E000', 'D4ML0': 'S0000', 'FA': '1,0', 'FB': '1,0'}
MLINK = {4: {0: '1.0009', 1: '0.8453', 2: '1.0009'}, 3: {0: '0.6673', 1: '0.5636', 2: '0.6673'}}   # out/fhc_gauss_v1.out (MOCK use)
PINS_ALL = {
    'm2b_kv': '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',
    'm2b_asm_out': 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391',
    'm2bw_kv': 'd74ac24b3e1d2e9c8a4f2b9deb22400ae7f43ccf1778b8c70c4dc472137e42e9',
    'list_r0': 'e26dab2b95867801eb8b6a9dcef891af98aab6e931a6eedb77db4a59a2cfa994',
    'list_l0': '5b6c00afb19a69383fd669248bed8a152a8f7a1da9f75d279345beab0251849a',
    'list_d4': '1e717d64c6206500897e187590a46e9cca069f0f67117153e9a635c33b62e29a',
    'means': 'd6df054024d73630b19b99c575443f2ddb95cd5bd7a9804c1370a7cf733024f0',
    'hs_kv': 'b80760c5b79f121a0c39d3302308816064a482fb47c90341938d52f9420772a3',
    'rtr': 'a2b08d873bc88b1fcdb2e64db91070ce0b204eedef725d9bf45ad15074c7a430',
    'trb': '2c17c287c0affbfe0e0fcbd8097edff2258ea1109d91381d6206a11d4efdd694',
    'ruling22': 'ece4cded241b4e60a7f6e95abfca877ffb95f0d6c35cd26ef2664c78937b48f3',
    'ruling_e112': 'e2ba63a3f56940ad88b22bb06ff15ef705a54189b1157104ab486343ee33ddce',
    'hs_note': 'ffd98fc1946714e36e86359c338c38a6b89af31eb7f707306a0a59f3f281493b',
    'gjj': '38820caf78cebb529ad010676167ac042cebd5f4e9d62381af1e3a342eec2516',
    'gjj_out': '7a47219a3b5055afcf1b22a6d82a29fe1ec80d902a8cdd7410fb5d0d2563bb55',
    'means_out': '08954d9a9d525399d80b971f5bd526878e012e4f99791144c47391dc30cbc2d8',
    'm2bw_out': '263a4000d27eb4e6b59d9ffa0a8eb12c4e5da4833dd1bbe5348df04004eddf59',
    'rhmod': 'c536e5cf6fd65c678175ece6f2b05e0a63cd1ade33fca0ef19423ea7d3928b56',
    'harm': '815e8073cc1579c3b70382f8d73b6252ccf24b9f0d08c90fd6687b2df39674ac',
    'graph': '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    's8h': 'f6f50741c51305b19a4a0d230a0a07b6afd84b3c83755dd36ac30d1e413a9aed',
    'add6': 'a0fbebdd6da733c7538c609a9af737438c1b199c69b6da505763beee16fe60ad',
    'interface': '7ef0e195f95a2559558b254bd72ff54356e254b2899f2d6ce8fce00b58ab5706',
    'rows': 'c6822a6d3355b819813f78f561d16a745e016de757da968e78391c81fc7e48f1',
    4: {'ent_r0': 'f55a38d9ca41e91d0c2f7592e82a5add0f0deb05542724a661aaf7ff9029c93d',
        'ent_d4': '78abb911cb4edf247171f1b7cf40c945223e56727445afe0cb4670e780c407ca',
        'ts': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
        'trial': '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19'},
    3: {'ent_r0': 'bda8d2024dd877209aea1a75ba0c8749cc643a5486eca4e19eb4509a362b8f98',
        'ent_d4': '4e28743ecfccb5e66d285665517dd738ec4722fb458ff1742c5aa29a8a65a56c',
        'ts': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
        'trial': '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0'}}
BOTH_BOND_COUNT = {'W3e': 10, 'W3f': 1, 'D4L0': 3, 'D4ML0': 4}     # 04dc9e2d sect. 1 (C-K3-COUNT), the same at each N


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_mod(path, full_sha, name):
    got = sha(path)
    if full_sha is not None and got != full_sha:
        raise ValueError('C-HASH: %s is %s, pinned %s' % (path, got, full_sha))
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, got


def main(argv):
    if len(argv) < 3 or argv[0] not in ITEMS or not re.fullmatch(r'[A-Za-z0-9]{1,12}', argv[1]) or argv[2] not in ('mock', 'cert') or \
            (argv[2] == 'cert') != (len(argv) == 4):
        print('usage: kt_uhat_asm_v1_8.py n4|n3 TAG mock | n4|n3 TAG cert CERT_INPUTS.json')
        return 2
    ITEM, TAG, MODE = argv[0], argv[1], argv[2]
    N = ITEMS[ITEM]
    resource.setrlimit(resource.RLIMIT_CPU, (300, 305))
    resource.setrlimit(resource.RLIMIT_FSIZE, (60 * 2 ** 20, 60 * 2 ** 20))
    if os.path.dirname(os.path.abspath(__file__)) != OWN:
        print('kt_uhat_asm_v1_8 must run from its own folder')
        return 2
    OUTD = os.path.join(OWN, 'out')
    OUT_PATH = os.path.join(OUTD, 'out_kt_uhat_asm_v1_8_%s_%s.out' % (ITEM, TAG))
    REC = os.path.join(OUTD, 'UHAT_ASM_v1_8_N%d_%s.kv' % (N, TAG))
    for p_ in (OUT_PATH, REC):
        if os.path.realpath(os.path.dirname(p_)) != os.path.realpath(OUTD) or os.path.exists(p_):
            print('output path check failed (own out/ folder, new file): %s' % p_)
            return 2
    FH = open(OUT_PATH, 'x')

    def out(line):
        FH.write(line + '\n')
        FH.flush()
    T0 = time.process_time()
    FAILS, FIRES = [], []

    def gate(name, ok, line):
        out('%s: %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
        if not ok:
            FAILS.append(name)

    def plant(name, fired, line):
        out('%s: %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            FIRES.append(name)

    def refused(fn, *a, **kw):
        try:
            fn(*a, **kw)
        except Exception as e_:                                    # every library refusal is a ValueError (UhatError)
            return isinstance(e_, ValueError), str(e_)[:160]
        return False, 'accepted'
    try:
        ctx.prec = 512
        U, USHA = load_mod(LIB_PATH, LIB_SHA, 'uhat_lib_v1')
        L, _ = load_mod(RLIB_PATH, RLIB_SHA, 'r0asm_lib_v1_3_1')
        MR, _ = load_mod(MREAD_PATH, MREAD_SHA, 'm2b_reader_v1')
        RDR, _ = load_mod(RDR_PATH, RDR_SHA, 'm3_reader_v6_3')             # cert mode's record reader; C-CERT-PATH uses its parser in mock
        DECLOG = []

        def dhi(x):
            f_ = L.end_frac(arb(x).upper())
            s_ = L.dec_round(f_, True)
            DECLOG.append((s_, f_, True))
            return s_

        def dlo(x):
            f_ = L.end_frac(arb(x).lower())
            s_ = L.dec_round(f_, False)
            DECLOG.append((s_, f_, False))
            return s_

        def dball(x):
            return '%s %s' % (dlo(x), dhi(x))
        # ------------------------------------------------------------ inputs and C-HASH
        F = {'m2b_kv': OWN + '/M2B_KV_v1.txt', 'm2b_asm_out': OWN + '/out/out_m2b_asm_v1.out', 'm2bw_kv': OWN + '/M2B_W_KV_v1_r1.txt',
             'list_r0': W4 + '/out/r64_v1/ROUTE0B_ENTRY_LIST_v1.json', 'list_l0': W4 + '/out/r64_v1/ROUTE0L0_ENTRY_LIST_v1.json',
             'list_d4': W4 + '/out/b4c_v1/D4BULK_ENTRY_LIST_v1.json',
             'means': HZ + '/out/export_p2_14_means_cert_kt_p2_assembly_v1_37.kv', 'hs_kv': S4 + '/out/HS_INV_NORMX_v1_d3d4b.kv',
             'rtr': S4 + '/S4_RTR_CERTIFIED_v1.md', 'trb': S4 + '/S4_TRB_CERTIFIED_v1.md',
             'gjj': CODEDIR + '/pk12/out/gjj_v1_1/GJJ_EXPORT_v1_kt_gjj_export_v1_1.kv',
             'gjj_out': CODEDIR + '/pk12/out/gjj_v1_1/out_kt_gjj_export_v1_1_run.out',
             'means_out': HZ + '/out/out_kt_p2_assembly_v1_37_cert.out', 'm2bw_out': OWN + '/out/out_m2b_wasm_v1_2_r1.out',
             'rhmod': CODEDIR + '/pk14/paper/rh_module_v1_4/RH_MODULE_v1_4.tex', 'ruling22': CODEDIR + '/' + RULING_22.split(':')[0],
             'ruling_e112': CODEDIR + '/rv02/RULING_E112_FAR_BOND_V2_rv02.md', 'hs_note': S4 + '/HS_NORMX_LEMMA_NOTE_v1.md',
             'harm': OWN + '/out/fhc_gauss_v1.out', 'graph': CODEDIR + '/pk03/m3_graph_v3.py',
             's8h': W4 + '/out/TABLE_S8H_FLOAT_VALUES_v1_1.tsv', 'add6': OWN + '/DESIGN_UHAT_ASM_v1_3_ADD6.md',
             'interface': OWN + '/INTERFACE_UHAT_R65_v1_4.md', 'rows': CODEDIR + '/pk12/R65_D3_ROUTE0_ROWS_v1.kv',
             'ent_r0': W4 + '/out/r64_v1/r64_ent_v1.%d.json' % N, 'ent_d4': W4 + '/out/b4c_v1/b4c_ent_v1.%d.json' % N,
             'ts': W4 + '/out/%s' % ('ts_N4_J170_D_S_z9sym_v1.json' if N == 4 else 'ts_N3_S_z9sym_v1.json'),
             'trial': SCR + '/m2_N%d_J170.json.b' % N}
        PINS = dict(PINS_ALL[N], **{k: v for k, v in PINS_ALL.items() if isinstance(k, str)})
        cfg = None
        if MODE == 'cert':
            F['config'] = os.path.abspath(argv[3])
            if not F['config'].startswith(CODEDIR + '/') or '..' in os.path.relpath(F['config'], CODEDIR).split('/'):
                raise Refused('C-INPUTS: CERT_INPUTS must be named by a path under code/ (its info.input line is relative to code/)')
            cfg = json.load(open(F['config']))
        FULL = {k: sha(p) for k, p in F.items()}
        SELF = sha(os.path.abspath(__file__))
        out('kt_uhat_asm_v1_8 sha256 %s ITEM=%s TAG=%s MODE=%s; lib uhat_lib_v1_2 %s, r0asm_lib %s, m2b_reader %s, m3_reader_v6_3 %s' % (
            SELF, ITEM, TAG, MODE, USHA, RLIB_SHA[:8], MREAD_SHA[:8], RDR_SHA[:8]))
        bad = [k for k, v in PINS.items() if len(v) != 64 or FULL[k] != v]                 # full sha256 pins only
        gate('C-HASH', not bad, 'full sha256 of %d files read: %s%s' % (len(F), ', '.join('%s %s' % (k, FULL[k][:8]) for k in sorted(F)),
                                                                       ('; differ: %s' % bad) if bad else ''))
        if bad:
            raise ValueError('C-HASH')

        # ------------------------------------------------------------ C-V2: rule V2 on every pinned input
        def v2_problem(name, rsha, out_text, head, sha_word):
            """rule V2: the writer's output names the input (base name) with its full sha256 on exactly one line '<head> <name> <sha256>'
            (sha_word: '<head> <name> sha256 <sha256>'), the writer's own form, and its VERDICT lines are exactly one 'VERDICT VALID', the
            last non-empty line. None, or the problem."""
            lines_ = out_text.split('\n')
            want = [head, name] + (['sha256'] if sha_word else []) + [rsha]
            hits = [ln for ln in lines_ if ln.split()[:2] == [head, name]]
            if len(hits) != 1 or hits[0].split() != want:
                return '%s: %d %s lines name it, the form "%s" not met once' % (name, len(hits), head, ' '.join(want[:-1] + ['<sha256>']))
            body = [ln for ln in lines_ if ln.strip()]
            if [ln for ln in lines_ if ln.startswith('VERDICT')] != ['VERDICT VALID'] or body[-1] != 'VERDICT VALID':
                return '%s: the writer\'s VERDICT lines are not one "VERDICT VALID" as the last line' % name
            return None

        def v2_file(rec_path, out_path, head, sha_word):
            return v2_problem(os.path.basename(rec_path), sha(rec_path), open(out_path).read(), head, sha_word)
        V2_IN = [('m2b_kv', 'm2b_asm_out', 'RECORD', False), ('m2bw_kv', 'm2bw_out', 'RECORD', False), ('gjj', 'gjj_out', 'RECORD', True),
                 ('means', 'means_out', 'EXPORT', True)]
        v2_bad = [p_ for p_ in (v2_file(F[r_], F[o_], h_, w_) for r_, o_, h_, w_ in V2_IN) if p_]
        gate('C-V2', not v2_bad, 'rule V2 on the pinned inputs, each in its writer\'s form: M2B_KV_v1 (518f7a4c) and M2B_W_KV_v1_r1 (9cc64e7c) '
             '"RECORD <name> <sha256>", GJJ v1_1 (b5361309) "RECORD <name> sha256 <sha256>", the means export (e353d42b) "EXPORT <name> sha256 '
             '<sha256>"; each writer ends with the single line VERDICT VALID; problems %s' % (v2_bad[:2] or 'none'))
        g_out, mn_out, mb_out = (open(F[k_]).read() for k_ in ('gjj_out', 'means_out', 'm2b_asm_out'))
        g_name, g_sha = os.path.basename(F['gjj']), FULL['gjj']
        p_v2 = {'a flipped sha256': v2_problem(g_name, g_sha, g_out.replace(g_sha, g_sha[::-1]), 'RECORD', True),
                'a second VERDICT line': v2_problem(os.path.basename(F['means']), FULL['means'], mn_out + 'VERDICT VALID\n', 'EXPORT', True),
                'a line after VERDICT': v2_problem(os.path.basename(F['m2b_kv']), FULL['m2b_kv'], mb_out + 'INFO after\n', 'RECORD', False),
                'the form without "sha256"': v2_problem(g_name, g_sha, g_out, 'RECORD', False)}
        plant('PLANT-V2', all(p_v2.values()), 'the same check refuses %s' % ', '.join('%s (%s)' % (k_, 'refused' if v_ else 'ACCEPTED')
                                                                                   for k_, v_ in p_v2.items()))
        # ------------------------------------------------------------ C-INPUTS: cert mode needs every certified record pinned
        CI_NAMES = {('r0b', 'asm_out'): 'pk03/out/m3_run_r0b_v1_4_asm.%d.out' % N, ('w2m', 'asm_out'): 'pk03/out/m3_run_r0m_v1_2_asm.%d.out' % N,
                    ('w2m', 'record'): 'pk03/out/m3_r0m_W2M_N%d_J300_v1.json' % N}
        CI_NAMES.update({('r0b', g_): 'pk03/out/m3_r0b_%s_N%d_J300_v1.json' % (g_, N) for g_ in R0B_FAMS})

        def cert_inputs(cfg_):
            """C-INPUTS: CERT_INPUTS (format CERT_INPUTS_UHAT_v1, this N) pins every certified record of this N and its writer's output by
            path relative to code/ (exactly the producer's name) and full sha256, and each file hashes to its pin. ({slot: path}, problems)."""
            if not isinstance(cfg_, dict) or cfg_.get('format') != 'CERT_INPUTS_UHAT_v1' or cfg_.get('N') != N:
                return {}, ['not CERT_INPUTS_UHAT_v1 for N%d' % N]
            got_, bad_ = {}, []
            for (grp, slot), rel in sorted(CI_NAMES.items()):
                sect = cfg_.get(grp) if isinstance(cfg_.get(grp), dict) else {}
                d_ = sect.get(slot) if slot in ('asm_out', 'record') else (sect.get('records') or {}).get(slot)
                if not isinstance(d_, dict) or d_.get('path') != rel or not re.fullmatch('[0-9a-f]{64}', str(d_.get('sha256'))):
                    bad_.append('%s.%s not pinned as %s with a full sha256' % (grp, slot, rel))
                    continue
                p_ = os.path.join(CODEDIR, rel)
                if not os.path.isfile(p_) or sha(p_) != d_['sha256']:
                    bad_.append('%s.%s: %s missing or not its pin' % (grp, slot, rel))
                    continue
                got_[(grp, slot)] = p_
            return got_, bad_
        tmpl = {'format': 'CERT_INPUTS_UHAT_v1', 'N': N, 'r0b': {'asm_out': {'path': CI_NAMES[('r0b', 'asm_out')], 'sha256': None},
                'records': {g_: {'path': CI_NAMES[('r0b', g_)], 'sha256': None} for g_ in R0B_FAMS}},
                'w2m': {'asm_out': {'path': CI_NAMES[('w2m', 'asm_out')], 'sha256': None}, 'record': {'path': CI_NAMES[('w2m', 'record')],
                                                                                                       'sha256': None}}}
        wrong = json.loads(json.dumps(tmpl))
        wrong['r0b']['records']['W2'] = {'path': os.path.relpath(F['gjj'], CODEDIR), 'sha256': FULL['gjj']}     # a real, pinned file, the wrong name
        _, pb1 = cert_inputs(tmpl)
        _, pb2 = cert_inputs(wrong)
        plant('PLANT-INPUTS', len(pb1) == len(CI_NAMES) and any(x_.startswith('r0b.W2 ') for x_ in pb2), 'the same check refuses the template '
              '(%d of %d slots unpinned) and a W2 slot that holds a real file with its right sha256 under another name' % (len(pb1), len(CI_NAMES)))
        CI = {}
        if MODE == 'cert':
            CI, ci_bad = cert_inputs(cfg)
            gate('C-INPUTS', not ci_bad, 'CERT_INPUTS (%s) pins the six r0b records of N%d with m3_run_r0b_v1_4_asm.%d.out and the W2M record '
                 'with m3_run_r0m_v1_2_asm.%d.out, by path and full sha256; problems %s' % (FULL['config'][:8], N, N, N, ci_bad[:3] or 'none'))
            if ci_bad:
                raise Refused('C-INPUTS: cert mode needs every certified record pinned (%d of %d slots unpinned or off their pins: %s)' % (
                    len(ci_bad), len(CI_NAMES), '; '.join(ci_bad)))
            v2c = [p_ for p_ in [v2_file(CI[('r0b', g_)], CI[('r0b', 'asm_out')], 'RECORD', False) for g_ in R0B_FAMS] +
                   [v2_file(CI[('w2m', 'record')], CI[('w2m', 'asm_out')], 'RECORD', False)] if p_]
            gate('C-V2-CERT', not v2c, 'rule V2 on the certified records: each named once by its asm output as "RECORD <name> <sha256>", '
                 'which ends with the single line VERDICT VALID; problems %s' % (v2c[:2] or 'none'))
        # ------------------------------------------------------------ M2B (G-S), M2B_W, trial table, kbar
        rec = MR.load(F['m2b_kv'], F['m2b_asm_out'], expected_sha256=PINS['m2b_kv'])
        kn = rec['N%d' % N]
        eps_r = U.up(MR.farb(MR.dec(kn['EPS_R_300'][0], 'EPS_R_300')))
        s_hi = U.up(MR.farb(MR.dec(kn['S_300'][0], 'S_300')))
        eps_w = U.up(MR.farb(MR.dec(kn['EPS_W_300'][0], 'EPS_W_300')))
        eps_d = U.up(MR.farb(MR.dec(kn['EPS_D_300'][0], 'EPS_D_300')))
        s2 = U.up(s_hi * s_hi)
        sp = U.up(s_hi * (1 + s_hi))
        MU = U.up(1 / U.lo(1 - eps_r))
        A = arb(N - 1) / 2
        trial = json.load(open(F['trial']))
        kbar = arb(trial['kbar'])
        gate('G-S', bool(s_hi > 0) and bool(s_hi < arb('1e-3')) and sorted(trial.keys()) == ['J', 'N', 'items', 'kbar'] and
             trial['N'] == N, 's = %s and eps_r = %s from M2B_KV_v1 (13cc0d9a) through m2b_reader_v1.load bound to its asm output; '
             's\' = s(1 + s) = %.10e; kbar %.16g from the PIN_TRIAL file m2_N%d_J170.json.b' % (
                 kn['S_300'][0], kn['EPS_R_300'][0], float(sp), float(kbar.mid()), N))
        wkv = {}
        for ln in open(F['m2bw_kv']).read().split('\n'):
            if ' = ' in ln and not ln.startswith('#'):
                k_, v_ = ln.split(' = ', 1)
                wkv[k_.strip()] = v_.strip()
        okw = wkv.get('VERDICT_OF_WRITER') == 'VALID' and wkv.get('RECORD') == 'M2B_W_KV_v1'
        EK = {'eps_r': eps_r, 'eps_w': eps_w, 'eps_d': eps_d, 'kbar': kbar}
        for nm in ('XITB', 'XITM2', 'XITB2', 'XITM_XIMB', 'XITM_XITB'):
            EK[nm] = U.up(U.farb(Fraction(wkv['N%d_EPS_W_%s_300' % (N, nm)])))
        gate('C-M2BW', okw, 'M2B_W_KV_v1_r1 (f73a1071) VERDICT_OF_WRITER VALID; xi-only keys %s (units mu-hat ||psi-hat||)' % (
            ', '.join('%s %.4e' % (nm, float(EK[nm])) for nm in ('XITB', 'XITM2', 'XITB2', 'XITM_XIMB', 'XITM_XITB'))))
        S = json.load(open(F['ts']))['S']
        # ------------------------------------------------------------ beta-hat and beta_2 constants by key (ADD1 sect. 3, ADD2 sect. 1)

        def kv_str(path, key):
            ms = re.findall(r'^%s = (\S+)\s*$' % re.escape(key), open(path).read(), re.M)
            if len(ms) != 1:
                raise ValueError('C-K3-SRC: %s has %d lines for %s' % (os.path.basename(path), len(ms), key))
            return ms[0]
        CK = {'A2': kv_str(F['hs_kv'], 'N%d_A2' % N), 'RTR': kv_str(F['hs_kv'], 'N%d_RTR' % N), 'TRB': kv_str(F['trb'], 'N%d_TRB' % N),
              'M1': kv_str(F['rtr'], 'N%d_MHAT_M1' % N), 'M2': kv_str(F['rtr'], 'N%d_MHAT_M2' % N), 'M3': kv_str(F['rtr'], 'N%d_MHAT_M3' % N)}
        A2c, RTRc, TRBc = (U.farb(Fraction(CK[k_])) for k_ in ('A2', 'RTR', 'TRB'))           # decimal upper ends, exact
        MH = [U.farb(Fraction(float(CK[k_]))) for k_ in ('M1', 'M2', 'M3')]                   # binary64 literals (MHAT_RULE), exact
        rtr_hs = kv_str(F['rtr'], 'N%d_RTR' % N) == CK['RTR']

        def src_ok(val, key_):
            """C-K3-SRC: a constant is the ball of the record's exact decimal read by key (endpoint for endpoint), never a typed number."""
            canon = U.farb(Fraction(CK[key_]))
            return isinstance(val, arb) and bool(val.lower() == canon.lower()) and bool(val.upper() == canon.upper())
        gate('C-K3-SRC', src_ok(A2c, 'A2') and src_ok(RTRc, 'RTR') and src_ok(TRBc, 'TRB') and rtr_hs and all(bool(m_ > 0) for m_ in MH),
             'read by key: N%d_A2 %s and N%d_RTR %s (HS_INV_NORMX_v1_d3d4b f8e3d5e0; N%d_RTR equal in S4_RTR_CERTIFIED_v1 417cb603), '
             'N%d_TRB %s (S4_TRB_CERTIFIED_v1 91109301), N%d_MHAT_M1..M3 %s (binary64 literals, all > 0)' % (
                 N, CK['A2'], N, CK['RTR'], N, N, CK['TRB'], N, ' '.join(CK[k_] for k_ in ('M1', 'M2', 'M3'))))
        typed = arb(2.33539825174 if N == 4 else 1.47608088926)
        plant('PLANT-K3-SRC', not src_ok(typed, 'A2'), 'a hand-typed N*_A2 (the float %r) is not the record\'s exact decimal' % float(typed))
        fmh, wmh = refused(U.mhat_lo, MH[0], -MH[1], MH[2], '400')
        plant('PLANT-MHAT', fmh, 'a read m2 <= 0 (the sign flipped) is refused (mhat increasing needs m1..m3 > 0): %s' % wmh)

        def int_v_ok(cert, graph_int):
            """C-K3-SRC's int-column condition (ADD4 sect. 2): the int column's couplings equal the certificates' column V."""
            return cert is not None and tuple(cert) == tuple(graph_int)

        def column_couplings(strip_fn, columns, col):
            """(T-M, M-B, T-B) tags of one column from pk03's strip(columns) edge list (None where the edge is absent)."""
            _, E_ = strip_fn(columns)
            tags = {tuple(sorted(e_)): str(t_) for e_, t_ in E_}
            T_, M_, B_ = 3 * col, 3 * col + 1, 3 * col + 2
            return tuple(tags.get(p_) for p_ in ((T_, M_), (M_, B_), (T_, B_)))
        sys.modules.setdefault('m3_scal', type(sys)('m3_scal'))            # strip() uses no m3_scal function; the stub only lets it import
        MG, _ = load_mod(F['graph'], PINS['graph'], 'm3_graph_v3')
        GCOL = {'vac': column_couplings(MG.strip, ['vac', 'int', 'vac'], 0), 'int': column_couplings(MG.strip, ['vac', 'int', 'vac'], 1)}
        hs_l33 = open(F['hs_note']).read().split('\n')[32]
        CERT_V = ('1', '1', None) if 'V(sigma) = e^{J(s_T.s_M - 1)} e^{J(s_M.s_B - 1)}' in hs_l33 and 's_T.s_B' not in hs_l33 else None
        gate('C-K3-SRC-V', int_v_ok(CERT_V, GCOL['int']), 'the certificates\' column V (HS_NORMX_LEMMA_NOTE_v1 1340a52c l.33: couplings %s, '
             'no T-B edge) equals the int column\'s couplings %s read from pk03\'s m3_graph_v3.strip (020d4b54); the vac columns\' %s are '
             'model columns and enter no operator bound' % (CERT_V, GCOL['int'], GCOL['vac']))
        plant('PLANT-K3-SRC-V', not int_v_ok(CERT_V, column_couplings(MG.strip, ['vac', 'vac', 'vac'], 1)), 'a vac column (with its T-B '
              'edge, %s) offered as the int column is refused, read through the same strip() code' % (column_couplings(MG.strip, ['vac', 'vac',
                                                                                                                         'vac'], 1),))
        # ------------------------------------------------------------ lists, entries (mock: float ent files; cert: the r0b records), C-KTAB
        l_r0, l_l0, l_d4 = json.load(open(F['list_r0'])), json.load(open(F['list_l0'])), json.load(open(F['list_d4']))
        rdf = L.FloatReader([json.load(open(F['ent_r0'])), json.load(open(F['ent_d4']))])
        ITEMS_, AKF = {}, {}
        for lst, fams in ((l_r0, ('W2', 'W3e', 'W3f')), (l_l0, ('D4L0', 'D4ML0')), (l_d4, ('FA',))):
            graphs = lst.get('graphs', {})
            for key_, e in lst['entries'].items():
                fam, k_ = key_.split(':', 1)
                if fam not in fams:
                    continue
                if fam in ('D4L0', 'D4ML0'):
                    AKF[(fam, k_)] = [float(x) for x in e['ak_float']['N%d' % N][:4]]
                    co = ([arb(x) for x in AKF[(fam, k_)]], 0.0)
                else:
                    AKF[(fam, k_)] = [float(x) for x in rdf.fl(fam, k_)]
                    co = rdf.entry(fam, k_)
                cols = graphs.get(fam, {}).get('columns') or (['vac', 'vac'] if fam == 'W2' else ['vac', 'int', 'vac'])
                ITEMS_[(fam, k_)] = {'factors': e['factors'], 'role': e.get('role'), 'co': co, 'columns': cols}
        CERT_ROLES = ('certify', 'check')                                   # the keys the r0b records hold (info keys carry no entry)
        LIST_PIN = {'W2': 'list_r0', 'W3e': 'list_r0', 'W3f': 'list_r0', 'D4L0': 'list_l0', 'D4ML0': 'list_l0', 'FA': 'list_d4'}

        def list_src_ok(s_, lk):
            """an entry_list field 'name:sha256[ note]': the list's file name and its pinned full sha256."""
            m_ = re.fullmatch(r'([^:\s]+):([0-9a-f]{64})( .*)?', s_ if isinstance(s_, str) else '')
            return bool(m_) and os.path.basename(m_.group(1)) == os.path.basename(F[lk]) and m_.group(2) == PINS[lk]

        def mirror_rule_factors(w_):
            """the W2M window w_'s factor list by m3_run_r0m_v1's rule: Z = [p0, p1], M,b = [p0, st_b 0, p1, st_b 1], XT,b / XB,b = Z or M,b
            with xi (0, 3) / (2, 5)."""
            b_ = int(w_.split(',')[1]) if ',' in w_ else 0
            base = [['p', 0]] + ([['st', b_, 0]] if b_ else []) + [['p', 1]] + ([['st', b_, 1]] if b_ else [])
            return base if w_[0] in 'ZM' else base + [['xi', [{'T': 0, 'B': 2}[w_[1]], 3 + {'T': 0, 'B': 2}[w_[1]]]]]

        def fac_key(fs):
            return sorted(json.dumps(f_ if f_[0] != 'xi' else ['xi', sorted(f_[1])]) for f_ in fs)

        def dry_item(ak, role, factors, empty):
            """one PRECERT item: ak as written, every bar part and radius 0, the u-hat fields as a certified record carries them."""
            law = {'n': N - 1, 'J_REF': 300, 'a_G': [[1.0, 1.0]]}
            return {'kind': 'entry', 'ak': [float(a_) for a_ in ak], 'ak_rad': [0.0] * 4, 'B': {p_: 0.0 for p_ in RDR.PARTS},
                    'Bp': {p_: 0.0 for p_ in RDR.PARTS[:4]}, 'err': 0.0, 'parity': 'free', 'role': role, 'factors': factors, 'empty': empty,
                    'laws': {'rem_tpow': 4, 'tail': dict(law), 'ann': dict(law), 'far_rate': 1.0, 'far_cF': '1'}}

        def dry_raws(akf):
            """the DRY records of mock mode, JSON objects in m3_reader_v6_3's PRECERT form (never written to a file, never certified): the
            six r0b records from the float entries akf, with the producer, graph, entry list and each item's role, factors and empty key as
            a certified record carries them; the W2M record with the rule's twelve windows (Z = W2's Z, M,b = Z, XT,b and XB,b = Z times the
            mock's link mean of their row), so that its window ratios hold the mock mirrors."""
            head = {'format': 'M3_RECORD_v1_PRECERT', 'claim': RDR.NONCERT['M3_RECORD_v1_PRECERT'] + RDR.CERT_CLAIM, 'J_REF': 300, 'N': N}
            raws = {}
            for g_ in R0B_FAMS:
                raws[g_] = dict(head, engine={R0B_ENGINE4[0]: R0B_ENGINE4[1], R0B_ENGINE[0]: R0B_ENGINE[1]}, graph=g_, entry_list='%s:%s' % (
                    os.path.basename(F[LIST_PIN[g_]]), PINS[LIST_PIN[g_]]), items={
                    k_: dry_item(akf[(f_, k_)], it['role'], it['factors'], EMPTY[g_]) for (f_, k_), it in ITEMS_.items()
                    if f_ == g_ and it['role'] in CERT_ROLES})
            zak = akf[('W2', 'Z')]
            raws['W2M'] = dict(head, engine={R0M_ENGINE[0]: R0M_ENGINE[1]}, graph='W2M', entry_list='%s:%s (W2\'s certify keys, by mirror rule)' % (
                os.path.basename(F['list_r0']), PINS['list_r0']), items={
                w_: dry_item([a_ * (1.0 if w_[0] in 'ZM' else float(MLINK[N][{'T': 0, 'B': 2}[w_[1]]])) for a_ in zak], 'certify',
                             mirror_rule_factors(w_), 'Z') for w_ in W2M_WINDOWS})
            for w_ in W2M_WINDOWS:                                          # as m3_run_r0m_v1_2 writes them: XB,b an alias copy of XT,b
                if w_.startswith('XB,'):
                    raws['W2M']['items'][w_] = dict(raws['W2M']['items']['XT,' + w_[3:]], factors=mirror_rule_factors(w_), alias_of='XT,' + w_[3:],
                                                    alias_kind='tb')
            return raws

        def parse_dry(raws):
            return {g_: RDR.loads_noncert(json.dumps(r_), 300, N, 'PRECERT_%s' % g_) for g_, r_ in raws.items()}

        def cert_list_bad(raws, recs):
            """C-CERT-LIST: each r0b record's producer (m3_run_r0b_v1_4 and m3_run_r0b_v1_3, both by full sha256), graph, entry list (the list's file name and pinned
            sha256), key set (the list's certify and check keys of the family, in the file and as the reader parsed it) and every item's
            role, factors and empty key as the list; the W2M record's producer, graph and entry list."""
            bad_ = []
            for g_ in R0B_FAMS:
                top_, its_ = raws[g_], raws[g_].get('items', {})
                want_ = {k_: it for (f_, k_), it in ITEMS_.items() if f_ == g_ and it['role'] in CERT_ROLES}
                if (top_.get('engine') or {}).get(R0B_ENGINE[0]) != R0B_ENGINE[1] or (top_.get('engine') or {}).get(R0B_ENGINE4[0]) != R0B_ENGINE4[1] or \
                        top_.get('graph') != g_ or \
                        not list_src_ok(top_.get('entry_list'), LIST_PIN[g_]):
                    bad_.append('%s: producer, graph or entry list' % g_)
                if set(its_) != set(want_) or set(recs[g_]['balls']) != set(want_):
                    bad_.append('%s: key set (%d record, %d list)' % (g_, len(its_), len(want_)))
                bad_ += ['%s:%s role, factors or empty' % (g_, k_) for k_, it in sorted(want_.items()) if k_ in its_ and (
                    its_[k_].get('role') != it['role'] or its_[k_].get('factors') != it['factors'] or its_[k_].get('empty') != EMPTY[g_])]
            top_ = raws['W2M']
            if (top_.get('engine') or {}).get(R0M_ENGINE[0]) != R0M_ENGINE[1] or top_.get('graph') != 'W2M' or \
                    not list_src_ok(top_.get('entry_list'), 'list_r0'):
                bad_.append('W2M: producer, graph or entry list')
            return bad_

        def w2m_rule_bad(raw_, rec_):
            """C-W2M-RULE: the W2M record holds exactly the twelve windows (in the file and as the reader parsed it), each with the
            mirror rule's factor list; an alias (m3_run_r0m_v1_2) only as XB,b -> XT,b, with exactly the source's ball."""
            its_ = raw_.get('items', {})
            bad_ = [w_ for w_ in W2M_WINDOWS if w_ not in its_ or fac_key(its_[w_].get('factors') or []) != fac_key(mirror_rule_factors(w_))]
            if set(its_) != set(W2M_WINDOWS) or set(rec_['balls']) != set(W2M_WINDOWS):
                bad_.append('the window set')
            for w_ in W2M_WINDOWS:
                src_ = (its_.get(w_) or {}).get('alias_of')
                if src_ is not None and (not w_.startswith('XB,') or src_ != 'XT,' + w_[3:] or rec_['balls'].get(w_) != rec_['balls'].get(src_)):
                    bad_.append('%s: alias of %s' % (w_, src_))
            return bad_

        def entries_bad(recs):
            """C-CERT-PATH: every certify and check entry read through r0asm_lib's CertReader (key format '{k}', one record per family)
            equals the mock entry endpoint for endpoint (a key the records lack raises)."""
            cr_ = L.CertReader(RDR, recs, '{k}')
            bad_ = []
            for (f_, k_), it in sorted(ITEMS_.items()):
                if it['role'] not in CERT_ROLES:
                    continue
                c_, b_ = cr_.entry(f_, k_)
                c0, b0 = it['co']
                if (len(c_) != 4 or len(c0) != 4 or float(b_) != float(b0) or
                        not all(bool(x_.lower() == y_.lower()) and bool(x_.upper() == y_.upper()) for x_, y_ in zip(c_, c0))):
                    bad_.append('%s:%s' % (f_, k_))
            return bad_
        if MODE == 'cert':
            RAW, RECS = {}, {}
            for g_ in R0B_FAMS:
                RECS[g_] = RDR.load(CI[('r0b', g_)], CI[('r0b', 'asm_out')], 300, N)          # certified, bound to its asm output
                RAW[g_] = json.load(open(CI[('r0b', g_)]))
            RECS['W2M'] = RDR.load(CI[('w2m', 'record')], CI[('w2m', 'asm_out')], 300, N)
            RAW['W2M'] = json.load(open(CI[('w2m', 'record')]))
            how = 'read by m3_reader_v6_3.load, each bound to its asm output'
        else:
            RAW = dry_raws(AKF)
            RECS = parse_dry(RAW)
            how = 'DRY: PRECERT objects written from the float entries, parsed by m3_reader_v6_3.loads_noncert, never written'
        cl_bad = cert_list_bad(RAW, RECS)
        gate('C-CERT-LIST', not cl_bad, 'the six r0b records (producers %s %s and %s %s) and the W2M record (%s %s), %s: graph, entry list by name and '
             'full sha256, the key set (the list\'s certify and check keys) and every item\'s role, factors and empty key as the list; problems '
             '%s' % (R0B_ENGINE4[0], R0B_ENGINE4[1][:8], R0B_ENGINE[0], R0B_ENGINE[1][:8], R0M_ENGINE[0], R0M_ENGINE[1][:8], how, cl_bad[:3] or 'none'))
        w2r = w2m_rule_bad(RAW['W2M'], RECS['W2M'])
        gate('C-W2M-RULE', not w2r, 'the W2M record (%s) holds exactly the twelve windows %s, each with the mirror rule\'s factor list, '
             'aliases only XB,b -> XT,b with the same ball (%d present); problems %s' % (
                 'DRY' if MODE == 'mock' else 'certified', ' '.join(W2M_WINDOWS),
                 sum(1 for v_ in RAW['W2M'].get('items', {}).values() if v_.get('alias_of')), w2r or 'none'))
        CRD = L.CertReader(RDR, RECS, '{k}')
        W2MCO = {w_: CRD.entry('W2M', w_) for w_ in W2M_WINDOWS}           # cert: the bars' mirrors; mock: C-CERT-MIRROR's dry windows
        if MODE == 'cert':
            for (fam, k_), it in ITEMS_.items():
                it['co'] = CRD.entry(fam, k_) if it['role'] in CERT_ROLES else None
        else:
            cpb = entries_bad(RECS)
            ncp = sum(1 for it in ITEMS_.values() if it['role'] in CERT_ROLES)
            gate('C-CERT-PATH', not cpb, 'DRY: the cert path\'s reader chain (m3_reader_v6_3 628d2059\'s parser, then r0asm_lib\'s CertReader '
                 'with key format {k}, one record per family %s) gives all %d certify and check entries back exactly; differ %s' % (
                     '/'.join(R0B_FAMS), ncp, cpb[:3] or 'none'))
            k0 = sorted(k_ for k_, it in ITEMS_.items() if it['role'] == 'certify')[0]
            akp = dict(AKF)
            akp[k0] = [akp[k0][0] + 2.0 ** -30] + list(akp[k0][1:])
            plant('PLANT-CERT-PATH', entries_bad(parse_dry(dry_raws(akp))) == ['%s:%s' % k0], 'the same chain flags exactly %s:%s when its '
                  'a_0 is moved by 2^-30 in the dry record' % k0)
            rp = json.loads(json.dumps(RAW))
            rp['W3e']['engine'][R0B_ENGINE[0]] = R0B_ENGINE[1][::-1]
            rp['D4L0']['engine'].pop(R0B_ENGINE4[0], None)
            kf = sorted(rp['FA']['items'])[0]
            rp['FA']['items'][kf]['factors'] = rp['FA']['items'][kf]['factors'][1:]
            pcl = cert_list_bad(rp, RECS)
            plant('PLANT-CERT-LIST', any(x_.startswith('W3e: producer') for x_ in pcl) and any(x_.startswith('D4L0: producer') for x_ in pcl) and \
                  any(x_.startswith('FA:%s ' % kf) for x_ in pcl),
                  'the same check refuses a W3e record from another producer sha256, a D4L0 record without the m3_run_r0b_v1_4 entry and an FA item '
                  '(%s) whose factor list lost a factor' % kf)
            rw = json.loads(json.dumps(RAW['W2M']))
            rw['items']['XT,1']['factors'] = mirror_rule_factors('XB,1')
            rw2 = json.loads(json.dumps(RAW['W2M']))
            rw2['items']['XB,1']['alias_of'] = 'XT,2'
            plant('PLANT-W2M-RULE', w2m_rule_bad(rw, RECS['W2M']) == ['XT,1'] and w2m_rule_bad(rw2, RECS['W2M']) == ['XB,1: alias of XT,2'],
                  'the same check refuses a W2M record whose XT,1 carries XB,1\'s bond (2, 5), and one whose XB,1 names XT,2 as its alias source')
        kt_bad, kt_n = [], 0
        for (fam, k_), it in ITEMS_.items():
            roles = (['gram', 'vcomp'] if (fam == 'W2' and U.G_RE.match(k_)) else ['entry'])
            for ro in roles:
                try:
                    U.uhat_k(fam, k_, it['columns'], it['factors'], ro)
                    kt_n += 1
                except ValueError as e_:
                    kt_bad.append('%s:%s/%s %s' % (fam, k_, ro, e_))
        gate('C-KTAB', not kt_bad, '%d (key, role) pairs classified by family, key pattern and role (W2 G,a,b: gram k 1, vcomp k 2); '
             'refusals %s' % (kt_n, kt_bad[:3] or 'none'))
        it_z = ITEMS_[('W2', 'Z')]
        f1, w1 = refused(U.uhat_k, 'W2', 'G,0,0', it_z['columns'], it_z['factors'], 'entry')
        f2, w2 = refused(U.uhat_k, 'FA', '1,0', ['vac', 'int', 'vac'], [['p', 0], ['p', 2]], 'entry')
        f3, w3 = refused(U.uhat_k, 'W2', 'Z', it_z['columns'], it_z['factors'], 'gram')
        plant('PLANT-KTAB', f1 and f2 and f3, 'G,0,0 without a role (as if read through its alias Z): %s; an FA item without its cp factor '
              '(counted with its cp column): %s; the non-G key Z in the Gram role: %s' % (w1, w2, w3))
        it_g01 = ITEMS_[('W2', 'G,0,1')]
        fkr, wkr = refused(U.ktab_role_check, 'W2', 'G,0,1', it_g01['columns'], it_g01['factors'], 'vcomp', 1)
        plant('PLANT-KROLE', fkr, 'the gram-role k = 1 fed to the vcomp companion G,0,1 is refused: %s' % wkr)
        fw2m, ww2m = refused(U.ktab_role_check, 'W2M', 'XT,0', ['vac', 'vac'], [], 'entry', 3)
        kw2m = U.uhat_k('W2M', 'XT,0', ['vac', 'vac'], [], 'entry')
        plant('PLANT-W2M', fw2m and kw2m == 2, 'the W2M row gives k = %d; a W2M mirror window offered with k = 3 is refused: %s' % (kw2m, ww2m))
        # ------------------------------------------------------------ the J grid and the centre balls: R4's means export (ADD1 sect. 2)
        EXP, JMIN, CEN, JS = {}, None, {}, {}
        mtxt = open(F['means']).read()
        rx = re.compile(r'^N%d_(D3|D4|D4M)_P(\d{4}) = (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)$' % N)
        for ln in mtxt.split('\n'):
            m = rx.match(ln)
            if m:
                cls, pc = m.group(1), int(m.group(2))
                JS[(cls, pc)] = (m.group(3), m.group(4))
                CEN[(cls, pc)] = (m.group(5), m.group(6), m.group(7), m.group(8))
                if cls == 'D3':
                    EXP[pc] = (m.group(3), m.group(4))
            elif ln.startswith('J_MIN = '):
                JMIN = ln.split('=', 1)[1].strip()
        npc = len(EXP)
        mhead = all(('\n%s\n' % h_) in mtxt for h_ in ('EXPORT_STATUS = CERTIFIED', 'RUN_VERDICT = VALID',
                                                     'FIELDS = jlo jhi ce_lo ce_hi cf_lo cf_hi Cov_inf_lo Cov_inf_hi'))
        samej = all(JS.get((cls, pc)) == EXP[pc] for cls in ('D3', 'D4', 'D4M') for pc in range(npc))
        gate('C-JGRID', mhead and samej and sorted(EXP) == list(range(npc)) and npc >= 10 and
             all(EXP[i][1] == EXP[i + 1][0] for i in range(npc - 1)) and JMIN is not None and Fraction(EXP[0][0]) >= Fraction(JMIN) and
             EXP[npc - 1][1] == 'inf', 'the means export (db731c93, CERTIFIED, RUN_VERDICT VALID, FIELDS jlo jhi ce_lo ce_hi cf_lo cf_hi ...) '
             'has P0000..P%04d for N%d in D3, D4 and D4M with the same J ends, adjacent pieces share their ends, J_lo_0 %s >= J_MIN %s, the '
             'last piece runs to inf' % (npc - 1, N, EXP[0][0], JMIN))
        # the record's piece set (the rule after the v1_2 check): the GJJ export's N<N>_PIECES, the range of S8 and R6.5; below its
        # first piece RH_MODULE_v1_4 cor:rhstrips gives Cov >= 0, so no J-uniform part needs the pieces there
        GKV = {}
        for ln in open(F['gjj']).read().split('\n'):
            if ' = ' in ln and not ln.startswith('#'):
                k_, v_ = ln.split(' = ', 1)
                if k_ in GKV:
                    raise ValueError('C-PIECES: the GJJ export has %s twice' % k_)
                GKV[k_] = v_.strip()
        rh_lines = open(F['rhmod']).read().split('\n')
        RH = {}
        if '\\label{cor:rhstrips}' in rh_lines[441]:
            RH = {int(n_): (lo_, hi_) for n_, lo_, hi_ in re.findall(r'\$N=([34])\$ and every \$J\\in\[(\d+),(\d+)\]\$', rh_lines[442])}

        def pieces_ok(first, last, gkv):
            """C-PIECES: P<first>..P<last> is the GJJ export's N<N>_PIECES and ends at the means export's last piece; every piece of the set
            has the means export's J ends in the GJJ export; RH_MODULE_v1_4 cor:rhstrips' strip [lo, hi] for this N covers every J of the
            means export below the first piece (lo <= J_MIN and the first piece's J_lo <= hi)."""
            if gkv.get('N%d_PIECES' % N) != 'P%04d..P%04d' % (first, last) or last != npc - 1 or not 0 <= first <= last or N not in RH:
                return False
            for pc in range(first, last + 1):
                f_ = gkv.get('N%d_P%04d' % (N, pc), '').split()
                if len(f_) < 2 or (f_[0], f_[1]) != EXP[pc]:
                    return False
            return Fraction(RH[N][0]) <= Fraction(JMIN) and Fraction(EXP[first][0]) <= Fraction(RH[N][1])
        mP = re.fullmatch(r'P(\d{4})\.\.P(\d{4})', GKV.get('N%d_PIECES' % N, ''))
        PF, PL = (int(mP.group(1)), int(mP.group(2))) if mP else (-1, -1)
        okP = mP is not None and GKV.get('EXPORT_STATUS') == 'CERTIFIED' and pieces_ok(PF, PL, GKV)
        gate('C-PIECES', okP, 'the record\'s piece set at N%d is P%04d..P%04d (%d pieces): the GJJ export v1_1\'s N%d_PIECES (1c3ffc33, CERTIFIED), '
             'each piece with the means export\'s J ends; RH_MODULE_v1_4 cor:rhstrips (4b28147a l.443: N%d, J in [%s, %s]) covers the '
             'export\'s J from J_MIN %s up to the first piece\'s J_lo %s' % (N, PF, PL, PL - PF + 1, N, N, RH.get(N, ('-', '-'))[0],
                                                                            RH.get(N, ('-', '-'))[1], JMIN, EXP[PF][0] if okP else '-'))
        if not okP:
            raise ValueError('C-PIECES: the record\'s piece set is not established')
        PCS = range(PF, PL + 1)
        JRNG = '%s inf' % EXP[PF][0]                                        # the first piece's J_lo as written in centres.source

        def gjj_bad(gkv):
            """C-GJJ: the GJJ export is CERTIFIED, its N<N>_J_RANGE is the record's J range, and N<N>_MAX is, for each j = 1..3, the max of
            the upper ends u_j > 0 on the set's piece lines (exact rationals)."""
            if gkv.get('EXPORT_STATUS') != 'CERTIFIED' or gkv.get('N%d_J_RANGE' % N) != JRNG:
                return 'status %r or J range %r' % (gkv.get('EXPORT_STATUS'), gkv.get('N%d_J_RANGE' % N))
            mx = [Fraction(x_) for x_ in gkv.get('N%d_MAX' % N, '').split()]
            us = [[Fraction(x_) for x_ in gkv.get('N%d_P%04d' % (N, pc), '').split()[2:5]] for pc in PCS]
            if len(mx) != 3 or any(len(u_) != 3 or min(u_) <= 0 for u_ in us):
                return 'shape: N%d_MAX or a piece line is not three values > 0' % N
            if [max(u_[j] for u_ in us) for j in range(3)] != mx:
                return 'N%d_MAX is not the max over P%04d..P%04d' % (N, PF, PL)
            return None
        gj = gjj_bad(GKV)
        GJJ_MAX = [Fraction(x_) for x_ in GKV['N%d_MAX' % N].split()]      # u_1..u_3: FA's certified g for j = 1..3 (g = 1 at j = 0)
        gate('C-GJJ', gj is None, 'the GJJ export v1_1 (1c3ffc33, bound to its run output by C-V2): CERTIFIED, N%d_J_RANGE "%s" = the record\'s, '
             'N%d_MAX %s = the max of g_jj/g_00\'s upper ends over the %d piece lines P%04d..P%04d; problem %s' % (
                 N, JRNG, N, ' '.join(GKV['N%d_MAX' % N].split()), len(PCS), PF, PL, gj or 'none'))
        mx_l = GKV['N%d_MAX' % N].split()
        gp3 = dict(GKV, **{'N%d_MAX' % N: ' '.join([str(Fraction(mx_l[0]) * Fraction(999999, 1000000))] + mx_l[1:])})
        plant('PLANT-GJJ', gjj_bad(gp3) is not None, 'the same check refuses an export whose N%d_MAX u_1 sits 1e-6 below the max over its '
              'pieces' % N)
        gp1 = dict(GKV, **{'N%d_PIECES' % N: 'P%04d..P%04d' % (PF + 1, PL)})
        gp2 = dict(GKV, **{'N%d_P%04d' % (N, PF): ' '.join([EXP[PF][0] + '1'] + GKV['N%d_P%04d' % (N, PF)].split()[1:])})
        plant('PLANT-PIECES', not pieces_ok(PF + 1, PL, gp1) and not pieces_ok(PF, PL, gp2), 'the same check refuses a GJJ export whose set '
              'starts one piece later (P%04d, J_lo %s, above the RH strip\'s %s) and one whose P%04d has a J_lo the means export does not have' % (
                  PF + 1, EXP[PF + 1][0], RH[N][1], PF))

        def cball(lo_s, hi_s):
            """the exact decimal ball [lo, hi] of the export, outward."""
            return U.farb(Fraction(lo_s)).union(U.farb(Fraction(hi_s)))

        def centres_at(pc, cls):
            """G-C (ADD1 sect. 2): the certified centre balls of piece pc from the class key N<N>_<cls>_P<pc>: c_t = ce; D3: c_bb = cf;
            D4 and D4M: c_b = cf. Route 0 reads D3 (c_e = c_t, c_f = c_bb); D4L0 and B' read D4; D4ML0 reads D4M."""
            ce_lo, ce_hi, cf_lo, cf_hi = CEN[(cls, pc)]
            ce, cf = cball(ce_lo, ce_hi), cball(cf_lo, cf_hi)
            out_ = {'c_e': ce, 'c_f': cf, 'c_t': ce, 'cls': cls, 'pc': pc}
            out_['c_bb' if cls == 'D3' else 'c_b'] = cf
            return out_
        GC_CHECKED, GC_BAD = [0], []

        def gc_ok(cc):
            """G-C's check: the centres a piece uses are the export's balls for that piece, endpoint for endpoint."""
            ref = centres_at(cc['pc'], cc['cls'])
            return all(bool(cc[k_].lower() == ref[k_].lower()) and bool(cc[k_].upper() == ref[k_].upper()) for k_ in ('c_e', 'c_f'))

        def gc_use(cc):
            GC_CHECKED[0] += 1
            if not gc_ok(cc):
                GC_BAD.append((cc['cls'], cc['pc']))
            return cc

        # ------------------------------------------------------------ the per-piece machinery
        def val(co, T):
            c, bar = co
            return c[0] + c[1] * T + c[2] * U.sq(T) + U.UNIT * L.rbar(c, bar, T.upper(), 0.0)

        def ratio(fam, k_, T):
            return val(ITEMS_[(fam, k_)]['co'], T) / val(ITEMS_[(fam, EMPTY[fam])]['co'], T)

        def mock_mirror(fam, k_, end, kind, truth, T=None):
            base = arb(1)
            if kind == 'K':
                return base
            it = ITEMS_[(fam, k_)]
            adj = (1 - end) if fam == 'W2' else U.FAM_INT[fam]
            rows_ = U.junction_bonds(it['factors'], end, adj)
            return base * arb(MLINK[N][rows_[0]])

        def mirror_name(factors, end, kind):
            """the W2M window a W2 key's end reads (m3_run_r0m_v1's rule, recomputed here): the rest, the factors off the end column, must
            be p and at most one st_b, all on the other column, with at most one bond at the end's K step; kind 'K' reads Z (b = 0) or M,b,
            kind 'Kxi' reads XT,b or XB,b by the bond's row (a T or B bond only)."""
            rest, bonds = [], []
            for f_ in factors:
                cs = {f_[-1]} if f_[0] in ('p', 'st', 'cp') else {f_[1][0] // 3, f_[1][1] // 3}
                if end in cs:
                    if f_[0] == 'xi' and len(cs) == 2:
                        bonds.append(f_[1][0] % 3)
                    continue
                rest.append(f_)
            if sorted(f_[0] for f_ in rest) not in (['p'], ['p', 'st']) or any(f_[-1] != 1 - end for f_ in rest) or len(bonds) > 1:
                raise ValueError('C-W2M-MAP: no mirror window for %s at end %d (rest %r, bonds %r)' % (factors, end, rest, bonds))
            b_ = ([f_[1] for f_ in rest if f_[0] == 'st'] or [0])[0]
            if kind == 'K':
                return ('M,%d' % b_) if b_ else 'Z'
            if len(bonds) != 1 or bonds[0] not in (0, 2):
                raise ValueError('C-W2M-MAP: the +1-pair window of %s at end %d needs one T or B bond, found rows %r' % (factors, end, bonds))
            return 'X%s,%d' % ('TMB'[bonds[0]], b_)

        def cert_mirror(fam, k_, end, kind, truth, T):
            """cert mode's W2 mirror: R[window] = W[window]/W[Z] of the W2M record over the piece T (the ball over T), the window by
            mirror_name."""
            if fam != 'W2':
                raise ValueError('C-W2M-MAP: only W2 reads mirror windows, not %s' % fam)
            return val(W2MCO[mirror_name(ITEMS_[(fam, k_)]['factors'], end, kind)], T) / val(W2MCO['Z'], T)
        MIRF = cert_mirror if MODE == 'cert' else mock_mirror
        W2_MIR = ['Z', 'CE', 'CF'] + ['%s,%d' % (p_, a_) for p_ in ('V', 'KE', 'K1') for a_ in range(4)] + ['G,0,%d' % a_ for a_ in range(4)]
        wm_bad, wm_n, wm_x, WMAP = [], 0, 0, {}
        for k_ in W2_MIR:                                                   # every W2 key the bars read outside the Gram role, both ends
            for end_ in (0, 1):
                fs_ = ITEMS_[('W2', k_)]['factors']
                try:
                    WMAP[(k_, end_, 'K')] = mirror_name(fs_, end_, 'K')
                    wm_n += 1
                    if U.junction_bonds(fs_, end_, 1 - end_):
                        WMAP[(k_, end_, 'Kxi')] = mirror_name(fs_, end_, 'Kxi')
                        wm_x += 1
                except ValueError as e_:
                    wm_bad.append(str(e_)[:90])
        gate('C-W2M-MAP', not wm_bad and set(WMAP.values()) <= set(W2M_WINDOWS), 'the W2 ends the bars read (%d keys outside the Gram role, '
             '%d ends, %d bond ends) each map to one of the W2M record\'s windows by the mirror rule: %d windows used (%s); problems %s' % (
                 len(W2_MIR), wm_n, wm_x, len(set(WMAP.values())), ' '.join(sorted(set(WMAP.values()))), wm_bad[:2] or 'none'))
        fw1, ww1 = refused(mirror_name, ITEMS_[('W2', 'G,1,2')]['factors'], 1, 'K')
        fw2, ww2 = refused(mirror_name, [['p', 0], ['xi', [1, 4]], ['p', 1]], 0, 'Kxi')
        plant('PLANT-W2M-MAP', fw1 and fw2, 'the same rule refuses G,1,2 at end 1 (two st in the rest: %s) and an M-row bond end (%s)' % (
            ww1[:60], ww2[:60]))
        if MODE == 'mock':                                                  # cert mode's mirror code on the dry W2M record
            T_f = L.piece_T(EXP[PF][0], EXP[PF][1])
            mm_bad, mm_w = [], 0.0
            for (k_, end_, kind_), w_ in sorted(WMAP.items()):
                cm_ = cert_mirror('W2', k_, end_, kind_, 'model', T_f)
                mk_ = mock_mirror('W2', k_, end_, kind_, 'model')
                mm_w = max(mm_w, float(cm_.rad()))
                if not (L.fin(cm_) and bool(cm_.contains(mk_))):
                    mm_bad.append('%s e%d %s' % (k_, end_, kind_))
            gate('C-CERT-MIRROR', not mm_bad, 'DRY: cert mode\'s W2 mirror (W[window]/W[Z] of the dry W2M record over P%04d\'s t-ball) holds '
                 'the mock mirror at each of the %d W2 end reads (largest radius %.2e); misses %s' % (PF, len(WMAP), mm_w, mm_bad[:3] or 'none'))

        def wmean_centres(pc):
            """the v1 mock's centre (float window means of W2's CE, CF at the piece centre, as points): G-C must refuse it (PLANT-GC-WMEAN)."""
            jlo, jhi = EXP[pc]
            tc = arb(L.piece_T(jlo, jhi).mid())
            ce = U.farb(Fraction('%.12g' % float(ratio('W2', 'CE', tc).mid())))
            cf = U.farb(Fraction('%.12g' % float(ratio('W2', 'CF', tc).mid())))
            return {'c_e': ce, 'c_f': cf, 'c_t': ce, 'c_bb': cf, 'cls': 'D3', 'pc': pc}

        PINNED = bool(RULING_22) and FULL['ruling22'] == RULING_22.split(':')[1]
        J2 = 2 * arb(300)
        B1 = U.up(1 / U.lo(1 - s2))
        TRB_J, A2_J = U.up(TRBc / U.lo(1 - eps_r)), U.up(A2c / U.lo(1 - eps_r))

        def beta2_of(fam, k_):
            """column 2's beta_2 and its source (ADD3 sect. 2): 1/(1 - s^2) for k = 0; with the pin on 965f72f0 N*_TRB/(1 - eps_r) (k = 1)
            and N*_A2/(1 - eps_r) (k = 2), else the sup form (2 J_W)^k/(1 - s^2)."""
            kk = U.int_degree(fam, ITEMS_[(fam, k_)]['factors'])
            if kk == 0:
                return B1, 'beta(1)'
            if PINNED:
                return (TRB_J, 'N*_TRB') if kk == 1 else (A2_J, 'N*_A2')
            if kk == 2:
                raise ValueError('C-K3-OP: %s:%s without the pin on 965f72f0: the sup form (2J)^2 grows like J in a first-order term '
                                 '(ADD4 sect. 4)' % (fam, k_))
            return U.up(J2 * B1), 'sup(2J)^1'

        def beta2sq_of(fam, k_, e_end):
            """(beta_2 of f_2^2)^(1/2) for a bonded far link (ADD3 sect. 2-3): k = 0 (1/(1 - s^2))^(1/2); k = 1 (N*_A2/(1 - eps_r))^(1/2)
            with the pin, else 2 J_W (1/(1 - s^2))^(1/2); k = 2, the A4 spot, the route of record (A4 cancelled): 2 J_W (N*_A2/(1 - eps_r))^(1/2)
            (xi45^4 <= (2J)^2 xi45^2) with the pin, refused without it."""
            kk = U.int_degree(fam, ITEMS_[(fam, k_)]['factors'])
            if kk == 0:
                return U.up(B1.sqrt()), 'beta(1)^1/2'
            if kk == 1:
                return (U.up(A2_J.sqrt()), 'N*_A2^1/2') if PINNED else (U.up(J2 * B1.sqrt()), 'sup(2J)^1')
            if A4_PIN is not None or not PINNED:
                raise ValueError('C-K3-A4: %s:%s: the A4 spot takes 2 J_W (N*_A2/(1 - eps_r))^(1/2) with the pin and nothing else (A4 '
                                 'cancelled; A4_PIN %r, pin %s)' % (fam, k_, A4_PIN, PINNED))
            return U.up(J2 * A2_J.sqrt()), '2J N*_A2^1/2'
        GT = {}                                                             # FA's g (ADD5 sect. 1), MOCK: S8's float chain
        for ln in open(F['s8h']).read().split('\n'):
            f_ = ln.split('\t')
            if len(f_) >= 5 and f_[0] == str(N) and re.fullmatch(r'g,[0-3],[0-3]', f_[1]):
                GT[f_[1]] = (Fraction(f_[3]), Fraction(f_[4]))
        FA_G = {j: max(GT['g,%d,%d' % (j, j)][0] / GT['g,0,0'][0], GT['g,%d,%d' % (j, j)][1] / GT['g,0,0'][1]) for j in range(U.BPRIME_J)}

        def fa_T(fam, k_):
            """||T_{f_1}||/mu_R and ||T_{f_1^2}||/mu_R on FA's int column (ADD5 sect. 1): 1/(1 - s^2) when f_1 = 1; with xi(4,5) the J-free
            N*_TRB/(1 - eps_r) and N*_A2/(1 - eps_r), only with the pin on 965f72f0."""
            if U.int_degree(fam, ITEMS_[(fam, k_)]['factors']) == 1:
                if not PINNED:
                    raise ValueError('C-FA-OPS: %s:%s needs the pin on 965f72f0 for its xi(4,5) traces' % (fam, k_))
                return TRB_J, A2_J, 'N*_TRB,N*_A2'
            return B1, B1, 'beta(1)'

        def fa_g_cert(j):
            """cert mode's g = g_jj/g_00: 1 exactly at j = 0, else the GJJ export v1_1's N<N>_MAX u_j as an upper end (C-GJJ, C-FA-G)."""
            return (arb(1), 'g_00/g_00') if j == 0 else (U.up(U.farb(GJJ_MAX[j - 1])), 'GJJ_EXPORT_v1_1 N%d_MAX' % N)

        def fa_g(fam, k_):
            """g = g_jj/g_00 (ADD5 sect. 1): MOCK from S8's float chain (TABLE_S8H_FLOAT_VALUES_v1_1, the larger of the a_0 and J = 300
            ratios, a planning value); cert from fa_g_cert."""
            j = int(k_.split(',')[1])
            if j not in FA_G:
                raise ValueError('C-FA-OPS: %s:%s has no g_jj (v_hat_raw.0..%d only)' % (fam, k_, U.BPRIME_J - 1))
            if MODE == 'cert':
                return fa_g_cert(j)
            return U.up(U.farb(FA_G[j])), 'S8H_float_MOCK'

        def fa_g_bad(gfun, gkv):
            """C-FA-G: the g of cert mode's FA rests is 1 exactly at j = 0 and, for j = 1..3, at least the largest upper
            end u_j on the set's piece lines of the GJJ export (recomputed from the lines, not read from N<N>_MAX)."""
            us = [[Fraction(x_) for x_ in gkv['N%d_P%04d' % (N, pc)].split()[2:5]] for pc in PCS]
            bad_ = []
            for j in range(U.BPRIME_J):
                g_, _ = gfun(j)
                ok_ = bool(g_ == 1) if j == 0 else (L.end_frac(arb(g_).lower()) >= max(u_[j - 1] for u_ in us))
                if not ok_:
                    bad_.append('j = %d' % j)
            return bad_
        FA_OPS = {'T': fa_T, 'g': fa_g, 'lam0': B1}
        GB_CACHE = {}

        def farf_of(T, cc, J_lo):
            """G_33^(1/2) of an end's far end (ADD3 sect. 1): W2's G,b,b in the gram role (the k = 1 model's G_bb, upper end) for a state
            st_b, G_00 = 1; the A2 trace (N*_A2/(1 - eps_r))^(1/2) for D4ML0's xi(7,8) on a vac column; 1 when f_3 = 1."""
            def f_(fam, k_, e_end):
                facs = ITEMS_[(fam, k_)]['factors']
                far = 2 if e_end == 0 else 0
                if fam == 'W3e':
                    sts_ = [f[1] for f in facs if f[0] == 'st' and f[2] == far]
                    if not sts_ or sts_[0] == 0:
                        return arb(1)
                    gk = (str(T), sts_[0])
                    if gk not in GB_CACHE:
                        Eg = E_pair('W2', 'G,%d,%d' % (sts_[0], sts_[0]), 'gram', T, cc, J_lo)[0]
                        GB_CACHE[gk] = U.up(U.up(Eg).sqrt())
                    return GB_CACHE[gk]
                if fam == 'D4ML0' and any(f[0] == 'xi' and f[1][0] // 3 == far and f[1][1] // 3 == far for f in facs):
                    if not PINNED:                                  # the 2.2 trace step (ADD4 sect. 4)
                        raise ValueError('C-K3-OP: D4ML0:%s far-end xi(7,8) trace needs the pin on 965f72f0' % k_)
                    return U.up(A2_J.sqrt())
                return arb(1)
            return f_
        HB, OMH = U.up(A * B1), U.up(B1.sqrt())                    # F4's A lambda_0/mu_R; lambda_0^(1/2)/mu_R^(1/2)
        EPS_CACHE, KREC = {}, {}

        def bars_of(fam, k_, role, T, cc, J_lo):
            """(b_e, b_0, detail) of (entry, role) on the piece T; b_0 is the empty key's b_e in the same role."""
            it = ITEMS_[(fam, k_)]
            ctx_ = {'columns': it['columns'], 'A': A, 'MU': MU, 's2': s2, 'eps_r': eps_r, 'J_W': arb(300), 'c_R': A, 'c_far': U.up(abs(cc['c_e'])),
                    'beta2': beta2_of, 'beta2sq': beta2sq_of, 'farf': farf_of(T, cc, J_lo), 'hb': HB, 'om_half': OMH, 'fa_ops': FA_OPS}
            MIR = lambda f_, k2, e2, kind, tr: MIRF(f_, k2, e2, kind, tr, T)
            be, det = U.entry_bars(fam, k_, role, it['factors'], S, EK, MIR, ctx_)
            ekey = (fam, EMPTY[fam] if role != 'gram' else 'G,0,0', role)
            if ekey not in EPS_CACHE or EPS_CACHE[ekey][0] is not T:
                it0 = ITEMS_[(ekey[0], ekey[1])]
                b0_, _ = U.entry_bars(ekey[0], ekey[1], role, it0['factors'], S, EK, MIR, dict(ctx_, columns=it0['columns']))
                EPS_CACHE[ekey] = (T, b0_)
            return be, EPS_CACHE[ekey][1], det

        def E_pair(fam, k_, role, T, cc, J_lo):
            """the u-hat quantity E = R~ (F_k + [-b_0, b_0]) + [-b_e, b_e] on the piece T: (centre ball at t_c with the piece's remainder,
            Dual over T for the centered form, b_e, b_0, detail)."""
            be, b0, det = bars_of(fam, k_, role, T, cc, J_lo)
            KREC[(fam, k_, role)] = det['k']
            if fam == 'W2' and k_ == 'G,0,0' and role == 'gram':
                return arb(1), L.Dual(arb(1), arb(0)), arb(0), arb(0), det       # G_00 = 1 exactly (ADD1 sect. 1)
            Fk = U.fk_ball(det['k'], s2)
            Rc, Rd = ratio_pair(fam, k_, T)
            mult = Fk + U.UNIT * b0
            return Rc * mult + U.UNIT * be, Rd * mult + U.UNIT * be, be, b0, det

        def ratio_pair(fam, k_, T, exact=True):
            """R~ = the entry over its family's empty key on the piece T: (the centre ball at t_c with the piece's remainder, the Dual over T).
            The empty key over itself is the same record value, so its ratio is 1 exactly (exact=False: the interval quotient, PLANT-ZZ)."""
            if exact and k_ == EMPTY[fam]:
                return arb(1), L.Dual(arb(1), arb(0))
            tc, trem = arb(T.mid()), T.upper()
            cn, ce_ = ITEMS_[(fam, k_)]['co'], ITEMS_[(fam, EMPTY[fam])]['co']
            return (L.entry_center(cn[0], cn[1], tc, trem, 0.0) / L.entry_center(ce_[0], ce_[1], tc, trem, 0.0),
                    L.entry_dual(cn[0], cn[1], T, trem, 0.0) / L.entry_dual(ce_[0], ce_[1], T, trem, 0.0))

        def zz_ok(Rc, Rd):
            """C-ZZ's test: the ratio is the exact point 1, its t-derivative the exact point 0."""
            return Rc.is_exact() and bool(Rc == 1) and Rd.v.is_exact() and bool(Rd.v == 1) and Rd.d.is_exact() and bool(Rd.d == 0)
        # C-ZZ ((a) of the route-0 analysis): the empty key over itself is 1 exactly, with a bar on the empty key
        T_z = L.piece_T(EXP[PF][0], EXP[PF][1])
        zz_bad, zz_plant = [], []
        for g_ in R0B_FAMS:
            ek_ = (g_, EMPTY[g_])
            sv_ = ITEMS_[ek_]['co']
            ITEMS_[ek_]['co'] = (sv_[0], U.up(U.farb(Fraction(1, 10000))))
            try:
                if not zz_ok(*ratio_pair(g_, EMPTY[g_], T_z)):
                    zz_bad.append(g_)
                if not zz_ok(*ratio_pair(g_, EMPTY[g_], T_z, exact=False)):
                    zz_plant.append(g_)
            finally:
                ITEMS_[ek_]['co'] = sv_
        gate('C-ZZ', not zz_bad, 'each family\'s empty key over itself is 1 exactly in E_pair, with a 1e-4 bar on the empty key at P%04d (%s); '
             'not exact %s' % (PF, ' '.join('%s:%s' % (g_, EMPTY[g_]) for g_ in R0B_FAMS), zz_bad or 'none'))
        plant('PLANT-ZZ', len(zz_plant) == len(R0B_FAMS), 'the interval quotient of the empty key by itself (the old form) is not exact, and the '
              'same test refuses it for %d of the %d families' % (len(zz_plant), len(R0B_FAMS)))

        def E_of(fam, k_, role, T, cc, J_lo):
            Ec, _, be, b0, det = E_pair(fam, k_, role, T, cc, J_lo)
            return Ec, be, b0, det

        def centred(c, d, T):
            """the centered form over T: the centre ball plus the Dual's t-derivative times [-Delta, Delta]."""
            return c + d.d * (U.UNIT * T.rad())

        # ------------------------------------------------------------ G-BAR over every (key, role) used, C-NOX, C-R2-POS plant
        T300 = L.piece_T('300', None)
        cc300 = gc_use(centres_at(PF, 'D3'))                              # the structural checks at the set's first piece (J >= 300 bars)
        ref0 = centres_at(PF, 'D3')
        wid = U.up(ref0['c_e']) - U.lo(ref0['c_e'])
        gpt = dict(ref0, c_e=arb(ref0['c_e'].mid()), c_f=arb(ref0['c_f'].mid()))
        gsh = dict(ref0, c_e=ref0['c_e'] + wid, c_f=ref0['c_f'] + wid)
        gwm = wmean_centres(PF)
        plant('PLANT-GC-POINT', not gc_ok(gpt), 'P%04d\'s D3 ball midpoints as points are refused' % PF)
        plant('PLANT-GC-SHIFT', not gc_ok(gsh), 'P%04d\'s D3 balls moved by their own width (%.3e) are refused' % (PF, float(wid)))
        plant('PLANT-GC-WMEAN', not gc_ok(gwm), 'the v1 mock\'s centre at P%04d (float window means of W2 CE, CF: %.10f, %.10f) is refused' % (
            PF, float(gwm['c_e']), float(gwm['c_f'])))
        used =[('W2', 'G,%d,%d' % (a, b), 'gram') for a in range(4) for b in range(a, 4)] + \
               [('W2', 'G,0,%d' % a, 'vcomp') for a in range(4)] + \
               [('W2', k_, 'entry') for k_ in ['Z', 'CE', 'CF'] + ['V,%d' % a for a in range(4)] + ['KE,%d' % a for a in range(4)] +
                ['K1,%d' % a for a in range(4)]] + \
               [('W3e', 'Z', 'entry'), ('W3e', 'ME2', 'entry')] + \
               [('W3e', 'M,%d,%d,%s' % (a, b, s_), 'entry') for a in range(4) for b in range(a, 4) for s_ in ('ee', 'e1', 'e2', '00')] + \
               [('W3f', k_, 'entry') for k_ in ('Z', 'FF', 'F1', 'F2')] + \
               [(fam, k_, 'entry') for (fam, k_) in ITEMS_ if fam in ('D4L0', 'D4ML0')] + \
               [('FA', '%s,%d' % (pre, j), 'entry') for j in range(U.BPRIME_J) for pre in ('1', 'T', 'B', 'X')]
        gb_bad, degs, forms = [], {}, {}
        K3_DET, FA_DET = {}, {}
        for fam, k_, ro in used:
            try:
                _, be, b0, det = E_of(fam, k_, ro, T300, cc300, arb(300))
                degs[(fam, k_, ro)] = max(d['deg'] for d in det['ends'].values())
                forms[det.get('k')] = forms.get(det.get('k'), 0) + 1
                if fam in U.K3_FAMS:
                    K3_DET[(fam, k_)] = det
                if fam == 'FA':
                    FA_DET[(fam, k_)] = det
            except ValueError as e_:
                gb_bad.append('%s:%s/%s %s' % (fam, k_, ro, e_))
        gate('G-BAR', not gb_bad and max(degs.values()) <= 2, '%d (key, role) pairs: every end weight of degree <= 2 (largest %d), every '
             'eps from M2B\'s identity or the xi-only keys, every bond at a row link, at most one bond per junction; refusals %s' % (
                 len(used), max(degs.values()) if degs else -1, gb_bad[:3] or 'none'))
        it44 = ITEMS_.get(('W2', 'G,4,4'))
        f44, w44 = refused(U.eps_insertion, U.column_poly(it44['factors'], 0, S), EK) if it44 else (False, 'G,4,4 not in the list')
        plant('PLANT-GBAR-DEG', f44, 'the info key G,4,4 (end weight st_4^2, degree 4) is refused: %s' % w44)
        gate('C-NOX', not any(k_.startswith('XT') for k_ in EK), 'no X-factor key is read: the eps table holds %s' % ', '.join(sorted(EK)))
        fr, wr = refused(U.rest_P, A, arb(1), arb('1.6'), arb(1))
        plant('PLANT-R2POS', fr, 'W_xi[mirror] raised to 1.6 R[mirror] at m = A = %s: %s' % (A.str(3), wr))
        f_r1, w_r1 = refused(U.junction_bonds, [['xi', [0, 4]]], 0, 1)
        f_r2, w_r2 = refused(U.junction_bonds, [['xi', [0, 3]], ['xi', [2, 5]]], 0, 1)
        plant('PLANT-R1-SAMEROW', f_r1 and f_r2, 'a bond on a non-row link (0, 4): %s; bonds on two rows at one junction: %s' % (w_r1, w_r2))
        # C-K3-MONO: the n + 1 rate conditions for every eps law in a k = 3 second-order term (ADD1 sect. 4)
        lam_x = Fraction(wkv['N%d_W_LAMSTAR_X_A' % N].split()[0])
        aeF = Fraction(kn['AE'][0])
        kapB = Fraction(rec['const']['KAPPA_B'][0])
        lamX_r1 = Fraction(kn['TX_LAMSTAR'][0])
        farc_v1 = Fraction(rec['const']['A_M'][0]) / 2            # LAW v1's far factor e^(-0.5 a_m (J - 150))
        farc_w = Fraction(3, 10)                                   # below FAR_CRUDE_v1's c = binary64(0.3025) (NOTE_M2B_WEIGHTED_LAWS_v1 l.72)
        g_rate = Fraction(95, 100) * Fraction(1 - math.cos(math.radians(40))) / 2

        def mono_ok(n_, lam, ae, kb, far_c, far_p, gr):
            m1 = n_ + 1
            return (Fraction(m1, 300) < lam * ae / 2 and Fraction(m1, 300) < Fraction(45, 100) * kb / 2 and
                    Fraction(2 * m1 + far_p, 300) < far_c and Fraction(m1 + 1, 300) < gr)
        laws = (('eps_r (LAW v1)', 0, lamX_r1, farc_v1), ('eps_w, eps_d (LAW v1)', 1, lamX_r1, farc_v1),
                ('xi-only keys (LAW-W v1, n <= 2)', 2, lam_x, farc_w))
        conds = [(nm, mono_ok(n_, lam, aeF, kapB, fc, 2, g_rate)) for nm, n_, lam, fc in laws]
        gate('C-K3-MONO', all(c for _, c in conds), 'J eps(J) nonincreasing on [300, inf) for each eps law of the k = 3 second-order terms, '
             'each at its own rates with n + 1 (tails (n + 1)/300 < lam* a_e/2 and 0.45 kappa_B/2, far (2 (n + 1) + p)/300 < c, '
             'g (n + 2)/300 < 0.95 (1 - cos 40 deg)/2; a_e, kappa_B, a_m and lam* from the records): %s' % ', '.join('%s %s' % c for c in conds))
        plant('PLANT-K3-MONO-TAIL', not mono_ok(2, Fraction(1, 1000), aeF, kapB, farc_w, 2, g_rate), 'a tail rate lam* = 0.001 breaks '
              '(n + 1)/300 < lam* a_e/2 for n = 2')
        plant('PLANT-K3-MONO-FAR', not mono_ok(2, lam_x, aeF, kapB, Fraction(1, 1000), 2, g_rate), 'a far rate c = 0.001 breaks '
              '(2 (n + 1) + p)/300 < c for n = 2')
        plant('PLANT-K3-MONO-G', not mono_ok(2, lam_x, aeF, kapB, farc_w, 2, Fraction(1, 1000)), 'a g rate bound 0.001 breaks '
              '(n + 2)/300 < 0.95 (1 - cos 40 deg)/2 for n = 2')
        # C-K3-DECOMP, C-K3-OP, C-K3-A4 on every k = 3 detail (ADD3 sect. 4): true-V rests, labels recomputed from the factors, sources
        k3_keys = sorted(set((f_, k_) for (f_, k_, ro) in used if f_ in U.K3_FAMS))
        k3_bad = []
        for x in k3_keys:
            try:
                U.k3_check(x[0], x[1], ITEMS_[x]['factors'], K3_DET[x], PINNED)
            except (ValueError, KeyError) as e_:
                k3_bad.append('%s:%s %s' % (x[0], x[1], str(e_)[:120]))
        rcount = {}
        for x in k3_keys:
            for e_end, d_ in sorted(K3_DET.get(x, {'ends': {}})['ends'].items()):
                tag = (x[0], 'R' if d_['jbond'] else 'T', d_['route'], d_['b2_src'], d_['b2sq_src'])
                rcount[tag] = rcount.get(tag, 0) + 1
        a4s = sorted('%s:%s end %d' % (x[0], x[1], e_) for x in k3_keys for e_, d_ in K3_DET[x]['ends'].items() if d_['a4_spot'])
        gate('C-K3-OP', not k3_bad and len(K3_DET) == len(k3_keys) and A4_PIN is None, '%d k = 3 keys (pin 965f72f0 %s, A4 %s); every first-order rest ends in the '
             'true V column (C-K3-DECOMP), its labels match the factors, its sources follow ADD3 sect. 2-3 (C-K3-A4): %s; A4 spots %s; bad %s' % (
                 len(k3_keys), 'read' if PINNED else 'NOT pinned', 'cancelled (the 2J form is the route of record)' if A4_PIN is None else
                 'PINNED %r: refused' % A4_PIN,
                 ', '.join('%s %s %s %s %s x%d' % (t + (n_,)) for t, n_ in sorted(rcount.items())), a4s, k3_bad[:3] or 'none'))
        it_l = next(k_ for (f_, k_) in ITEMS_ if f_ == 'D4L0' and k_.endswith('2'))
        bad_ctx = {'columns': ITEMS_[('D4L0', it_l)]['columns'], 'A': A, 'MU': MU, 's2': s2, 'eps_r': eps_r, 'J_W': arb(300), 'c_R': A,
                   'c_far': arb(1)}
        fk3, wk3 = refused(U.entry_bars, 'D4L0', it_l, 'entry', ITEMS_[('D4L0', it_l)]['factors'], S, EK,
                           lambda *a_: mock_mirror(*a_), bad_ctx)
        plant('PLANT-K3-OP', fk3, 'a D4L0 end without the operator factors (no beta2 in the context) is refused: %s' % wk3)
        f101 = ITEMS_[('D4L0', 'E101')]['factors']
        plant('PLANT-K3-OP-SRC', not U.k3_src_ok('D4L0', 'E101', f101, 'N*_TRB', False), 'a non-E112 D4L0 k = 1 term (E101) with N*_TRB and no '
              'pin is refused')
        # plants that rerun the code on perturbed inputs
        x1 = ('W3e', 'M,0,0,e1')
        fac1 = ITEMS_[x1]['factors']
        fac1_p = [f for f in fac1 if not (f[0] == 'xi' and tuple(f[1]) == (0, 3))]          # the junction bond dropped
        ctx_p = {'columns': ITEMS_[x1]['columns'], 'A': A, 'MU': MU, 's2': s2, 'eps_r': eps_r, 'J_W': arb(300), 'c_R': A,
                 'c_far': U.up(abs(cc300['c_e'])), 'beta2': beta2_of, 'beta2sq': beta2sq_of, 'farf': farf_of(T300, cc300, arb(300)), 'hb': HB,
                 'om_half': OMH, 'fa_ops': FA_OPS}
        _, det_p = U.entry_bars(x1[0], x1[1], 'entry', fac1_p, S, EK, lambda *a_: mock_mirror(*a_), ctx_p)
        frt, wrt = refused(U.k3_check, x1[0], x1[1], fac1, det_p, PINNED)
        plant('PLANT-K3-ROUTE', frt, 'the bars of W3e M,0,0,e1 computed from its factor list without the junction bond (which drops '
              '(2A + |A - c| + |c|)) are refused against the item\'s own factors: %s' % wrt)
        U1, _ = load_mod(OWN + '/uhat_lib_v1.py', '1e32223037ca4f890d7b59f73ee8b8dfcda2018214c4466a122cd1b13f3c1cfa', 'uhat_lib_v1')
        ctx_v1 = dict(ctx_p, beta2=lambda f_, k_: (B1, 'beta(1)'), ruling_22=True)
        _, det_v1 = U1.entry_bars(x1[0], x1[1], 'entry', fac1, S, EK, lambda *a_: mock_mirror(*a_), ctx_v1)
        fdc, wdc = refused(U.k3_check, x1[0], x1[1], fac1, det_v1, PINNED)
        plant('PLANT-K3-DECOMP', fdc, 'W3e M,0,0,e1\'s bars from uhat_lib_v1 (a0d0a5e2: the two-term form, F~ at the far end of a bonded '
              'junction) are refused: %s' % wdc)
        f112 = ITEMS_[('D4L0', 'E112')]['factors']
        plant('PLANT-K3-A4', not U.k3_sq_src_ok('D4L0', 'E112', f112, 0, 'N*_A2^1/2', True), 'the A2 factor (N*_A2^1/2) used for xi45^4 at '
              'E112\'s A4 spot is refused')
        A4_SAVE = globals()['A4_PIN']
        globals()['A4_PIN'] = 'pk08/A4_TRACE_PLANT.md:' + '0' * 64
        fpin, wpin = refused(beta2sq_of, 'D4L0', 'E112', 0)
        globals()['A4_PIN'] = A4_SAVE
        plant('PLANT-K3-A4-PIN', fpin and not U.k3_sq_src_ok('D4L0', 'E112', f112, 0, 'N*_A4^1/2', True), 'an A4 pin offered to the A4 '
              'spot (beta2sq_of rerun with A4_PIN set) and an N*_A4 source are refused: %s' % wpin)
        A4_EXPECT = {('D4L0', 'E012'), ('D4L0', 'E102'), ('D4L0', 'E112')}

        def a4_keys(facs_of):
            return set(x for x in k3_keys if any(U.a4_spot(x[0], facs_of(x), e_) for e_ in U.FAM_ENDS[x[0]]))
        a4set = a4_keys(lambda x: ITEMS_[x]['factors'])
        gate('C-K3-A4', a4set == A4_EXPECT and A4_PIN is None, 'the A4-spot key set derived from the factors (column 2 of degree 2 next to a '
             'bonded far link): %s; expected %s; A4 cancelled, no A4 pin (%r)' % (sorted(a4set), sorted(A4_EXPECT), A4_PIN))
        f002p = ITEMS_[('D4L0', 'E002')]['factors'] + [['xi', [3, 6]]]
        a4p = a4_keys(lambda x: f002p if x == ('D4L0', 'E002') else ITEMS_[x]['factors'])
        plant('PLANT-K3-A4-SET', a4p != A4_EXPECT, 'D4L0 E002\'s factor list given a far-link bond makes the same derivation find a fourth key '
              '(%s), which is refused' % sorted(a4p - A4_EXPECT))
        # C-K3-COUNT: the both-bond keys per shape (04dc9e2d sect. 1), each with a two-bond Delta-Delta term

        def both_count(facs_of):
            bs = set(x for x in k3_keys if U.both_bonds(x[0], facs_of(x)))
            return bs, {f_: sum(1 for x in bs if x[0] == f_) for f_ in BOTH_BOND_COUNT}
        both, bcount = both_count(lambda x: ITEMS_[x]['factors'])
        r24 = set(x for x in k3_keys if K3_DET[x]['dd_bonds'] == 2)
        gate('C-K3-COUNT', bcount == BOTH_BOND_COUNT and r24 == both, 'both-bond keys %s (04dc9e2d sect. 1: %s); each carries the two-bond '
             'Delta-Delta term (2J at J_W, C-K3-MONO): %s' % (bcount, BOTH_BOND_COUNT, r24 == both))
        xb = sorted(both)[0]
        fxb_p = [f for f in ITEMS_[xb]['factors'] if not (f[0] == 'xi' and tuple(f[1]) in ((3, 6), (5, 8)))]
        _, bcp = both_count(lambda x: fxb_p if x == xb else ITEMS_[x]['factors'])
        plant('PLANT-K3-COUNT', bcp != BOTH_BOND_COUNT, 'with %s\'s far-link bond removed from its factor list, the same count gives %s, which is '
              'refused' % (xb, bcp))
        # C-FA-OPS (ADD5 sect. 2): FA's form, sources and value against ADD5 recomputed from the pinned inputs
        fa_bad = []
        for x in sorted(FA_DET):
            try:
                Tf1_, Tf1sq_, _ = fa_T(x[0], x[1])
                g_, _ = fa_g(x[0], x[1])
                U.fa_check(x[0], x[1], ITEMS_[x]['factors'], FA_DET[x], PINNED, Tf1_, Tf1sq_, g_, B1, A)
            except (ValueError, KeyError) as e_:
                fa_bad.append('%s:%s %s' % (x[0], x[1], str(e_)[:120]))
        fforms = {}
        for x in FA_DET:
            d_ = FA_DET[x]['ends'][2]
            fforms[(d_['form'], d_['T_src'], d_['c'])] = fforms.get((d_['form'], d_['T_src'], d_['c']), 0) + 1
        gate('C-FA-OPS', not fa_bad and len(FA_DET) == 4 * U.BPRIME_J, '%d FA keys (j = 0..%d) by operators (ADD5): %s; g_jj/g_00 %s (%s); '
             'bad %s' % (len(FA_DET), U.BPRIME_J - 1, ', '.join('%s %s %s x%d' % (t + (n_,)) for t, n_ in sorted(fforms.items())),
                         ', '.join('%.12f' % float(fa_g('FA', 'T,%d' % j)[0].upper()) for j in range(U.BPRIME_J)),
                         'cert: the GJJ export\'s N%d_MAX' % N if MODE == 'cert' else 'MOCK: S8\'s float chain', fa_bad[:3] or 'none'))
        fgb = fa_g_bad(fa_g_cert, GKV)
        gate('C-FA-G', not fgb, 'cert mode\'s g for FA (fa_g_cert; %s): j = 0 gives 1 exactly, j = 1..3 give %s, each at least the largest u_j '
             'on the %d piece lines P%04d..P%04d of the GJJ export v1_1; problems %s' % (
                 'the bars use it' if MODE == 'cert' else 'checked here, the MOCK bars use S8\'s float chain',
                 ' '.join('%.17g' % float(fa_g_cert(j)[0].upper()) for j in range(1, U.BPRIME_J)), len(PCS), PF, PL, fgb or 'none'))
        plant('PLANT-FA-G', fa_g_bad(lambda j: (arb(1), '-') if j == 0 else (U.farb(GJJ_MAX[j - 1] * Fraction(999999, 1000000)), '-'), GKV) ==
              ['j = 1', 'j = 2', 'j = 3'], 'the same check refuses g values 1e-6 below the GJJ export\'s N%d_MAX at j = 1..3' % N)
        fer, wer = refused(U.fa_rest, A, 'FA-ER', B1, B1, U.farb(FA_G[1]), B1)
        plant('PLANT-FA-ER', fer, 'an E-R rest factor offered for an FA bond key is refused by fa_rest: %s' % wer)
        xt = ('FA', 'T,1')
        g1, _ = fa_g('FA', 'T,1')
        b1_ = U.up(B1 * g1.sqrt())
        rest4 = U.up(U.up(2 * A * B1 * g1).sqrt() + A * b1_)               # ADD4's display at c = A: no lambda_0, no end factor
        dlam = {'ends': {2: dict(FA_DET[xt]['ends'][2], rest=rest4)}}
        flam, wlam = refused(U.fa_check, 'FA', 'T,1', ITEMS_[xt]['factors'], dlam, PINNED, B1, B1, g1, B1, A)
        plant('PLANT-FA-LAMBDA', flam, 'ADD4\'s display for FA T,1 (%.4f per eps_r, without lambda_0 and the end factor) is refused against '
              'ADD5\'s %.4f: %s' % (float(rest4), float(FA_DET[xt]['ends'][2]['rest']), wlam))
        # ------------------------------------------------------------ route 0 per row (route P for D3, U4 at the site)
        NONFIN = []

        def finchk(tag, xs):
            for x in xs:
                if not L.fin(x):
                    NONFIN.append(tag)
                    return

        def chain_at(pc):
            """route 0 on piece pc by the centered form: the chain on the centre balls and on the Duals over T."""
            jlo, jhi = EXP[pc]
            T = L.piece_T(jlo, jhi)
            cc = gc_use(centres_at(pc, 'D3'))
            Jl = arb(jlo)
            Ep = {}

            def pair(g, k_, ro):
                key_ = (g, k_, ro)
                if key_ not in Ep:
                    Ep[key_] = E_pair(g, k_, ro, T, cc, Jl)
                return Ep[key_]
            rc = U.chain_uhat(lambda g, k_, ro: pair(g, k_, ro)[0], cc['c_e'], cc['c_f'])
            rv = U.chain_uhat(lambda g, k_, ro: pair(g, k_, ro)[1], cc['c_e'], cc['c_f'], sqf=L.sq, cholf=L.chol)
            r = {'G': rc['G'], 'pd': rc['pd'] and rv['pd'], 'why': rc['why'] or rv['why'], 'Ep': Ep}
            finchk('piece %d' % pc, [x for row in rc['G'] for x in row] + rc['v'] + rc['KE'] + [rc['Eh2']])
            if r['pd']:
                bMb, hp2 = centred(rc['bMb'], rv['bMb'], T), centred(rc['hp2'], rv['hp2'], T)
                r.update(bMb=bMb, hp2=hp2, **U.q_hat(bMb, hp2, cc['c_e'], A, s2))
                if 'stop' in r:
                    r.update(pd=False, why=r['stop'])
                finchk('piece %d q' % pc, [bMb, hp2])
            return r, cc, T
        # route 0 at every piece of the set (ADD3 sect. 6): q-hat depends on the piece only; each row's J-uniform value is the max over PCS
        PCREC, nstop_pc = {}, []
        for pc in PCS:
            r, cc, T = chain_at(pc)
            if not r['pd']:
                nstop_pc.append((pc, r['why']))
                continue
            qh = r['q_hat_hi']
            bs = U.beta_D3(A, cc['c_t'], cc['c_bb'], s2, 2)
            m_abs = bs                                                          # beta-hat fallback
            xu = U.up((qh * qh + m_abs * m_abs).sqrt())
            Ts = U.u4_T(sp, bs, m_abs, xu, bs)
            PCREC[pc] = {'q_hat_hi': qh, 'Ps': r['Ps'], 'beta_s': bs, 'm_abs': m_abs, 'xu': xu, 'T_s': Ts, 'q_true': U.route_P(qh, Ts)}
        wpc = None
        for pc_, x_ in PCREC.items():
            if wpc is None or bool(x_['q_true'] > PCREC[wpc]['q_true']):
                wpc = pc_
        AGG = {}
        if PCREC:                                                           # ADD4 sect. 3: each part its own max, q the form at those parts
            AGG = {f_: U.amax_up(*[x_[f_] for x_ in PCREC.values()]) for f_ in ('q_hat_hi', 'Ps', 'beta_s', 'm_abs')}
            AGG['xu'] = U.up((AGG['q_hat_hi'] * AGG['q_hat_hi'] + AGG['m_abs'] * AGG['m_abs']).sqrt())
            AGG['T_s'] = U.u4_T(sp, AGG['beta_s'], AGG['m_abs'], AGG['xu'], AGG['beta_s'])
            AGG['q_true'] = U.route_P(AGG['q_hat_hi'], AGG['T_s'])
        if PCREC:
            out('ROUTE0 N%d over P%04d..P%04d (%d pieces, %d stop): q-hat_b max %.6e, T_s max %.4e, q_true max %.6e at P%04d (route P, '
                'beta-hat_s fallback)' % (N, PF, PL, len(PCS), len(nstop_pc), float(AGG['q_hat_hi']), float(AGG['T_s']), float(AGG['q_true']),
                                          wpc))
        rtxt = open(F['rows']).read()                                       # the reader's pinned row list (INTERFACE sect. 2, ROWS)
        ROWK = re.search(r'^ROWS_N%d = (.*)$' % N, rtxt, re.M).group(1).split()
        TYPK = re.search(r'^TYPES_N%d = (.*)$' % N, rtxt, re.M).group(1).split()
        CNTK = int(re.search(r'^COUNT_N%d = (\d+)$' % N, rtxt, re.M).group(1))

        def row_label(key_):
            """the reader's rname of a ROWS key: <fam>_<dL>_<dR>, 'm' for '-', as "<fam> (<dL>,<dR>)"."""
            fam_, dL_, dR_ = key_.split('_')
            return '%s (%s,%s)' % (fam_, dL_.replace('m', '-'), dR_)
        rec_rows = []
        for key_, typ in zip(ROWK, TYPK):
            rr = {'row': key_, 'label': row_label(key_), 'type': typ, 'piece_of_max': wpc}
            if nstop_pc or not PCREC:
                rr['stop'] = 'piece %d: %s' % nstop_pc[0] if nstop_pc else 'no piece evaluated'
            else:
                rr.update(AGG)
            rec_rows.append(rr)
        gate('C-ROWS', len(ROWK) == CNTK == len(TYPK) and len(rec_rows) == CNTK and all('q_hat_hi' in x_ for x_ in rec_rows) and
             len(PCREC) + len(nstop_pc) == len(PCS), 'completeness: the %d route-0 rows of ROWS (pk12 R65_D3_ROUTE0_ROWS_v1 6afdb5dd, '
             'ROWS_N%d) recorded with the max over the %d pieces P%04d..P%04d (%d stop); R6.5 decides each row on certified values (lo > 0)' % (
                 CNTK, N, len(PCS), PF, PL, len(nstop_pc)))
        # C-T-RECOMPUTE: every piece's T_s recomputed from its recorded parts, and a plant
        okT = all(bool(abs(U.u4_T(sp, x['beta_s'], x['m_abs'], x['xu'], x['beta_s']) - x['T_s']) <= arb('1e-30') * x['T_s'])
                  for x in PCREC.values())
        gate('C-T-RECOMPUTE', okT and len(PCREC) > 0, 'every piece\'s T_s equals U4\'s formula on its recorded parts (s\', beta-hat_s, '
             '|m-hat_s|, ||X_s psi_u||, the adjoint term)')
        if PCREC:
            x0 = PCREC[min(PCREC)]
            Tb = U.u4_T(sp, x0['beta_s'], x0['m_abs'], x0['xu'], arb(0))
            plant('PLANT-TRECOMP', bool(Tb < x0['T_s']), 'the adjoint term dropped from the first piece\'s T_s changes it (%.4e < %.4e)' % (
                float(Tb), float(x0['T_s'])))
        tight = ('route 0', 'max', wpc) if wpc is not None else None
        # C-TGT: one-at-a-time ends of the worst piece's entries stay inside its q-hat_hi
        if tight is not None:
            r, cc, T = chain_at(wpc)
            Ep = r['Ep']
            mids = {k2: arb(v2[0].mid()) for k2, v2 in Ep.items()}
            nin, nout, nstop, worst_t = 0, 0, 0, None
            for k2 in sorted(Ep):
                for side in (U.lo, U.up):
                    thin = dict(mids)
                    thin[k2] = side(Ep[k2][0])
                    r2 = U.chain_uhat(lambda g, k_, ro: thin[(g, k_, ro)], cc['c_e'], cc['c_f'])
                    if not r2['pd']:
                        nstop += 1
                        continue
                    q2 = U.q_hat(r2['bMb'], r2['hp2'], cc['c_e'], A, s2)
                    if 'stop' in q2:
                        nstop += 1
                        continue
                    if bool(q2['q_hat_hi'] <= r['q_hat_hi']):
                        nin += 1
                    else:
                        nout += 1
                    worst_t = q2['q_hat_hi'] if worst_t is None or bool(q2['q_hat_hi'] > worst_t) else worst_t
            gate('C-TGT', nout == 0 and nin > 0, 'the tightest row %s: %d one-at-a-time ends of its %d entries (others at their centre '
                 'midpoints): %d inside q-hat_hi %.6e, %d outside, %d stop (not admissible); largest thin q-hat %s' % (
                     tight, 2 * len(Ep), len(Ep), nin, float(r['q_hat_hi']), nout, nstop, ('%.6e' % float(worst_t)) if worst_t else '-'))
        # ------------------------------------------------------------ L0 windows (route H, one J-uniform piece t in [0, 1/300])
        l0, ccL, L0_SKIP = {}, {}, {}
        for g in ('D4L0', 'D4ML0'):
            keys_ = [k_ for (f_, k_) in ITEMS_ if f_ == g]
            cls = 'D4' if g == 'D4L0' else 'D4M'
            L0max, mmax, btmax, wpcL = None, None, None, None
            for pc in PCS:
                jlo, jhi = EXP[pc]
                T = L.piece_T(jlo, jhi)
                ccp = gc_use(centres_at(pc, cls))                                   # G-C: the piece's certified balls (c_t, c_b)
                ce, cf = ccp['c_e'], ccp['c_f']
                Ep = {k_: E_pair(g, k_, 'entry', T, ccp, arb(jlo)) for k_ in keys_}
                form = U.l0_d4l0 if g == 'D4L0' else U.l0_d4ml0
                Evc = {k_: v[0] for k_, v in Ep.items()}
                sc, mc, L0c = U.c_centred2(lambda e_, f_: form(Evc, e_, f_, sqf=U.csq), ce, cf)    # mean-value form over the centre balls
                sd, md, L0d = form({k_: v[1] for k_, v in Ep.items()}, ce, cf, sqf=L.sq)
                L0T, mT = centred(L0c, L0d, T), centred(mc, md, T)
                finchk('%s piece %d' % (g, pc), [L0T, mT])
                bt = U.beta_D4(A, ce, cf, A2c, U.mhat_lo(MH[0], MH[1], MH[2], jhi), RTRc, s2, eps_r)
                if L0max is None or bool(U.up(L0T) > L0max):
                    L0max, wpcL = U.up(L0T), pc
                mmax = U.up(abs(mT)) if mmax is None else U.amax_up(mmax, abs(mT))
                btmax = bt if btmax is None else U.amax_up(btmax, bt)
                ccL.setdefault(g, {})[pc] = CEN[(cls, pc)]
            qh = U.up(U.amax_up(L0max, arb(0)).sqrt())
            l0[g] = {'L0_hi': L0max, 'q_hat_hi': qh, 'm_abs': mmax, 'beta': btmax, 'worst_piece': wpcL}
        for g, adj in (('D4L0', 'D4ML0'), ('D4ML0', 'D4L0')):
            if g not in l0:
                continue
            x = l0[g]
            bt = x['beta']
            xu = U.xu_bound(x['q_hat_hi'], x['m_abs'], s2)
            same_c = adj in l0 and ccL[adj] == ccL[g]
            xsu = U.xu_bound(l0[adj]['q_hat_hi'], l0[adj]['m_abs'], s2) if same_c else bt
            T = U.u4_T(sp, bt, x['m_abs'], xu, xsu)
            qhi = U.route_H(x['q_hat_hi'], x['m_abs'], eps_r, T, s2)
            x.update(xu=xu, xsu=xsu, xsu_src=('adjoint %s (same c)' % adj) if same_c else (
                'beta-hat fallback (G-ADJ: %s)' % ('other c' if adj in l0 else 'adjoint window not written')), T_U4=T, q_hi=qhi, route='H')
            out('L0 %s N%d: max over the %d pieces P%04d..P%04d (worst P%04d): L0_hi %.6e, q-hat_s %.6e, |m-hat_s| %.4e, beta-hat %.4f, '
                'T_U4 %.4e (%s), q_hi (route H) %.6e' % (g, N, len(PCS), PF, PL, x['worst_piece'], float(x['L0_hi']), float(x['q_hat_hi']),
                                                         float(x['m_abs']), float(bt), float(T), x['xsu_src'], float(qhi)))
        L0_FIELDS = ('L0_hi', 'q_hat_hi', 'm_abs', 'beta', 'xu', 'xsu', 'xsu_src', 'T_U4', 'q_hi', 'route')

        def l0_post_ok(win):
            """C-L0-POST's field check: every part R6.5 recomputes q_hi from is present and q_hi is the route-H form on those parts."""
            if not all(k_ in win for k_ in L0_FIELDS) or win['route'] != 'H':
                return False
            return bool(abs(U.route_H(win['q_hat_hi'], win['m_abs'], eps_r, win['T_U4'], s2) - win['q_hi']) <= arb('1e-30') * win['q_hi'])
        gate('C-L0-POST', all(l0_post_ok(l0[g]) for g in l0) and len(l0) == 2, 'each l0_hat window carries its parts (%s) and q_hi equals '
             'route H on them' % ', '.join(L0_FIELDS))
        lp = {g: dict(l0[g]) for g in l0}
        lp['D4ML0'].pop('m_abs', None)
        lq = dict(l0['D4L0'], q_hi=U.up(l0['D4L0']['q_hi'] * arb('0.999')))
        plant('PLANT-L0POST', not l0_post_ok(lp['D4ML0']) and not l0_post_ok(lq), 'the same check refuses a window without |m-hat_s|_hi and one '
              'whose q_hi sits 0.1% below route H on its parts')
        gate('G-ADJ', all(l0[g]['xsu_src'].startswith(('adjoint', 'beta-hat')) for g in l0), 'the adjoint term: the adjoint window\'s site '
             'value at the same c, else beta-hat: %s' % ', '.join('%s %s' % (g, l0[g]['xsu_src']) for g in l0))
        # ------------------------------------------------------------ B' (FA) per piece: raw overlaps, basis raw, T_v
        bp_pieces = []
        Tv_max = arb(0)
        for pc in PCS:
            jlo, jhi = EXP[pc]
            T = L.piece_T(jlo, jhi)
            ccp = gc_use(centres_at(pc, 'D4'))                                      # G-C: X_c in B' at the D4 balls (c_t, c_b)
            ct, cb = ccp['c_t'], ccp['c_b']
            Ep = {}
            for j in range(U.BPRIME_J):
                for pre in ('1', 'T', 'B', 'X'):
                    Ep['%s,%d' % (pre, j)] = E_pair('FA', '%s,%d' % (pre, j), 'entry', T, ccp, arb(jlo))
            Evc = {k_: v[0] for k_, v in Ep.items()}
            vc = list(U.c_centred2(lambda t_, b_: tuple(U.bprime_raw(Evc, t_, b_)), ct, cb))       # mean-value form over the D4 balls
            vd = U.bprime_raw({k_: v[1] for k_, v in Ep.items()}, ct, cb)
            vr = [centred(vc[j], vd[j], T) for j in range(U.BPRIME_J)]
            finchk('FA piece %d' % pc, vr)
            bt = U.beta_D4(A, ct, cb, A2c, U.mhat_lo(MH[0], MH[1], MH[2], jhi), RTRc, s2, eps_r)
            Tv = U.up(bt * sp)
            Tv_max = U.amax_up(Tv_max, Tv)
            bp_pieces.append((pc, jlo, jhi, vr, Tv, bt))
        gate('C-BASIS-RAW', [p_[0] for p_ in bp_pieces] == list(PCS) and all(len(p_[3]) == U.BPRIME_J for p_ in bp_pieces), 'B\' writes '
             'v_hat_raw_j = F_k R(X_c; j) for j = 0..%d at all %d pieces P%04d..P%04d in the raw basis (R6.5 centres with S8\'s g_j0/g00 and '
             'applies C^ once); T_v = beta-hat s\' per piece (ADD6), largest %.4e' % (U.BPRIME_J - 1, len(PCS), PF, PL, float(Tv_max)))
        gate('G-C', GC_CHECKED[0] > 0 and not GC_BAD, '%d piece centre uses, each the means export\'s balls for its piece and class (db731c93: '
             'D3 for route 0, D4 for D4L0 and B\', D4M for D4ML0), endpoint for endpoint; mismatches %s' % (GC_CHECKED[0], GC_BAD[:3] or 'none'))
        # G-C thin check: the c-polynomial quantities with the entries at their midpoints and c at the corners of B_c lie
        # inside the ball evaluation the run uses; the evaluation at the ball's midpoint alone must miss some corner value
        corners = lambda ce_, cf_: [(U.lo(ce_), U.lo(cf_)), (U.up(ce_), U.up(cf_)), (U.lo(ce_), U.up(cf_)), (U.up(ce_), U.lo(cf_))]
        TH_IN, TH_OUT, TH_MIDMISS = [0], [], [0]

        def thin_cmp(ball_vals, mid_vals, thin_vals, tag):
            for b_, m_, t_ in zip(ball_vals, mid_vals, thin_vals):
                if bool(b_.contains(t_)):
                    TH_IN[0] += 1
                else:
                    TH_OUT.append(tag)
                if not bool(m_.contains(t_)):
                    TH_MIDMISS[0] += 1
        r0t, cc0, _ = chain_at(PF)                                          # at the set's first piece
        Ep0 = r0t['Ep']
        ballE = lambda g, k_, ro: Ep0[(g, k_, ro)][0]
        midE = lambda g, k_, ro: arb(Ep0[(g, k_, ro)][0].mid())

        def flat_r0(rr_):
            return rr_['v'] + rr_['KE'] + [x for row_ in rr_['M'] for x in row_] + [rr_['Eh2']]
        rb0 = flat_r0(U.chain_uhat(ballE, cc0['c_e'], cc0['c_f']))
        rm0 = flat_r0(U.chain_uhat(ballE, arb(cc0['c_e'].mid()), arb(cc0['c_f'].mid())))
        for ce_, cf_ in corners(cc0['c_e'], cc0['c_f']):
            thin_cmp(rb0, rm0, flat_r0(U.chain_uhat(midE, ce_, cf_)), 'route 0 P%04d' % PF)
        T0 = L.piece_T(EXP[PF][0], EXP[PF][1])
        for g in ('D4L0', 'D4ML0'):
            cls = 'D4' if g == 'D4L0' else 'D4M'
            ccp = centres_at(PF, cls)
            keys_ = [k_ for (f_, k_) in ITEMS_ if f_ == g]
            Evc = {k_: E_pair(g, k_, 'entry', T0, ccp, arb(EXP[PF][0]))[0] for k_ in keys_}
            Evm = {k_: arb(v_.mid()) for k_, v_ in Evc.items()}
            form = U.l0_d4l0 if g == 'D4L0' else U.l0_d4ml0
            fb = U.c_centred2(lambda e_, f_: form(Evc, e_, f_, sqf=U.csq), ccp['c_e'], ccp['c_f'])
            fm = U.c_centred2(lambda e_, f_: form(Evc, e_, f_, sqf=U.csq), arb(ccp['c_e'].mid()), arb(ccp['c_f'].mid()))
            for ce_, cf_ in corners(ccp['c_e'], ccp['c_f']):
                thin_cmp(fb, fm, form(Evm, ce_, cf_), '%s P%04d' % (g, PF))
        ccp = centres_at(PF, 'D4')
        EvF = {}
        for j in range(U.BPRIME_J):
            for pre in ('1', 'T', 'B', 'X'):
                EvF['%s,%d' % (pre, j)] = E_pair('FA', '%s,%d' % (pre, j), 'entry', T0, ccp, arb(EXP[PF][0]))[0]
        EvFm = {k_: arb(v_.mid()) for k_, v_ in EvF.items()}
        bb = U.c_centred2(lambda t_, b_: tuple(U.bprime_raw(EvF, t_, b_)), ccp['c_t'], ccp['c_b'])
        bm = U.c_centred2(lambda t_, b_: tuple(U.bprime_raw(EvF, t_, b_)), arb(ccp['c_t'].mid()), arb(ccp['c_b'].mid()))
        for ct_, cb_ in corners(ccp['c_t'], ccp['c_b']):
            thin_cmp(bb, bm, U.bprime_raw(EvFm, ct_, cb_), 'B\' P%04d' % PF)
        gate('G-C', TH_IN[0] > 0 and not TH_OUT, 'thin check at P%04d (route 0 v, KE, M, E[h^2]; the D4L0 and D4ML0 forms; B\''
             's overlaps): %d corner values with midpoint entries inside the ball evaluation, outside %s' % (PF, TH_IN[0], TH_OUT[:3] or 'none'))
        plant('PLANT-GC-THIN', TH_MIDMISS[0] > 0, 'the evaluation at the balls\' midpoints alone misses %d corner values' % TH_MIDMISS[0])
        kr_bad = []
        for (fam, k_, ro), kk_ in sorted(KREC.items()):
            try:
                U.ktab_role_check(fam, k_, ITEMS_[(fam, k_)]['columns'], ITEMS_[(fam, k_)]['factors'], ro, kk_)
            except ValueError as e_:
                kr_bad.append(str(e_)[:100])
        gate('C-KTAB', not kr_bad and len(KREC) > 0, '%d (family, key, role, k) triples the chain read match the table (W2 G,a,b: gram k = 1, '
             'vcomp k = 2); mismatches %s' % (len(KREC), kr_bad[:3] or 'none'))
        # ------------------------------------------------------------ PLANT-NAN, C-FINITE, C-DEC, record
        it_n = dict(ITEMS_[('W2', 'G,1,2')])
        it_n['co'] = ([arb(float('nan'))] + it_n['co'][0][1:], it_n['co'][1])
        ITEMS_[('W2', 'G,1,2')], keep = it_n, ITEMS_[('W2', 'G,1,2')]
        pn_ = wpc if wpc is not None else 0
        rn, _, _ = chain_at(pn_)
        ITEMS_[('W2', 'G,1,2')] = keep
        nn = sum(1 for row in rn['G'] for x in row if not L.fin(x))
        plant('PLANT-NAN', nn > 0, 'W2 G,1,2 a_0 = NaN: C-FINITE finds %d non-finite G entries' % nn)
        if NONFIN and NONFIN[-1].startswith('piece %d' % pn_):
            NONFIN.pop()
        # ------------------------------------------------------------ the record in INTERFACE_UHAT_R65_v1_4's format
        def row_key(lab):
            """INTERFACE sect. 3: the reader's rname "<fam> (<dL>,<dR>)" as <fam>_<dL>_<dR>, '-' written 'm'."""
            m_ = re.fullmatch(r'(\w+) \((-?\d+),(\w+)\)', lab)
            if not m_:
                raise ValueError('INTERFACE: the row label %r is not "<fam> (<dL>,<dR>)"' % lab)
            return '%s_%s_%s' % (m_.group(1), m_.group(2).replace('-', 'm'), m_.group(3))
        KV, WORLD = [], {}

        def put(key, val, world='-'):
            KV.append('%s = %s' % (key, val))
            WORLD[key] = world

        def rv(dec_s):
            """the ball of a recorded decimal, exactly its value inside (U.farb): derived values are formed on the recorded parts."""
            return U.farb(Fraction(dec_s))
        # every value the table defines by a form of other recorded values is that form on their recorded decimals, outward (
        # pk12's catch on l0_hat.D4ML0.q_hat_hi): the parts first, then each derived value from their decimals, rounded up
        if AGG:
            r0d = {'q_hat_hi': dhi(AGG['q_hat_hi']), 'beta_hat_s': dhi(AGG['beta_s']), 'm_hat_s_hi': dhi(AGG['m_abs'])}
            r0d['xu_hi'] = dhi(U.up((rv(r0d['q_hat_hi']) * rv(r0d['q_hat_hi']) + rv(r0d['m_hat_s_hi']) * rv(r0d['m_hat_s_hi'])).sqrt()))
            r0d['T_s'] = dhi(U.u4_T(sp, rv(r0d['beta_hat_s']), rv(r0d['m_hat_s_hi']), rv(r0d['xu_hi']), rv(r0d['beta_hat_s'])))
            r0d['q_b_hi'] = dhi(U.route_P(rv(r0d['q_hat_hi']), rv(r0d['T_s'])))
        for x in rec_rows:
            if row_key(x['label']) != x['row']:
                raise ValueError('INTERFACE: the ROWS key %s does not round-trip through its rname %r' % (x['row'], x['label']))
            rk = 'route0b_hat.%s' % x['row']
            if any(k_.startswith(rk + '.') for k_ in WORLD):
                raise ValueError('INTERFACE: ROWS lists %s twice; the record carries one block per row' % x['row'])
            if 'q_hat_hi' not in x:
                raise ValueError('INTERFACE: route 0 row %s has no value (%s); the record carries every row' % (x['row'], x.get('stop')))
            put(rk + '.route', 'P')
            put(rk + '.formula', 'ROUTE_P_UHAT_v1')
            put(rk + '.q_hat_hi', r0d['q_hat_hi'], 'hat')
            put(rk + '.beta_hat_s', r0d['beta_hat_s'], 'transfer')
            put(rk + '.m_hat_s_hi', r0d['m_hat_s_hi'], 'hat')
            put(rk + '.m_hat_s_source', 'beta-hat_fallback')
            put(rk + '.xu_hi', r0d['xu_hi'], 'hat')
            put(rk + '.T_s', r0d['T_s'], 'transfer')
            put(rk + '.q_b_hi', r0d['q_b_hi'], 'true')
        l0d = {}
        for g in ('D4L0', 'D4ML0'):
            x = l0[g]
            d_ = {'L0_hi': dhi(x['L0_hi']), 'm_hat_s_hi': dhi(x['m_abs']), 'beta_hat': dhi(x['beta'])}
            d_['q_hat_hi'] = dhi(U.up(U.amax_up(rv(d_['L0_hi']), arb(0)).sqrt()))           # L0_hi^(1/2) of the recorded L0_hi, rounded up
            d_['xu_hi'] = dhi(U.xu_bound(rv(d_['q_hat_hi']), rv(d_['m_hat_s_hi']), s2))
            l0d[g] = d_
        for g, adj in (('D4L0', 'D4ML0'), ('D4ML0', 'D4L0')):
            x, d_ = l0[g], l0d[g]
            d_['xsu_hi'] = l0d[adj]['xu_hi'] if x['xsu_src'].startswith('adjoint') else d_['beta_hat']
            d_['T_U4'] = dhi(U.u4_T(sp, rv(d_['beta_hat']), rv(d_['m_hat_s_hi']), rv(d_['xu_hi']), rv(d_['xsu_hi'])))
            d_['q_hi'] = dhi(U.route_H(rv(d_['q_hat_hi']), rv(d_['m_hat_s_hi']), eps_r, rv(d_['T_U4']), s2))
        for g in ('D4L0', 'D4ML0'):
            x, d_ = l0[g], l0d[g]
            pre = 'l0_hat.%s.' % g
            put(pre + 'route', 'H')
            put(pre + 'L0_hi', d_['L0_hi'], 'hat')
            put(pre + 'q_hat_hi', d_['q_hat_hi'], 'hat')
            put(pre + 'm_hat_s_hi', d_['m_hat_s_hi'], 'hat')
            put(pre + 'beta_hat', d_['beta_hat'], 'transfer')
            put(pre + 'xu_hi', d_['xu_hi'], 'hat')
            put(pre + 'xsu_hi', d_['xsu_hi'], 'hat')
            put(pre + 'xsu_source', 'adjoint_same_c' if x['xsu_src'].startswith('adjoint') else 'beta-hat_fallback')
            put(pre + 'T_U4', d_['T_U4'], 'transfer')
            put(pre + 'q_hi', d_['q_hi'], 'true')
        hull = [None] * U.BPRIME_J
        for pc, jlo, jhi, vr, Tv, bt in bp_pieces:
            for j in range(U.BPRIME_J):
                hull[j] = vr[j] if hull[j] is None else hull[j].union(vr[j])
        put('bprime_hat.FA.basis', 'raw')
        for j in range(U.BPRIME_J):
            put('bprime_hat.FA.v_hat_raw.%d' % j, dball(hull[j]), 'hat')
        put('bprime_hat.FA.T_v', dhi(Tv_max), 'transfer')
        put('bprime_hat.FA.T_v_source', 'pk02/DESIGN_UHAT_ASM_v1_3_ADD6.md:%s' % FULL['add6'])
        WU = ' '.join(k_ for k_ in WORLD if WORLD[k_] == 'hat')
        WT = ' '.join(k_ for k_ in WORLD if WORLD[k_] == 'true')

        def world_ok(kv_keys, wu, wt, worlds):
            """C-WORLD-U (INTERFACE sect. 3): every hat key is listed in WORLD_U_HAT only, every true key in WORLD_TRUE_U
            only, transfer and tag keys in neither, and every listed key is a key of the record."""
            su, st = set(wu.split()), set(wt.split())
            for k_ in kv_keys:
                w_ = worlds[k_]
                if (k_ in su) != (w_ == 'hat') or (k_ in st) != (w_ == 'true'):
                    return False
            return (su | st) <= set(kv_keys)
        gate('C-WORLD-U', world_ok(list(WORLD), WU, WT, WORLD), '%d hat keys in WORLD_U_HAT, %d true keys in WORLD_TRUE_U, %d transfer or tag '
             'keys in neither' % (len(WU.split()), len(WT.split()), sum(1 for w_ in WORLD.values() if w_ not in ('hat', 'true'))))
        tk = next(k_ for k_ in WORLD if WORLD[k_] == 'true')
        plant('PLANT-WORLD-U', not world_ok(list(WORLD), WU + ' ' + tk, ' '.join(k_ for k_ in WT.split() if k_ != tk), WORLD), 'the true key %s '
              'filed under WORLD_U_HAT is refused by the same check' % tk)
        lines = ['# UHAT_ASM_v1 record by pk02 kt_uhat_asm_v1_8 (DESIGN_UHAT_ASM_v1_3 faa09e23 with ADD1-ADD6), in INTERFACE_UHAT_R65_v1_4\'s '
                 'format. Every decimal is an outward end; a ball is "lo hi"; every derived value is its form on the recorded parts, rounded up.',
                 '# INFO: constants N%d_A2 %s, N%d_RTR %s, N%d_TRB %s, N%d_MHAT_M1..M3 %s; RULING_22 %s (%s); A4 cancelled (the 2J form is the '
                 'route of record); FA by operators (ADD5) with g from %s; pieces P%04d..P%04d (the GJJ export\'s N%d_PIECES; below P%04d '
                 'RH_MODULE_v1_4 cor:rhstrips, J in [%s, %s]); entries and W2 mirrors from %s; every input on an info.input line' % (
                     N, CK['A2'], N, CK['RTR'], N, CK['TRB'], N, ' '.join(CK[k_] for k_ in ('M1', 'M2', 'M3')), RULING_22,
                     'read' if PINNED else 'NOT matching', 'S8\'s float chain (MOCK)' if MODE == 'mock' else 'the GJJ export\'s N%d_MAX' % N,
                     PF, PL, N, PF, RH[N][0], RH[N][1], 'the r0b v1_3 and W2M records (m3_reader_v6_3)' if MODE == 'cert' else
                     'the float ent files and the deterministic mock (MOCK)'),
                 'RECORD = UHAT_ASM_v1', 'FORMAT = S4U_KV_v1', 'EXPORT_STATUS = <status>', 'MOCK = <mock>', 'VERDICT_OF_WRITER = <verdict>',
                 'N = %d' % N, 'INTERFACE = pk02/INTERFACE_UHAT_R65_v1_4.md:%s' % FULL['interface'],
                 'ROWS = pk12/R65_D3_ROUTE0_ROWS_v1.kv:%s' % FULL['rows'], 'J_RANGE = %s' % JRNG,
                 'J_UNIFORMITY = UNIFORM-J each value below holds for every J in J_RANGE: the max over centres.pieces for an upper end, the '
                 'hull for a ball (ADD4 sect. 3)',
                 'centres.source = pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37.kv:%s' % FULL['means'],
                 'centres.pieces = P%04d..P%04d' % (PF, PL), 'M2B = pk02/M2B_KV_v1.txt:%s' % FULL['m2b_kv'],
                 'CODE = pk02/kt_uhat_asm_v1_8.py:%s' % SELF, 'LIB = pk02/uhat_lib_v1_2.py:%s' % USHA,
                 'WORLD_U_HAT = %s' % WU, 'WORLD_TRUE_U = %s' % WT] + KV
        for pc_ in sorted(PCREC):
            x = PCREC[pc_]
            iq_, it_ = dhi(x['q_hat_hi']), dhi(x['T_s'])
            lines += ['info.route0b_hat.P%04d.q_hat_hi = %s' % (pc_, iq_), 'info.route0b_hat.P%04d.T_s = %s' % (pc_, it_),
                      'info.route0b_hat.P%04d.q_b_hi = %s' % (pc_, dhi(U.route_P(rv(iq_), rv(it_))))]
        for pc, jlo, jhi, vr, Tv, bt in bp_pieces:
            lines.append('info.bprime_hat.FA.P%04d.T_v = %s' % (pc, dhi(Tv)))
            for j in range(U.BPRIME_J):
                lines.append('info.bprime_hat.FA.P%04d.v_hat_raw.%d = %s' % (pc, j, dball(vr[j])))
        INP = [('m2b_asm_out', F['m2b_asm_out']), ('m2bw', F['m2bw_kv']), ('m2bw_out', F['m2bw_out']), ('gjj', F['gjj']), ('gjj_out', F['gjj_out']),
               ('means_out', F['means_out'])]
        if MODE == 'cert':
            INP += [('r0b_%s' % g_, CI[('r0b', g_)]) for g_ in R0B_FAMS] + [('r0b_asm_out', CI[('r0b', 'asm_out')]),
                                                                          ('w2m', CI[('w2m', 'record')]), ('w2m_asm_out', CI[('w2m', 'asm_out')]),
                                                                          ('cert_inputs', F['config'])]
        lines += ['info.input.%s = %s:%s' % (nm_, os.path.relpath(p_, CODEDIR), sha(p_)) for nm_, p_ in INP]
        okdec = all(L.dec_ok(s_, f_, up_) for s_, f_, up_ in DECLOG)
        gate('C-DEC', okdec and len(DECLOG) > 0, '%d decimal strings re-read: each brackets its exact end outward' % len(DECLOG))
        badv = [ln for ln in lines if ' = ' in ln and re.search(r'(?i)\bnan\b', ln.split(' = ', 1)[1])]
        badv += [ln for ln in lines if ' = ' in ln and re.search(r'(?i)\binf\b', ln.split(' = ', 1)[1]) and not ln.endswith(' inf')]
        okfin = not NONFIN and not badv
        gate('C-FINITE', okfin, 'every evaluated ball finite; non-finite at %s' % (NONFIN[:3] or 'none'))
        # the lines exactly as written when every gate passes and every plant fires (a failed run writes no record)
        sub = {'EXPORT_STATUS = <status>': 'EXPORT_STATUS = %s' % ('MOCK' if MODE == 'mock' else 'CERTIFIED'),
               'MOCK = <mock>': 'MOCK = %s' % ('TRUE' if MODE == 'mock' else 'FALSE'), 'VERDICT_OF_WRITER = <verdict>': 'VERDICT_OF_WRITER = VALID'}
        lines = [sub.get(ln, ln) for ln in lines] + ['END = UHAT_ASM_v1']
        # ------------------------------------------------------------ C-FORM: INTERFACE_UHAT_R65_v1_4 sect. 1-5 on the written lines
        DECX = r'[-+]?[0-9]+(\.[0-9]*)?([eE][-+]?[0-9]+)?'
        HDR = {'RECORD': ('tag', ('UHAT_ASM_v1',)), 'FORMAT': ('tag', ('S4U_KV_v1',)), 'EXPORT_STATUS': ('tag', ('MOCK', 'CERTIFIED')),
               'MOCK': ('tag', ('TRUE', 'FALSE')), 'VERDICT_OF_WRITER': ('tag', ('VALID',)), 'N': ('tag', ('4', '3')), 'INTERFACE': ('src', None),
               'ROWS': ('src', None), 'J_RANGE': ('list', None), 'J_UNIFORMITY': ('text', 'UNIFORM-J'), 'centres.source': ('src', None),
               'centres.pieces': ('range', None), 'M2B': ('src', None), 'CODE': ('src', None), 'LIB': ('src', None),
               'WORLD_U_HAT': ('list', None), 'WORLD_TRUE_U': ('list', None), 'END': ('tag', ('UHAT_ASM_v1',))}
        HDR = {k_: v_ + ('-',) for k_, v_ in HDR.items()}
        # sect. 3's (form, allowed, world) with the table's world column (C-FORM checks the WORLD lists against it)
        R0K = {'route': ('tag', ('P', 'H'), '-'), 'formula': ('tag', ('ROUTE_P_UHAT_v1', 'ROUTE_H_NB1'), '-'), 'q_hat_hi': ('up', None, 'hat'),
               'beta_hat_s': ('up', None, 'transfer'), 'm_hat_s_hi': ('up', None, 'hat'),
               'm_hat_s_source': ('tag', ('beta-hat_fallback', 'certified_mean'), '-'), 'xu_hi': ('up', None, 'hat'),
               'T_s': ('up', None, 'transfer'), 'T_U4': ('up', None, 'transfer'), 'q_b_hi': ('up', None, 'true')}
        L0K = {'route': ('tag', ('H',), '-'), 'L0_hi': ('up', None, 'hat'), 'q_hat_hi': ('up', None, 'hat'), 'm_hat_s_hi': ('up', None, 'hat'),
               'beta_hat': ('up', None, 'transfer'), 'xu_hi': ('up', None, 'hat'), 'xsu_hi': ('up', None, 'hat'),
               'xsu_source': ('tag', ('adjoint_same_c', 'beta-hat_fallback'), '-'), 'T_U4': ('up', None, 'transfer'), 'q_hi': ('up', None, 'true')}
        BPK = dict([('basis', ('tag', ('raw',), '-')), ('T_v', ('up', None, 'transfer')), ('T_v_source', ('src', None, '-'))] +
                   [('v_hat_raw.%d' % j, ('ball', None, 'hat')) for j in range(4)])
        POSK = ('T_s', 'T_U4')                                  # every up >= 0; T_s, T_U4 > 0
        FIXV = {'N': str(N), 'J_RANGE': JRNG, 'INTERFACE': 'pk02/INTERFACE_UHAT_R65_v1_4.md:%s' % PINS['interface'],
                'ROWS': 'pk12/R65_D3_ROUTE0_ROWS_v1.kv:%s' % PINS['rows'], 'M2B': 'pk02/M2B_KV_v1.txt:%s' % PINS['m2b_kv'],
                'centres.source': 'pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37.kv:%s' % PINS['means'],
                'centres.pieces': GKV['N%d_PIECES' % N], 'bprime_hat.FA.T_v_source': 'pk02/DESIGN_UHAT_ASM_v1_3_ADD6.md:%s' % PINS['add6']}
        HC = {}

        def hash_rel(p_):
            """the sha256 of a src path (relative to code/), None for a path outside code/ or a missing file."""
            if p_.startswith('/') or '..' in p_.split('/'):
                return None
            if p_ not in HC:
                q_ = os.path.join(CODEDIR, p_)
                HC[p_] = sha(q_) if os.path.isfile(q_) else None
            return HC[p_]

        def form_of(key, rowset):
            """(form, allowed) of a record key by the table (sect. 2-3); None for a key outside it."""
            if key in HDR:
                return HDR[key]
            p_ = key.split('.')
            if p_[0] == 'route0b_hat' and len(p_) == 3 and p_[1] in rowset:
                return R0K.get(p_[2])
            if p_[0] == 'l0_hat' and len(p_) == 3 and p_[1] in ('D4L0', 'D4ML0'):
                return L0K.get(p_[2])
            if key.startswith('bprime_hat.FA.'):
                return BPK.get(key[len('bprime_hat.FA.'):])
            return None

        def is_ball(v_):
            return bool(re.fullmatch('%s %s' % (DECX, DECX), v_)) and Fraction(v_.split()[0]) <= Fraction(v_.split()[1])

        def form_problems(lns, rowk):
            """every way the record lines lns break INTERFACE_UHAT_R65_v1_4 (sect. 1-5) with ROWS_N<N> = rowk; [] when they conform."""
            bad_, kv_, rowset = [], {}, set(rowk)
            body = [ln for ln in lns if not ln.startswith('#')]
            if not body or body[-1] != 'END = UHAT_ASM_v1':
                bad_.append('END is not the last line')
            for ln in body:
                if ' = ' not in ln:
                    bad_.append('not "key = value": %r' % ln[:60])
                    continue
                k_, v_ = ln.split(' = ', 1)
                if k_ in kv_:
                    bad_.append('key twice: %s' % k_)
                kv_[k_] = v_
            wu_, wt_ = set(kv_.get('WORLD_U_HAT', '').split()), set(kv_.get('WORLD_TRUE_U', '').split())
            if not (wu_ | wt_) <= set(kv_) or wu_ & wt_:
                bad_.append('a WORLD list names a key the record lacks, or a key in both lists')
            for k_, v_ in kv_.items():
                if k_.startswith('info.input.'):                            # an input's src line: path relative to code/ and its sha256
                    m_ = re.fullmatch(r'([^\s:]+):([0-9a-f]{64})', v_)
                    if not (m_ and hash_rel(m_.group(1)) == m_.group(2)):
                        bad_.append('%s: %r is not a src that hashes to its pin' % (k_, v_[:60]))
                    continue
                if k_.startswith('info.'):
                    if not (re.fullmatch(DECX, v_) or is_ball(v_)):
                        bad_.append('%s: %r is not a dec or a ball' % (k_, v_[:40]))
                    continue
                fm = form_of(k_, rowset)
                if fm is None:
                    bad_.append('outside the table: %s' % k_)
                    continue
                f_, al_, wd_ = fm
                if k_ not in HDR and ((k_ in wu_) != (wd_ == 'hat') or (k_ in wt_) != (wd_ == 'true')):
                    bad_.append('%s: world %s, but filed under %s' % (k_, wd_, 'WORLD_U_HAT' if k_ in wu_ else 'WORLD_TRUE_U' if k_ in wt_ else
                                                                      'neither list'))
                if f_ == 'up':
                    ok_ = bool(re.fullmatch(DECX, v_))
                elif f_ == 'ball':
                    ok_ = is_ball(v_)
                elif f_ == 'tag':
                    ok_ = v_ in al_
                elif f_ == 'src':
                    m_ = re.fullmatch(r'([^\s:]+):([0-9a-f]{64})', v_)
                    ok_ = bool(m_) and hash_rel(m_.group(1)) == m_.group(2)
                elif f_ == 'list':
                    ok_ = bool(re.fullmatch(r'\S+( \S+)*', v_))
                elif f_ == 'range':
                    ok_ = bool(re.fullmatch(r'P[0-9]{4}\.\.P[0-9]{4}', v_))
                else:
                    ok_ = v_.split(' ', 1)[0] == al_
                if not ok_:
                    bad_.append('%s: %r is not a %s' % (k_, v_[:40], f_))
                elif f_ == 'up' and (Fraction(v_) <= 0 if k_.split('.')[-1] in POSK else Fraction(v_) < 0):
                    bad_.append('%s: %s has the wrong sign' % (k_, v_))
            for k_, v_ in FIXV.items():
                if kv_.get(k_) != v_:
                    bad_.append('%s is not the pinned %s' % (k_, v_[:60]))
            if (kv_.get('EXPORT_STATUS') == 'MOCK') != (kv_.get('MOCK') == 'TRUE'):
                bad_.append('MOCK disagrees with EXPORT_STATUS')
            need = list(HDR) + ['l0_hat.%s.%s' % (w_, f_) for w_ in ('D4L0', 'D4ML0') for f_ in L0K] + ['bprime_hat.FA.' + f_ for f_ in BPK]
            for r_ in rowk:
                rt_, pre_ = kv_.get('route0b_hat.%s.route' % r_), 'route0b_hat.%s.' % r_
                if rt_ not in ('P', 'H') or kv_.get(pre_ + 'formula') != {'P': 'ROUTE_P_UHAT_v1', 'H': 'ROUTE_H_NB1'}.get(rt_):
                    bad_.append('%s: route %s and formula %s disagree' % (r_, rt_, kv_.get(pre_ + 'formula')))
                no_ = 'T_U4' if rt_ == 'P' else 'T_s'
                if pre_ + no_ in kv_:
                    bad_.append('%s: a route %s row carries %s' % (r_, rt_, no_))
                need += [pre_ + f_ for f_ in R0K if f_ != no_]
            miss_ = [k_ for k_ in need if k_ not in kv_]
            if miss_:
                bad_.append('missing %d keys: %s' % (len(miss_), ' '.join(miss_[:3])))
            return bad_
        fp = form_problems(lines, ROWK)
        nkey = sum(1 for ln in lines if ' = ' in ln and not ln.startswith(('#', 'info.')))
        gate('C-FORM', not fp, 'the record as written against INTERFACE_UHAT_R65_v1_4 sect. 1-5: %d table keys (%d route0b_hat blocks for the '
             '%d rows of ROWS_N%d), every value in its form, every sect. 3 key in the WORLD list of the table\'s world column'
             ', src files hash to their pins, centres.pieces %s and J_RANGE %s exactly, the sign rules, END last; problems %s' % (
                 nkey, len({ln.split('.')[1] for ln in lines if ln.startswith('route0b_hat.')}), len(ROWK), N, GKV['N%d_PIECES' % N], JRNG,
                 fp[:3] or 'none'))
        r0_ = 'route0b_hat.%s.' % ROWK[0]
        alt_set = ('P0000..P%04d' if PF > 0 else 'P0001..P%04d') % PL
        pert = {'another piece set (%s)' % alt_set: [('centres.pieces = %s' % alt_set) if ln.startswith('centres.pieces = ') else ln
                                                     for ln in lines],
                'J_RANGE "300 inf"': [('J_RANGE = 300 inf' if JRNG != '300 inf' else 'J_RANGE = 300.0 inf') if ln.startswith('J_RANGE = ') else ln
                                      for ln in lines],
                'a missing q_hat_hi': [ln for ln in lines if not ln.startswith(r0_ + 'q_hat_hi = ')],
                'an 8-hex src': [('bprime_hat.FA.T_v_source = pk02/DESIGN_UHAT_ASM_v1_3_ADD6.md:%s' % PINS['add6'][:8])
                                 if ln.startswith('bprime_hat.FA.T_v_source = ') else ln for ln in lines],
                'a ball with lo > hi': ['bprime_hat.FA.v_hat_raw.1 = 1 0' if ln.startswith('bprime_hat.FA.v_hat_raw.1 = ') else ln
                                        for ln in lines],
                'a wmat_hat key': lines[:-1] + ['wmat_hat.D4L0.W_hi = 1e-3', lines[-1]],
                'T_U4 on a route P row': lines[:-1] + [r0_ + 'T_U4 = 1e-4', lines[-1]],
                'a negative m_hat_s_hi': [(r0_ + 'm_hat_s_hi = -1e-3') if ln.startswith(r0_ + 'm_hat_s_hi = ') else ln for ln in lines],
                'a ROWS row without its block': [ln for ln in lines if not ln.startswith(r0_)],
                'an info.input line with another sha256': [(ln[:-64] + ln[-64:][::-1]) if ln.startswith('info.input.gjj = ') else ln
                                                            for ln in lines],
                'a true key under WORLD_U_HAT': [
                    ('WORLD_U_HAT = %s %sq_b_hi' % (ln.split(' = ', 1)[1], r0_)) if ln.startswith('WORLD_U_HAT = ') else
                    ('WORLD_TRUE_U = %s' % ' '.join(x_ for x_ in ln.split(' = ', 1)[1].split() if x_ != r0_ + 'q_b_hi'))
                    if ln.startswith('WORLD_TRUE_U = ') else ln for ln in lines]}
        caught = {k_: bool(form_problems(v_, ROWK)) for k_, v_ in pert.items()}
        plant('PLANT-FORM', all(caught.values()) and all(v_ != lines for v_ in pert.values()), 'the same check refuses each perturbed copy of '
              'the record: %s' % ', '.join('%s %s' % (k_, 'refused' if v_ else 'ACCEPTED') for k_, v_ in caught.items()))
        # ------------------------------------------------------------ C-DEC-UP: each derived value against its form on the recorded parts
        S_EX, E_EX = Fraction(kn['S_300'][0]), Fraction(kn['EPS_R_300'][0])     # M2B's s and eps_r, exactly as the reader takes them
        SP_EX = S_EX * (1 + S_EX)

        def u4_exact(b_, m_, xu_, xsu_):
            """U4's T as an exact rational: s' (beta + |m| + xu + xsu) + s'^2 (beta + xu + xsu) + beta s'^3, s' = s (1 + s)."""
            return SP_EX * (b_ + m_ + xu_ + xsu_) + SP_EX ** 2 * (b_ + xu_ + xsu_) + b_ * SP_EX ** 3

        def dec_up_bad(lns):
            """C-DEC-UP: every derived value of the record, re-read as an exact rational, is at least its form on the recorded
            decimals of its parts, with M2B's s and eps_r and square roots by squaring: route 0's xu_hi, T_s and q_b_hi per row, each L0
            window's q_hat_hi (L0_hi^(1/2)), xu_hi, xsu_hi, T_U4 and q_hi (route H), and each piece's info q_b_hi."""
            kv_ = dict(ln.split(' = ', 1) for ln in lns if ' = ' in ln and not ln.startswith('#'))
            Q = lambda k_: Fraction(kv_[k_])
            one_s2 = 1 - S_EX * S_EX
            bad_ = []
            for r_ in ROWK:
                p_ = 'route0b_hat.%s.' % r_
                q_, b_, m_, xu_, ts_, qb_ = (Q(p_ + f_) for f_ in ('q_hat_hi', 'beta_hat_s', 'm_hat_s_hi', 'xu_hi', 'T_s', 'q_b_hi'))
                bad_ += [p_ + f_ for f_, ok_ in (('xu_hi', xu_ >= 0 and xu_ * xu_ >= q_ * q_ + m_ * m_), ('T_s', ts_ >= u4_exact(b_, m_, xu_, b_)),
                                                ('q_b_hi', qb_ >= q_ + ts_)) if not ok_]
            for g_, adj_ in (('D4L0', 'D4ML0'), ('D4ML0', 'D4L0')):
                p_ = 'l0_hat.%s.' % g_
                L_, q_, m_, b_, xu_, xsu_, T_, qh_ = (Q(p_ + f_) for f_ in ('L0_hi', 'q_hat_hi', 'm_hat_s_hi', 'beta_hat', 'xu_hi', 'xsu_hi', 'T_U4',
                                                                            'q_hi'))
                xs_need = Q('l0_hat.%s.xu_hi' % adj_) if kv_[p_ + 'xsu_source'] == 'adjoint_same_c' else b_
                d_ = qh_ - E_EX * m_ / (1 - E_EX) - T_
                bad_ += [p_ + f_ for f_, ok_ in (('q_hat_hi', q_ >= 0 and q_ * q_ >= L_), ('xu_hi', xu_ >= 0 and xu_ * xu_ * one_s2 >= q_ * q_ + m_ * m_),
                                                ('xsu_hi', xsu_ >= xs_need), ('T_U4', T_ >= u4_exact(b_, m_, xu_, xsu_)),
                                                ('q_hi', d_ >= 0 and d_ * d_ * one_s2 >= q_ * q_)) if not ok_]
            bad_ += [k_ for k_ in kv_ if k_.startswith('info.route0b_hat.P') and k_.endswith('.q_b_hi') and
                     not Q(k_) >= Q(k_[:-6] + 'q_hat_hi') + Q(k_[:-6] + 'T_s')]
            return bad_
        dub = dec_up_bad(lines)
        nder = 3 * len(ROWK) + 10 + len(PCREC)
        gate('C-DEC-UP', not dub, '%d derived values, each re-read as an exact rational and at least its form on the recorded decimals of its parts '
             '(M2B\'s s and eps_r; square roots by squaring): route 0 xu_hi, T_s, q_b_hi per row; L0 q_hat_hi = L0_hi^(1/2), xu_hi, xsu_hi, T_U4, '
             'q_hi per window; info q_b_hi per piece; below %s' % (nder, dub[:3] or 'none'))
        kq, kb = 'l0_hat.D4ML0.q_hat_hi', 'route0b_hat.%s.q_b_hi' % ROWK[0]
        kvl = dict(ln.split(' = ', 1) for ln in lines if ' = ' in ln and not ln.startswith('#'))
        q_dn = L.dec_round(L.end_frac(U.lo(rv(kvl['l0_hat.D4ML0.L0_hi']).sqrt())), False)             # rounded the wrong way
        b_dn = L.dec_round(L.end_frac(U.lo(rv(kvl[r0_ + 'q_hat_hi']) + rv(kvl[r0_ + 'T_s']))), False)
        p_dq = [('%s = %s' % (kq, q_dn)) if ln.startswith(kq + ' = ') else ln for ln in lines]
        p_db = [('%s = %s' % (kb, b_dn)) if ln.startswith(kb + ' = ') else ln for ln in lines]
        plant('PLANT-DEC-UP', dec_up_bad(p_dq) == [kq] and dec_up_bad(p_db) == [kb], 'the same check refuses %s written as %s (L0_hi^(1/2) '
              'rounded down) and %s written as %s (q_hat_hi + T_s rounded down)' % (kq, q_dn, kb, b_dn))
        why = FAILS + ['%s did not fire' % x for x in FIRES]
        if not why:
            with open(REC, 'x') as fh:
                fh.write('\n'.join(lines) + '\n')
            out('RECORD %s sha256 %s' % (os.path.basename(REC), sha(REC)))          # Rule V2 (INTERFACE sect. 5)
        else:
            out('NO RECORD written (no record when a gate fails or a plant does not fire)')
    except Refused as e:
        out('REFUSED %s' % e)
        out('VERDICT INVALID (REFUSED)')
        return 1
    except Exception as e:
        for ln in traceback.format_exc().split('\n')[-16:]:
            out('TRACE ' + ln)
        out('ERROR at cpu %.1f s: %r' % (time.process_time() - T0, e))
        out('VERDICT INVALID (ERROR)')
        return 1
    why = FAILS + ['%s did not fire' % x for x in FIRES]
    out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (ITEM, time.process_time() - T0,
                                                          resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
