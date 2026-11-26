#!/usr/bin/env python3
"""m3_run_v1_7.py -- pk03 (code/pk03/). REVISION of m3_run_v1_6_1.py (fd935f57) after batch 1, which stopped at
Nk2.4 (CAP-STOP inside entry I_N: one entry needs more than a 540-s piece): entries are resumable between units (m3_bar_v8, 73273def).
- run_nk asks a budget before each unit: cpu + factor x the slowest unit (or per-entry series time) so far, at least 60 s, must stay within
  LIM - 20; the first unit of every piece always runs, so each piece advances. A stop hands off the completed entries, 'next' and
  'partial' (the entry's state: name, groups digest, the computed units' exact intervals, maxrel). The next piece resumes from the last
  valid hand-off (capped pieces skipped, factor doubled per capped piece). asm checks that every piece advances, by more entries or by
  more units of the entry in progress, that a carried state names the entry at 'next', and that no entry is left in progress (C-PIECES).
- C-RESUME (item D.N): one free D entry computed straight and from forced checkpoints at the end of stages a and b, each state through the
  hand-off codec and resumed with fresh caches, must give identical a_k and bars. PLANT-RESUME: the stage-a state with m0u doubled must
  change the bars.
- Pieces Nk1.N .. Nk19.N. TABLE-CPU (per moment table), UNIT (per unit) and GDATA-CPU (per entry) lines come from m3_bar_v8.
- Records and reader unchanged: m3_record_v4 (b2671d5a) and m3_reader_v4_4 (a5ba5c80); consumers keep their pins. Names are m3_run_v1_7's.
m3_run_v1_6_1: REVISION of m3_run_v1_6.py (de3f8e32, never run or cited), for the review
ad0ceca7 of m3_run_v1_5_1 and its ADD1 18a634fa: m3_reader_v4_4 (a5ba5c80) makes the bound loader the only certified entry point,
load(path, asm_out, J_REF, N), with loads(text, out_text, J_REF, N, name) in memory; the writer's C-FMT and plants call check_text,
the certified parse without the binding, before any file is written. C-BOUND-RT and the PLANT-BOUND-* plants call loads. Names are
m3_run_v1_6_1's; everything else is m3_run_v1_6's.
m3_run_v1_6: REVISION of m3_run_v1_5_1.py (1225b0fe, never run), for the review dfdc53da of
m3_run_v1_5 and ADD5 (sects. 1 and 4) and its check 6fb765fd of the M2(b) addendum:
- asm writes no file until every gate and plant has passed. It builds the five record texts, runs C-FMT on the texts
  (m3_reader_v4_3.loads), runs every plant and checks ctx.prec (C-PREC-ASM); only then does write_records write, and it refuses while
  any gate has failed, any plant has not fired or the TAG is not certified. PLANT-NOWRITE drives write_records with a forced gate
  failure, a forced unfired plant and a PRECERT tag: it must open no file. C-WRITE, after the write, checks each file against its text.
- Consumers bind each record to its asm output: asm prints 'RECORD <file name> <sha256>' for each file written, and
  m3_reader_v4_3.load_bound requires that line and VERDICT lines exactly ['VERDICT VALID'] (C-BOUND-RT; PLANT-BOUND-VERDICT,
  PLANT-BOUND-INVALID, PLANT-BOUND-TWO, PLANT-BOUND-SHA, PLANT-BOUND-NONE).
- m3_record_v4 (b2671d5a) requires the full kernel field: kernel_file, kernel_sha256, kernel_prec, validation [v1, v2, v3, v4, close],
  arb_kernel_file and arb_kernel_sha256 (arbeng_ma_stub_v1_1), arb_base_file and arb_base_sha256 (arbeng_c2b_v2). m3_reader_v4_3
  (adf51038) pins all of them (PLANT-ARBB for the base).
- C-HASH-REF reads the float references' VERDICT and TRIAL lines by exact equality.
- A capped N piece (no hand-off; its output's first line names this script and item, and its VERDICT lines are exactly
  ['VERDICT INCOMPLETE (CAP-STOP)']) is kept and skipped. The next piece resumes from the last valid hand-off, with its stop factor
  doubled per capped piece, and asm skips the capped piece in its walk (PIECE-CAPPED). Any other output without a hand-off is an error.
Names are m3_run_v1_6's.
m3_run_v1_5_1: REVISION of m3_run_v1_5.py (0283c60c, never run), for the review c897cdd7 of
pk02's SPEC_M2B_CERT_v1 sect. 4 (fixes 1, 2, 4 and sect. 5, as SPEC_M2B_CERT_v1_ADD1 2c97391f sects. 3, 4, 6, 7 carry them):
- every record carries kernel_prec (ctx.prec, 512) beside kernel_file, the full kernel_sha256 and the validation list, and its engine
  field gives full sha256s; m3_reader_v4_2 (0dad53a3) tests (file, sha256, prec, validation), the arb engine pin, the expected
  J_REF and N, and FORMAT and claim by exact allow-list;
- each record is bound to the run output that wrote it: asm prints one RECORD <file> <full sha256> line per record, and after asm
  ends with exactly ['VERDICT VALID'] pk03 writes a side manifest of that output's and the records' sha256 (sha256sum);
- C-PREC-END: each item ends with flint ctx.prec 512 (C-PREC checks the start);
- PLANT-READER-PREC, PLANT-LAYER-V1_1, PLANT-LAYER-V1_2, PLANT-CLAIM, PLANT-ARBK and PLANT-N join v1_5's plants.
Names are m3_run_v1_5_1's. m3_run_v1_5: The CERTIFIED Lemma 19.1c entries of S7 (PLAN_M3_CODE_v1 sects. 3-7, v1_1, v1_2,
ADD1-ADD5) on the closed M-a layer.
REVISION of m3_run_v1_4.py (71601c33, PRECERT) for ADD5 and the T48:
- Kernel arbeng_ma_v1_3 (075e3586), CLOSED by the review, ctx.prec 512 (C-PREC). The arb recompute
  engine is arbeng_ma_stub_v1_1 (4fc7e49d, over arbeng_c2b_v2 fb8cd1b5): only MAFallback is caught, and the guard, PLANT-GUARD and
  C-FALLBACK-PATH stay.
- C-VALIDATED: VALIDATED is keyed by (file, full sha256, the sha256s of kt_ma_val_v1_5's four outputs and of the close). The imported
  module's file must be pk02/arbeng_ma_v1_3.py with the pinned sha256; each validation output must hold exactly one VERDICT line,
  "VERDICT VALID"; v1_1 and v1_2 are denied by sha (tag_for, PLANT-DENY). This script runs only certified: TAG '' is required, and
  anything else is VERDICT INVALID.
- Modules: m3_bar_v8 (73273def), m3_record_v4 (b2671d5a), m3_reader_v4_4 (a5ba5c80) and m3_handoff_v3 (f73ea21f).
  - m3_bar_v8: v7's bars (prep norms take the M-a ball, C-BUDGET after the root, ex kept), resumable between units.
  - m3_record_v4: FORMAT 'M3_RECORD_v1', the full kernel field, kind 'entry'.
  - m3_reader_v4_4: the validated-layer pin with kernel_prec, the arb engine and base pins, expected J_REF and N, kinds, exact FORMAT
    and claim, and the bound load, the consumers' only certified entry point.
  - m3_handoff_v3: exact verdict lines.
- C-BUDGET: the largest relative radius of a norm entering the bars <= 1e-3, plus rnd <= 0.1 x bar. The a_k relative radii are INFO
  (ADD5 sect. 2). C-REP-B is unchanged: per part 1 - 1e-6 <= certified/float <= 1.15 (ADD5 sect. 3). ENTRY lines print every part at
  %.9e.
- Hand-offs require the producer record's VERDICT lines to equal exactly ['VERDICT VALID'] (T48 rule 2; PLANT-VERDICT).
- N entries run in resumable pieces Nk1.N .. Nk19.N, stopping between units (above); asm reads the pieces until 'next' reaches the end,
  skipping capped pieces and checking that each advances (C-PIECES).
- At asm, the records are m3_<f>_N<N>_J300_v1_7.json (FORMAT 'M3_RECORD_v1'). C-FMT reads each text back with
  m3_reader_v4_4.check_text(text, 300, N) before any write; each file written is named with its full sha256 on a RECORD line.
  Plants: PLANT-FMT, PLANT-RND, PLANT-READER-PRECERT, PLANT-READER-KERNEL, PLANT-READER-PREC, PLANT-LAYER-V1_1, PLANT-LAYER-V1_2,
  PLANT-CLAIM, PLANT-ARBK, PLANT-ARBB, PLANT-JREF, PLANT-N, PLANT-KIND, the five PLANT-BOUND-* and PLANT-NOWRITE.
Items (N = 4 or 3), one at a time, each under its LIM: D.N, mix.N, free2.N (prep and entries); Nu.N, Nc.N (the N prep's stages u and c,
single pieces by m3_probe_u_v2_1 9606d4a8); Nk1.N .. Nk19.N (resumable N entry pieces); asm.N. Every gate of m3_run_v1_4 is kept: C-HASH,
C-IMPORT, C-SERIES, C-PREC, C-CX, C-CX2, PLANT-GUARD, C-FALLBACK-PATH, PLANT-FALLBACK-ONLY, C-TILT, C-PREP-REF, C-MONO-FAR, C-ODD,
C-ODD-AK, C-HANDOFF(-RT), C-SCOPE, C-KR4, C-REP-B, C-REP-AK, C-FMT, C-KBAR, with their plants; C-PREC-END since v1_5_1; new in v1_6:
C-BOUND-RT, C-PREC-ASM and C-WRITE; new in v1_7: C-RESUME and PLANT-RESUME.
Arguments: ITEM LIM (5..540). Output: stdout (the run line redirects it to out/m3_run_v1_7_<ITEM>.out); hand-offs in hand/; records in out/.
Run: D=/mnt/g2/release/root/code/pk03; OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=$D/tmp
  timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B $D/m3_run_v1_7.py ITEM LIM
  > $D/out/m3_run_v1_7_ITEM.out 2> $D/out/m3_run_v1_7_ITEM.err
"""
import resource, sys, time, math, hashlib, signal, os, json, re, traceback

ITEM_RE = r'(D|mix|free2|Nu|Nc|Nk[1-9]|Nk1[0-9]|asm)\.(4|3)'
if len(sys.argv) != 3 or not re.fullmatch(ITEM_RE, sys.argv[1]):
    print('usage: m3_run_v1_7.py ITEM LIM   (ITEM = D|mix|free2|Nu|Nc|Nk1..Nk19|asm . 4|3; LIM = RLIMIT_CPU soft limit in s, 5..540)')
    sys.exit(2)
ITEM = sys.argv[1]
FAM, NN = ITEM.split('.')[0], int(ITEM.split('.')[1])
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
STAGE = ['start']


def cpu():
    return time.process_time()


def out(line):
    print(line, flush=True)


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk03'
C2B = CODEDIR + '/pk02'
INP = CODEDIR + '/pk10/scratch'
W4 = CODEDIR + '/pk11/out'
OUTD = OWN + '/out'
HANDD = OWN + '/hand'
KERNEL = 'arbeng_ma_v1_3'
ARBK = 'arbeng_ma_stub_v1_1'
ARBB = 'arbeng_c2b_v2'   # the arb base under ARBK (pinned in KFILES)
KFILES = {
    'arbeng_ma_v1_3.py': '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be',
    'arbeng_ma_stub_v1_1.py': '794fabc7111555db2f6390a144d3f5af6deeb358d02da8b5705cf3ceaefd0af1',
    'arbeng_c2b_v2.py': '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0',
}
VALREC = [   # the CLOSE_ARBENG_MA_V1_3 (9a290b50) conditions: kt_ma_val_v1_5's four outputs and the close itself
    (C2B + '/out', 'out_kt_ma_val_v1_5_v1.out', '5ccbb6d006f5365f219eb6221b7e66b76e7e7799e977148df94f34b0c3d86216'),
    (C2B + '/out', 'out_kt_ma_val_v1_5_v2.out', 'a61d893e6424b9ea524d944e40f625c934de04a2faeaa741e3fd333e97f48817'),
    (C2B + '/out', 'out_kt_ma_val_v1_5_v3.out', 'd613fe804a030be397fefa46ed1424063f794400b7d9618e12db8af046e09d93'),
    (C2B + '/out', 'out_kt_ma_val_v1_5_v4.out', '2ad13ec3cac14ef919f5e34fa19664f70eece05c3c3f208dcfec36a93cdd4473'),
    (CODEDIR + '/rv01', 'CLOSE_ARBENG_MA_V1_3_rv01.md', 'a8a5e8d020d2d1e1127c3ee8f400496011ddbd022af83180025ac3185ba22f95'),
]
VALIDATED = {('arbeng_ma_v1_3.py', '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be', tuple(v[2] for v in VALREC))}
DENY = {('arbeng_ma_v1_1.py', '81f7fb89f863343149b1558bfc3c8ba3e09b3e6c36ec00db4c12197b11158e7f'),
        ('arbeng_ma_v1_2.py', '935f2ca77dbcb7de0670d43505044f9c12c086f69de2a30f7b8133522ffcec80')}


def tag_for(kfile, ksha, vshas, validated=None):
    """'' (certified) only for a (file, full sha256, validation sha256s) in VALIDATED and never for a denied (file, sha256)."""
    if (kfile, ksha) in DENY:
        return '_PRECERT'
    return '' if (kfile, ksha, tuple(vshas)) in (VALIDATED if validated is None else validated) else (
        '_STUB' if 'stub' in kfile else '_PRECERT')


TAG = None   # set by C-VALIDATED after the imports
OWNMOD = {
    'm3_scal_v2.py': 'd22d3ad696074d4235f0fd31b026477e87f96f5d4b5331e29ab8d399e1e8f054',
    'm3_graph_v2.py': '262133cbb9cbc181d92d26114282a72a818111abdd6b96949bd8427742e16915',
    'm3_series_v2.py': '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    'm3_major_v2.py': '89dd5a2184a511d4dea39fb3c558501e9738af118be9d41f2ac4b2d4b8d7b016',
    'm3_bar_v8.py': '0dad3a36f624432080bfd2f716ed431c19dc5d398fbd5e3186090c47ab4a7bc4',
    'm3_entries_v2.py': '8c601f83b9fdc28a79df6400e34d144773c3ffebe19752895382dd0704aa7524',
    'm3_record_v4.py': '2c8a53efb5170d6c6e320bd814c824e69d2ccdd73c57cf87a9130b796109e30f',
    'm3_reader_v4_4.py': 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0',
    'm3_handoff_v3.py': 'e4f5bf0b111197d87e9659c89265c68fcfe39e564860c6e6b6eb91c9c48feb21',
}
INPUTS = {
    (OWN, 'M3_ENTRY_LIST_v1_2.json'): 'f6e844fb55249177e3cbeda4c2b974db78ea913b9dbef6f1f6880a622d9eac13',
    (W4, 'ts_N4_J170_D_S_z9sym_v1.json'): 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    (W4, 'ts_N3_S_z9sym_v1.json'): 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    (W4, 'vacres_K3_N4_sym_v1.json'): 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    (W4, 'vacres_K3_N3_sym_v1.json'): 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    (INP, 'm2_N4_J170.json.b'): '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    (INP, 'm2_N3_J170.json.b'): '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    (INP, 'b5_N4_J170.json'): 'f19d1e085ca8bc89b5d1c65a18589ebe61507886c891f5dcb924569f0f931928',
    (INP, 'b5_N3_J170.json'): '567f5543f49b4c4b379ed8724503cce3401646687ad113414617601786ee2db2',
    (INP, 'clT_N4_J170.json'): 'cfd2ab7c1be04487f8ec1b012eda42cbced4bb38310d00fcd2ac5e765b312669',
    (INP, 'clT_N3_J170.json'): '7d62c3030480a4ffb41befe931614bd790d06cf975e07963814dcac9269dc998',
    (INP, 'binding4_N4_J170.json'): '46a47036b45a90e5b0729901c764fd029cf87a92cece7597171e706b876415e4',
    (INP, 'binding4_N3_J170.json'): 'f5e90b08d606c2cec7e33635ebf6f45eee99925c125e82beaa3f162c91d46f6e',
    (INP, 'endw_N4_J170.json'): 'e8b1fe300f1de5ac1a1909c101afb6e00c5008b96de1747007accf5a6946f9c4',
    (INP, 'endw_N3_J170.json'): '0db59cc3459200ec06c5583b988291f7ab28eff9beeee8609ac93cdb4cf49d67',
    (OUTD, 'm3ref_v1_D.4.all.out'): '3ab76eb616846c6f70a13d64d364a7f6e904a1bdc51e788170551868a1854cc7',
    (OUTD, 'm3ref_v1_D.3.all.out'): '1a0c38dd0ed079a189496a2fb920cdde7df97bd4235fa49753b08c0a8a8af3d1',
    (OUTD, 'm3ref_v1_N1.4.all.out'): 'e21f3db18b21afc2bc0b56ceb06be97a3407e877728733c2a228bd9c160d8e7d',
    (OUTD, 'm3ref_v1_N1.3.all.out'): '2cc4445bb4ff045eeb6ba07a6ec07d20d82b2b280b90e52eeb8d3dd4f7c8e950',
    (OUTD, 'm3ref_v1_mix.4.all.out'): 'e178c9f694ab1fb7304abb7d49e979b8d786b74d972ba4edc7626ec663302c04',
    (OUTD, 'm3ref_v1_mix.3.all.out'): '67d9a636080c7f01202899effb3c5c3287436d8aba5c6a0b5fa5d598e7f4bbc5',
    (OUTD, 'm3ref_v1_free.4.all.out'): 'fb87c976cc324a071a674b31e63244444e23fd9394a2592dbddf76c5b5f6f064',
    (OUTD, 'm3ref_v1_free.3.all.out'): '9aa266628041b25e90430704c6733c263bf89a2bf1cacc5ed023cd10cdb4e1f6',
    (OUTD, 'm3ref_v1_2_D.4.all_z9sym.out'): '14b5f1910b5777b89f939127b107e1884a2cb7dbaca4d8a961b55f5b1868446f',
    (OUTD, 'm3ref_v1_2_N0T.4.all_z9sym.out'): 'c4700f0c1d8164735f83315bfe0c07fc97cad5c28294e9235b90e196921b1327',
    (OUTD, 'm3ref_v1_2_N0m.4.all_z9sym.out'): '4af1808ef405d1671daf2cab0c3d73f1539428e0b393f9c48aae11f9a5ed2ce3',
    (OUTD, 'm3ref_v1_2_N1.4.all_z9sym.out'): '9af0ce8ef35c24d60a09e6237a5333ff513fa336d78b497da3ef193309028ee8',
    (OUTD, 'm3ref_v1_2_N2.4.all_z9sym.out'): '49b484ed1334b17a868146589c7196a306010f87c55291123dc08323ef73acfe',
    (OUTD, 'm3ref_v1_2_mix.4.all_z9sym.out'): '94a36828d07ae51af934d3a0e9e284a28df657d979bef1c2954749fe15914814',
    (OUTD, 'm3ref_v1_2_free.4.all_z9sym.out'): '9527a96047a95aeccaea52c8d2cca62d4a35d2f0d8129aed201c0ce08051d4bc',
    (OUTD, 'm3ref_v1_2_D.3.all_z9sym.out'): 'c34f79f76ea42e87d959109559502dff28a432e56b0158ff2a0d93508e79c7ce',
    (OUTD, 'm3ref_v1_2_N0T.3.all_z9sym.out'): '750039535e6adc2dc8042e53607f83805677fa124a43e4d149bb762479b81259',
    (OUTD, 'm3ref_v1_2_N0m.3.all_z9sym.out'): '2f83ae76b537068c3a7352acaec06e1a75727dda9ad36b7990117c87dd2c720e',
    (OUTD, 'm3ref_v1_2_N1.3.all_z9sym.out'): '1dfc0231da346454e2ac38e8e4a0c95b2fee27329544d5a4f084a518f04d4557',
    (OUTD, 'm3ref_v1_2_N2.3.all_z9sym.out'): 'fa0893bdb8b6c4ef2819a3f53e543c6cc53d3d2d68c7c282b81bb460632989a5',
    (OUTD, 'm3ref_v1_2_mix.3.all_z9sym.out'): 'ff8ce1302c4af1ae0044edf48086dec5e66f830dfb6b1d096088461b2ef67c05',
    (OUTD, 'm3ref_v1_2_free.3.all_z9sym.out'): '0d8da9258c06611ee248362d1959b917f3dd1f5ff671522ac9324441f95df2b2',
}

FAILS, NOFIRE = [], []


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def valid_verdict():
    """the exact verdict line of a valid run of this script (certified TAG '' is required, so 'VERDICT VALID')."""
    return 'VERDICT VALID'


def finish():
    if 'S' in globals():
        out('PRECISION end: %s' % S.precision_line())
    if 'K' in globals() and 'flint' in globals():
        gate('C-PREC-END', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d at the end of the item; C-PREC checked the start)' % flint.ctx.prec)
    out('STAGE-CPU total %.2f s' % cpu())
    if FAILS or NOFIRE:
        out('VERDICT INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE]))
    elif TAG != '':
        out('VERDICT INVALID (C-VALIDATED: TAG %r; this script writes certified records only)' % (TAG,))
    else:
        out(valid_verdict())


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tsha(text):
    """the sha256 of a text as written (json.dumps texts are ASCII)."""
    return hashlib.sha256(text.encode()).hexdigest()


def flip(h):
    """h with its last hex digit changed (plants)."""
    return h[:-1] + ('0' if h[-1] != '0' else '1')


def stage(name):
    STAGE[0] = name
    out('STAGE-CPU %s start %.2f s' % (name, cpu()))


SELF_SHA = sha(os.path.abspath(__file__)); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_SELF = 'e55c5de17cde69e202d1543986ac74af1899b7975c59fb22e027c6c862207c2a'  # G-ORIG: option (C), acc2 two-producer acceptance
out('m3_run_v1_7 item %s LIM %d; script sha256 %s; python %s' % (ITEM, LIM, SELF_SHA, sys.version.split()[0]))
stage('C-HASH')
bad = [f for f, h in OWNMOD.items() if sha(os.path.join(OWN, f)) != h]
bad += [f for f, h in KFILES.items() if sha(os.path.join(C2B, f)) != h]
bad += [f for (d, f), h in INPUTS.items() if os.path.exists(os.path.join(d, f)) and sha(os.path.join(d, f)) != h]
missing = [f for (d, f), h in INPUTS.items() if not os.path.exists(os.path.join(d, f))]
gate('C-HASH', not bad and not missing, '(%d modules, the kernel files, %d inputs)%s%s' % (len(OWNMOD), len(INPUTS),
     (': changed ' + ', '.join(bad)) if bad else '', (': missing ' + ', '.join(missing)) if missing else ''))
plant('PLANT-HASH', sha(os.path.join(OWN, 'm3_scal_v2.py')) != OWNMOD['m3_scal_v2.py'][:-1] + ('0' if OWNMOD['m3_scal_v2.py'][-1] != '0' else '1'),
      '(m3_scal_v2 against a sha with its last digit changed)')
if FAILS:
    finish()
    sys.exit(1)
from fractions import Fraction
from decimal import Decimal
import importlib.util
GENERIC = [('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v2.py'), ('m3_series', 'm3_series_v2.py'), ('m3_major', 'm3_major_v2.py'),
           ('m3_bar', 'm3_bar_v8.py'), ('m3_entries', 'm3_entries_v2.py'), ('m3_record', 'm3_record_v4.py'), ('m3_reader', 'm3_reader_v4_4.py'),
           ('m3_handoff', 'm3_handoff_v3.py')]


def load_as(name, fname):
    """a pinned file of pk03/ loaded under its generic module name (dependencies first)."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(OWN, fname))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


MODS = {name: load_as(name, fname) for name, fname in GENERIC}
S, GR, SER, BAR, ENT, REC, RDR, HO = (MODS[k] for k in ('m3_scal', 'm3_graph', 'm3_series', 'm3_bar', 'm3_entries', 'm3_record', 'm3_reader',
                                                         'm3_handoff'))
sys.path.append(C2B)
import arbeng_ma_v1_3 as K
import arbeng_ma_stub_v1_1 as A
_to_arb0 = {'layer': K.to_arb, 'arb': A.to_arb}


def _guard(which):
    def conv(v):
        """the kernel's own converter, refusing mp.iv values: M3 passes arb balls only (a checked fact since m3_run_v1_3)."""
        if hasattr(v, '_mpi_'):
            raise TypeError('an mp.iv value reached the %s kernel converter; M3 passes arb only' % which)
        return _to_arb0[which](v)
    return conv


K.to_arb = _guard('layer')
A.to_arb = _guard('arb')
BAR.ARB['kern'] = A
import flint
from mpmath import iv
badw = [n for n, m in MODS.items() if os.path.abspath(m.__file__) != os.path.join(OWN, dict(GENERIC)[n])]
badw += [] if os.path.dirname(os.path.abspath(K.__file__)) == C2B else ['kernel']
badw += [] if os.path.dirname(os.path.abspath(A.__file__)) == C2B else ['arb kernel']
gate('C-IMPORT', not badw and K.VERSION == KERNEL and A.VERSION == ARBK, '(generic names from their pinned files in %s; kernel %s and arb kernel %s from %s)%s' % (
    OWN, K.VERSION, A.VERSION, C2B, (': ' + ', '.join(badw)) if badw else ''))
stage('C-VALIDATED')
vbad = []
if os.path.abspath(K.__file__) != os.path.join(C2B, KERNEL + '.py') or sha(os.path.abspath(K.__file__)) != KFILES[KERNEL + '.py']:
    vbad.append('the imported layer is not pk02/%s.py with the pinned sha256' % KERNEL)
for d_, f_, h_ in VALREC:
    p_ = os.path.join(d_, f_)
    if not os.path.exists(p_) or sha(p_) != h_:
        vbad.append('%s missing or changed' % f_)
    elif f_.startswith('out_kt_ma_val'):
        with open(p_) as fh:
            vl = [ln.rstrip('\n') for ln in fh if ln.startswith('VERDICT')]
        if vl != ['VERDICT VALID']:
            vbad.append('%s: VERDICT lines %r' % (f_, vl))
TAG = tag_for(KERNEL + '.py', KFILES[KERNEL + '.py'], [v[2] for v in VALREC])
gate('C-VALIDATED', not vbad and TAG == '', '(layer %s:%s; %d validation records with exactly ["VERDICT VALID"] and the close by sha256; TAG %r)%s' % (
    KERNEL, KFILES[KERNEL + '.py'][:8], len(VALREC), TAG, (': ' + '; '.join(vbad)) if vbad else ''))
d11 = [k for k in DENY if k[0] == 'arbeng_ma_v1_1.py'][0]
plant('PLANT-DENY', tag_for(d11[0], d11[1], [v[2] for v in VALREC], set(VALIDATED) | {(d11[0], d11[1], tuple(v[2] for v in VALREC))}) != '',
      '(arbeng_ma_v1_1 placed in a copy of VALIDATED must still be refused the certified tag)')
SER_RE = re.compile(r'[A-Za-z0-9]' + '_series' + r'\s*\(')
ser_hits = []
for p_ in [os.path.join(OWN, f) for f in OWNMOD] + [os.path.join(C2B, f) for f in KFILES] + [os.path.abspath(__file__)]:
    with open(p_) as fh:
        ser_hits += ['%s:%d' % (os.path.basename(p_), i + 1) for i, ln in enumerate(fh) if SER_RE.search(ln)]
gate('C-SERIES', not ser_hits, '(no *_series( call in %d modules, the kernel files and this script)%s' % (len(OWNMOD), (': ' + ', '.join(ser_hits)) if ser_hits else ''))
plant('PLANT-SERIES', bool(SER_RE.search('x = acb' + '_series(1)')), '(a planted *_series( call must be flagged)')
S.setup()
flint.ctx.prec = K.PREC
gate('C-PREC', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d = the layer\'s PREC %d)' % (flint.ctx.prec, K.PREC))
out('PRECISION start: %s; env %s' % (S.precision_line(), K.env_probes()))
cx_ok, cx_fired = S.crossings_test()
gate('C-CX', cx_ok, '(M3\'s own mp.iv <-> arb crossings: round trips contain their sources)')
plant('PLANT-CX', cx_fired, '(the unsigned to_man_exp form must lose -1/3)')


def _ef(raw):
    """an mp.iv end as an exact rational from its raw (sign, man, exp, bc); special values raise."""
    sign, man, exp, bc = raw
    if man == 0 and exp != 0:
        raise ValueError('special interval end %r' % (raw,))
    v = Fraction(man) * Fraction(2) ** exp
    return -v if sign else v


cx2 = []
for lo_, hi_ in (('-0.25', '0.75'), ('-0.75', '0.25'), ('-0.5', '0')):
    x_ = iv.mpf([lo_, hi_])
    a_ = S.iv_to_arb(x_)
    b_ = [_ef(r) for r in S.arb_to_iv(a_)._mpi_]
    cx2.append(a_.contains(flint.arb(lo_)) and a_.contains(flint.arb(hi_)) and b_[0] <= Fraction(lo_) and Fraction(hi_) <= b_[1])
gate('C-CX2', all(cx2), '(asymmetric straddling and zero-end intervals [-0.25, 0.75], [-0.75, 0.25], [-0.5, 0]: iv -> arb holds both ends, '
     'arb -> iv holds the source)')
from mpmath import libmp
x_ = iv.mpf(['-0.25', '0.75'])
um = [libmp.to_man_exp(r) for r in x_._mpi_]
uarb = (flint.arb(int(um[0][0])) * flint.arb(2) ** int(um[0][1])).union(flint.arb(int(um[1][0])) * flint.arb(2) ** int(um[1][1]))
plant('PLANT-CX2', not uarb.contains(flint.arb('-0.25')), '(the unsigned to_man_exp form of [-0.25, 0.75] must lose -0.25)')
gfired = []
for mod in (K, A):
    try:
        mod.to_arb(iv.mpf(1) / 3)
        gfired.append(False)
    except TypeError:
        gfired.append(True)
plant('PLANT-GUARD', all(gfired), '(an mp.iv value handed to either kernel converter must raise)')


def fallback_tests():
    """C-FALLBACK-PATH: a MAFallback forced at a 2-form table (Gam = [[2, 1], [1, 3]], W_int = I) is recomputed by the arb kernel, whose
    ball must overlap the layer's own for the same E2; PLANT-FALLBACK-ONLY: a ValueError in the layer's E2 must reach the caller."""
    tb = BAR.TableFB(K, S.arb_mat_of([[2, 1], [1, 3]]), NN - 1, 4, None, None, [[1, 0], [0, 1]], 'fallback test')
    P = S.spoly(K, {(1, 0): 1, (0, 1): -1}, 2)
    Q = S.spoly(K, {(1, 1): 1}, 2)
    v_ma = tb.E2(P, Q)
    real = tb.tab

    class Raise:
        def __init__(self, exc):
            self.exc = exc

        def E2(self, P_, Q_, fallback=True):
            raise self.exc

    n0 = len(BAR.FALLBACKS)
    tb.tab = Raise(K.MAFallback('forced by C-FALLBACK-PATH'))
    v_arb = tb.E2(P, Q)
    gate('C-FALLBACK-PATH', len(BAR.FALLBACKS) == n0 + 1 and v_ma.overlaps(v_arb),
         '(a forced MAFallback: the arb kernel\'s E2 %s overlaps the layer\'s %s)' % (v_arb.str(12), v_ma.str(12)))
    tb.tab = Raise(ValueError('planted'))
    try:
        tb.E2(P, Q)
        fired = False
    except ValueError:
        fired = True
    plant('PLANT-FALLBACK-ONLY', fired, '(a ValueError in the layer\'s E2 must reach the caller)')
    tb.tab = real
    del BAR.FALLBACKS[:]


def fb_info():
    """the item's MAFallback recomputes (INFO), printed and kept in its hand-off."""
    out('FALLBACKS %d (MAFallback recomputes in arb, INFO)%s' % (len(BAR.FALLBACKS), (': ' + '; '.join(BAR.FALLBACKS[:20])) if BAR.FALLBACKS else ''))
    return list(BAR.FALLBACKS)


fallback_tests()
T_REF = Fraction(1, 300)


def read_lines(path, tag):
    with open(path) as fh:
        return [json.loads(ln[len(tag) + 1:]) for ln in fh if ln.startswith(tag + ' ')]


with open(os.path.join(OWN, 'M3_ENTRY_LIST_v1_2.json')) as fh:
    LIST = json.load(fh)
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TS = ENT.load_trial(os.path.join(W4, {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]),
                    os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)
TRIAL = {'ts': '%s:%s' % ({4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN],
                          INPUTS[(W4, {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN])][:8]),
         'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)][:8])}
S7 = [e for e in LIST['entries'] if 'S7' in e.get('use', {})]
REFPREP = {'D': 'm3ref_v1_D.%d.all.out', 'N': 'm3ref_v1_N1.%d.all.out', 'mix': 'm3ref_v1_mix.%d.all.out', 'free2': 'm3ref_v1_free.%d.all.out'}
REFPREPZ = {'D': 'm3ref_v1_2_D.%d.all_z9sym.out', 'N': 'm3ref_v1_2_N1.%d.all_z9sym.out', 'mix': 'm3ref_v1_2_mix.%d.all_z9sym.out',
            'free2': 'm3ref_v1_2_free.%d.all_z9sym.out'}


def name_of(e):
    return e['id'].split(':', 1)[1]


def qcap_of(e):
    """the producer's qcap: 4 for cluster_T's keys, 6 for every other S7 producer."""
    return 4 if any(u.startswith('clT ') for u in e['use']['S7']) else 6


def entries_of(graph, names=None):
    out_ = [e for e in S7 if e['graph'] == graph and (names is None or name_of(e) in names)]
    if names is not None:
        assert sorted(name_of(e) for e in out_) == sorted(names), (names, [name_of(e) for e in out_])
    return out_


def family_graph(graph):
    """the family's GraphIV with the union of the pair forms of all its S7 entries (values do not depend on unused pairs)."""
    fls = [[ENT.factor(TS, graph, enc) for enc in e['factors']] for e in S7 if e['graph'] == graph]
    return ENT.build_graph(graph, NN, fls)


def ref_prep(graph):
    return read_lines(os.path.join(OUTD, REFPREP[graph] % NN), 'PREPJSON')[0]


def make_prep(graph, g, stages, scalars=None):
    rp = ref_prep(graph)
    pr = BAR.Prep(K, g, 300, rp['a_v'], rp['ap'], rp['theta0'], 6, log=out, stages=stages, scalars=scalars)
    encl = [-iv.log(1 - S.I(a)) / (2 * S.I(a)) * (1 / S.I(300)) for a in rp['a_v']]
    gate('C-TILT', pr.ok and all(S.I(r) >= x.b for r, x in zip(pr.rates, encl)),
         '(a) %d tilt rates rounded up from their mp.iv enclosures; (b) both tilts certainly positive definite (lowest pivots %s, %s)' % (
             len(pr.rates), None if not pr.tilt_c else S.down(pr.tilt_c['low']), None if not pr.tilt_p else S.down(pr.tilt_p['low'])))
    rz = read_lines(os.path.join(OUTD, REFPREPZ[graph] % NN), 'PREPJSON')[0]
    gate('C-PREP-REF', all(rp[k] == rz[k] for k in ('a_v', 'ap', 'theta0')), '(%s: a_v, ap and theta0 of %s equal those of %s)' % (
        graph, REFPREP[graph] % NN, REFPREPZ[graph] % NN))
    return pr, rp


def laws_of(pr, mF):
    """U3's laws (PLAN_M3_CODE_v1_2 sect. C) and Lemma U's far rate (lower end) for an entry with J-degree m_F."""
    g = pr.g
    cF = mF + Fraction(g.n * (g.V - 1), 2)
    rate = pr.alpha_lo - S.I(cF) / 300
    return {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, g.Gvv)]},
            'ann': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, pr.tilt_p['Gvv'])]},
            'far_rate': S.down(rate), 'far_cF': str(cF)}, rate


def compute_entry(pr, e, state=None):
    """one entry: (result dict for the hand-off). Parity zeros: C-ODD and a_k balls containing 0, no bars."""
    name = name_of(e)
    facs = [ENT.factor(TS, e['graph'], enc) for enc in e['factors']]
    pr.qcap = qcap_of(e)
    pr.maxrel = 0.0
    t0 = cpu()
    STAGE[0] = 'entry %s' % name
    if e['parity'] == 'zero':
        ok, why = ENT.c_odd(e['graph'], NN, facs)
        gate('C-ODD', ok, '%s: %s' % (name, why))
        ak, _, info = pr.bound(facs, e.get('grouping', 'std'), bars=False, entry=name, state=state)
        has0 = all(a.a <= 0 <= a.b for a in ak)
        gate('C-ODD-AK', has0, '%s: every a_k ball contains 0 (widest %.1e)' % (name, max(float((a.b - a.a).b) for a in ak)))
        out('STAGE-CPU entry %s %.2f s (parity zero)%s' % (name, cpu() - t0, resumed(state)))
        return {'name': name, 'parity': 'zero', 'ak': ak, 'qcap': pr.qcap, 'cpu': cpu() - t0}
    ak, bars, info = pr.bound(facs, e.get('grouping', 'std'), entry=name, state=state)
    laws, rate = laws_of(pr, info['mF'])
    gate('C-MONO-FAR', rate.a > 0, '%s: far rate alpha_min - (m_F + n(V-1)/2)/J_REF = %.4e > 0 (m_F %d)' % (name, S.down(rate), info['mF']))
    a0 = 1 if all(f[0] == 'p' for f in facs) else None
    rec = REC.entry_record(ak, bars, T_REF, 'free', a0_exact=a0, laws=laws)
    barsum = rec['Bp']['rem'] + rec['Bp']['tail'] + rec['Bp']['ann'] + rec['Bp']['far']
    okb = pr.maxrel <= 1e-3 and rec['B']['rnd'] <= 0.1 * barsum
    gate('C-BUDGET', okb, '%s: largest relative radius of a norm %.1e (<= 1e-3), rnd %.2e <= 0.1 x bar %.3e' % (name, pr.maxrel, rec['B']['rnd'], barsum))
    out('AKRAD-INFO %s: largest relative radius of an a_k %.2e' % (name, info.get('ak_relrad', 0.0)))
    out('ENTRY %s ak %s err %.9e parts rem %.9e tail %.9e ann %.9e far %.9e rnd %.3e groups %d Dn %d forms %d' % (
        name, ['%.12g' % x for x in rec['ak']], rec['err'], rec['B']['rem'], rec['B']['tail'], rec['B']['ann'], rec['B']['far'], rec['B']['rnd'],
        info['groups'], info['Dn'], len(info['forms'])))
    out('STAGE-CPU entry %s %.2f s%s' % (name, cpu() - t0, resumed(state)))
    return {'name': name, 'parity': 'free', 'ak': ak, 'bars': bars, 'a0_exact': a0, 'laws': laws, 'qcap': pr.qcap,
            'maxrel': pr.maxrel, 'cpu': cpu() - t0}


def plant_mono(pr):
    """PLANT-MONO: with theta0 = 1e-3 the far rate must not be certainly positive."""
    g = pr.g
    alpha = min((S.I(1e-3) * S.I(pr.ap) / (2 * gv)).a for gv in g.Gvv)
    rate = alpha - S.I(Fraction(g.n * (g.V - 1), 2)) / 300
    plant('PLANT-MONO', not (rate.a > 0), '(theta0 = 1e-3: far rate %.3e)' % S.down(rate))


def plant_odd(graph):
    """PLANT-ODD: one odd-state S entry + 1e-12 in a copy of the trial set must make C-ODD refuse g,0,2's zero."""
    import copy
    ts2 = copy.deepcopy(TS)
    ts2.S[1][2] = ts2.S[1][2] + 1e-12
    e = [x for x in S7 if x['id'] == 'D:g,0,2'][0]
    ok, why = ENT.c_odd('D', NN, [ENT.factor(ts2, 'D', enc) for enc in e['factors']])
    plant('PLANT-ODD', not ok, '(S[1][2] + 1e-12: %s)' % why)


def header(fam):
    return {'script': SELF_SHA, 'item': ITEM, 'family': fam, 'N': NN, 'kernel': '%s:%s' % (KERNEL, KFILES[KERNEL + '.py'][:8]),
            'arb_kernel': '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), 'trial': TRIAL, 'format': 'm3_run_v1_7 hand-off'}




def same(x, y):
    """exact equality of hand-off values: intervals by their raw ends, containers recursively."""
    if hasattr(x, '_mpi_') or hasattr(y, '_mpi_'):
        return hasattr(x, '_mpi_') and hasattr(y, '_mpi_') and x._mpi_ == y._mpi_
    if isinstance(x, dict) and isinstance(y, dict):
        return set(map(str, x)) == set(map(str, y)) and all(same(x[k], y[str(k)] if str(k) in y else y[k]) for k in x)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        return len(x) == len(y) and all(same(a, b) for a, b in zip(x, y))
    return x == y


def write_handoff(fam, body):
    name = 'm3_run_v1_7_%s.json' % ITEM
    path, hsha = HO.write(name, header(fam), body)
    out('HANDOFF %s %s' % (name, hsha))
    with open(path) as fh:
        text = fh.read()
    hdr_rt, body_rt = HO.read_text(text, {'script': SELF_SHA, 'item': ITEM, 'N': NN})
    gate('C-HANDOFF-RT', same(body, body_rt), '(the hand-off decodes to exactly the values written)')
    for lab, refused in HO.plant_handoff(text, {'script': SELF_SHA, 'item': ITEM, 'N': NN}):
        plant('PLANT-HANDOFF', refused, '(%s tampered in memory)' % lab)
    plant('PLANT-VERDICT', HO.plant_verdict(valid_verdict()), '(a producer record whose VERDICT line extends %r must be refused)' % valid_verdict())


def read_handoff(item, fam):
    name = 'm3_run_v1_7_%s.json' % item
    hdr, body = HO.read(name, ACC.out(os.path.join(OUTD, 'm3_run_v1_7_%s.out' % item), SELF_SHA, ORIG_SELF), {'script': ACC.expect(os.path.join(HANDD, name), SELF_SHA, ORIG_SELF), 'item': item, 'N': NN, 'family': fam},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (name, valid_verdict()))
    return body


def r_main_iv():
    """endw's r_main = main_mix^2/(main_D main_free) = exp(2 logmain(mix) - logmain(free2) - logmain(D)), J-independent (V = 6 for all three)."""
    gm = ENT.build_graph('mix', NN, [])
    gfr = ENT.build_graph('free2', NN, [])
    gd = ENT.build_graph('D', NN, [])
    return S.finite(iv.exp(2 * gm.logmain(300) - gfr.logmain(300) - gd.logmain(300)))


def resumed(state):
    return (' (this piece; %d units of the entry restored)' % len(state['vals'])) if state else ''


def check_resume(pr, e):
    """C-RESUME (m3_bar_v8): one free entry computed straight, then from forced checkpoints at the end of stage a (after 'm0c') and at
    the end of stage b (before the first 'c' unit), each state through a hand-off encode/decode round trip and resumed with fresh table
    and group caches; the a_k and the bars must be identical to the straight run's. PLANT-RESUME: the stage-a state with m0u doubled
    must change the bars."""
    name = name_of(e)
    facs = [ENT.factor(TS, e['graph'], enc) for enc in e['factors']]
    gr = e.get('grouping', 'std')
    pr.qcap = qcap_of(e)

    def run(state=None, cut=None):
        pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0
        cnt = [0]
        if cut is not None:
            pr.unit_done = lambda dt, prog: cnt.__setitem__(0, cnt[0] + (1 if prog else 0))
            pr.ubudget = lambda: cnt[0] < cut
        try:
            return pr.bound(facs, gr, entry=name, state=state), None
        except BAR.Checkpoint as cp:
            return None, HO.dec(json.loads(json.dumps(HO.enc(cp.state))))
        finally:
            pr.ubudget = pr.unit_done = None
    (ak0, b0, _), _ = run()
    seq = list(pr.ustate['vals'])
    cuts = [seq.index('m0c') + 1, next(i for i, k in enumerate(seq) if k.endswith('|c'))]
    ok, why, st_a = True, [], None
    for cut in cuts:
        _, st = run(cut=cut)
        st_a = st if st_a is None else st_a
        r1, _ = run(state=st)
        same_ = st is not None and len(st['vals']) == cut and r1 is not None and same(ak0, r1[0]) and same(b0, r1[1])
        ok = ok and same_
        why.append('cut after %d of %d units: %s' % (cut, len(seq), 'identical' if same_ else 'DIFFERENT'))
    gate('C-RESUME', ok, '(%s: %s)' % (name, '; '.join(why)))
    bad = dict(st_a, vals=dict(st_a['vals']))
    bad['vals']['m0u'] = 2 * bad['vals']['m0u']
    r2, _ = run(state=bad)
    plant('PLANT-RESUME', r2 is not None and not same(b0, r2[1]), '(%s: the stage-a state with m0u doubled must change the bars)' % name)
    pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0


def run_small(graph):
    stage('graph %s' % graph)
    g = family_graph(graph)
    pr, rp = make_prep(graph, g, ('u', 'c'))
    out('PREP %s N=%d: V %d, F %d, radii from %s, theta0 %r; rE %.6e nC8 %.6e nC6 %.6e farbase %.6e' % (
        graph, NN, g.V, g.F, REFPREP[graph] % NN, rp['theta0'], float(pr.rE.mid), float(pr.nC8.mid), float(pr.nC6.mid), float(pr.farbase.b)))
    plant_mono(pr)
    if graph == 'D':
        plant_odd(graph)
    res = [compute_entry(pr, e) for e in entries_of(graph)]
    if graph == 'D':
        check_resume(pr, [x for x in entries_of('D') if x['parity'] == 'free'][0])
    body = {'family': graph, 'entries': res, 'scal_u': pr.scalars_out('u'), 'scal_c': pr.scalars_out('c')}
    if graph == 'mix':
        rm = r_main_iv()
        body['r_main'] = rm
        out('R_MAIN %r in [%r, %r]' % (float(rm.mid), S.down(rm), S.up(rm)))
    body['fallbacks'] = fb_info()
    write_handoff(graph, body)


def run_prep_stage(stg):
    stage('N prep stage %s' % stg)
    g = family_graph('N')
    pr, rp = make_prep('N', g, (stg,))
    body = {'family': 'N', 'stage': stg, 'scal': pr.scalars_out(stg)}
    if stg == 'c':
        plant_mono(pr)
    body['fallbacks'] = fb_info()
    write_handoff('N', body)


def nk_order():
    """the N entries in M3_ENTRY_LIST_v1_2's order (the resumable pieces walk it)."""
    return [name_of(e) for e in entries_of('N')]


CAPPED = 'VERDICT INCOMPLETE (CAP-STOP)'


def piece_state(piece):
    """'valid' (its hand-off exists; read_handoff checks it), 'capped' (no hand-off; the output's first line names this script and
    item, and its VERDICT lines are exactly [CAPPED]) or 'missing' (no output); anything else raises ValueError."""
    item = 'Nk%d.%d' % (piece, NN)
    po = os.path.join(OUTD, 'm3_run_v1_7_%s.out' % item)
    ho = os.path.join(HANDD, 'm3_run_v1_7_%s.json' % item)
    if not os.path.exists(po):
        if os.path.exists(ho):
            raise ValueError('%s: a hand-off without its producer output' % item)
        return 'missing'
    if os.path.exists(ho):
        return 'valid'
    with open(po) as fh:
        lines = fh.read().split('\n')
    m = re.fullmatch(r'm3_run_v1_7 item (\S+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)', lines[0])
    if m and m.group(1) == item and ACC.ok(po, m.group(3), SELF_SHA, ORIG_SELF) and HO.verdict_ok(lines, CAPPED):
        return 'capped'
    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)


def run_nk(piece):
    stage('N keys piece %d' % piece)
    order = nk_order()
    g = family_graph('N')
    su = read_handoff('Nu.%d' % NN, 'N')['scal']
    sc = read_handoff('Nc.%d' % NN, 'N')['scal']
    start, caps, partial = 0, 0, None
    for j in range(piece - 1, 0, -1):
        st = piece_state(j)
        if st == 'capped':
            caps += 1
            continue
        if st != 'valid':
            raise ValueError('Nk%d.%d is %s, so piece %d cannot start' % (j, NN, st, piece))
        prev = read_handoff('Nk%d.%d' % (j, NN), 'N')
        start, partial = prev['next'], prev['partial']
        break
    factor = 1.5 * 2 ** caps
    nin = len(partial['vals']) if partial else 0
    out('PIECE-START piece %d resumes at entry %d%s after %d capped piece(s); stop factor %.1f' % (
        piece, start, (' with %d units of %s restored' % (nin, partial['entry'])) if partial else '', caps, factor))
    pr, rp = make_prep('N', g, (), scalars=dict(su, **sc))
    slow, units = [60.0], [0]

    def budget():
        return units[0] == 0 or cpu() + factor * slow[0] <= LIM - 20

    def done(dt, progress):
        slow[0] = max(slow[0], dt)
        if progress:
            units[0] += 1
    pr.ubudget, pr.unit_done = budget, done
    res, i, part = [], start, None
    while i < len(order):
        try:
            res.append(compute_entry(pr, entries_of('N', [order[i]])[0], state=partial))
        except BAR.Checkpoint as cp:
            part = cp.state
            break
        partial = None
        i += 1
    pr.ubudget = pr.unit_done = None
    nout = len(part['vals']) if part else 0
    prog = i > start or (part is not None and nout > nin)
    gate('C-PIECE', prog, '(piece %d: entries %d..%d of %d done, next %d; %d units computed%s)' % (
        piece, start, i - 1, len(order), i, units[0], (', %d units of %s carried' % (nout, part['entry'])) if part else ''))
    write_handoff('N', {'family': 'N', 'piece': piece, 'start': start, 'next': i, 'partial': part, 'stop_factor': factor,
                        'entries': res, 'fallbacks': fb_info()})


REFZ = ['m3ref_v1_2_%s.%d.all_z9sym.out' % (f, NN) for f in ('D', 'N0T', 'N0m', 'N1', 'N2', 'mix', 'free')]
FILES = ('m2', 'b5', 'clT', 'binding4', 'endw')
PK10 = {'m2': 'm2_N%d_J170.json.b', 'b5': 'b5_N%d_J170.json', 'clT': 'clT_N%d_J170.json', 'binding4': 'binding4_N%d_J170.json',
           'endw': 'endw_N%d_J170.json'}


def pk10_items(f):
    with open(os.path.join(INP, PK10[f] % NN)) as fh:
        d = json.load(fh)
    return {'I_N': d['I_N']} if f == 'binding4' else d['items']


def write_records(texts, paths, fails, nofire, tag, opener=open):
    """writes the record texts (open 'x', inside out/, no file there yet) only when no gate has failed, every
    plant so far has fired and the TAG is certified; returns [(file key, path)] written, or [] when it refuses."""
    if fails or nofire or tag != '':
        return []
    for f in FILES:
        if os.path.dirname(os.path.abspath(paths[f])) != OUTD or os.path.exists(paths[f]):
            raise ValueError('record path %s: outside out/ or already there' % paths[f])
    done = []
    for f in FILES:
        with opener(paths[f], 'x') as fh:
            fh.write(texts[f])
        done.append((f, paths[f]))
    return done


def run_asm():
    stage('asm')
    res = {}
    rmain = None
    for item, fam in (('D', 'D'), ('mix', 'mix'), ('free2', 'free2')):
        body = read_handoff('%s.%d' % (item, NN), fam)
        for r in body['entries']:
            res[(body['family'], r['name'])] = r
        if item == 'mix':
            rmain = body['r_main']
    order, nxt, piece, nin = nk_order(), 0, 1, 0
    while nxt < len(order) and piece <= 19:
        st = piece_state(piece)
        if st == 'missing':
            break
        if st == 'capped':
            out('PIECE-CAPPED Nk%d.%d: a clean CAP-STOP of this script, no hand-off; skipped and kept' % (piece, NN))
            piece += 1
            continue
        body = read_handoff('Nk%d.%d' % (piece, NN), 'N')
        pt = body['partial']
        nout = len(pt['vals']) if pt else 0
        okp = body['start'] == nxt and (body['next'] > nxt or nout > nin) and (pt is None or (body['next'] < len(order) and pt['entry'] == order[body['next']]))
        gate('C-PIECES', okp, '(Nk%d.%d: entries %d..%d complete%s)' % (piece, NN, body['start'], body['next'] - 1,
                                                                         (', %d units of %s carried' % (nout, pt['entry'])) if pt else ''))
        for r in body['entries']:
            res[('N', r['name'])] = r
        nxt, piece, nin = body['next'], piece + 1, nout
    gate('C-PIECES', nxt == len(order) and nin == 0, '(the N pieces cover all %d N entries, in order, none left in progress)' % len(order))
    refs = {}
    for fn in REFZ:
        p = os.path.join(OUTD, fn)
        with open(p) as fh:
            txt = fh.read()
        lines = txt.split('\n')
        okv = HO.verdict_ok(lines, 'VERDICT VALID') and [ln for ln in lines if ln.startswith('TRIAL')] == ['TRIAL z9sym']
        gate('C-HASH-REF', okv, '(%s, sha256 %s: VERDICT lines exactly [VERDICT VALID], TRIAL lines exactly [TRIAL z9sym])' % (fn, sha(p)))
        for d in read_lines(p, 'KEYJSON'):
            refs[d['key']] = d
    files = {f: {} for f in FILES}
    for e in S7:
        r = res[(e['graph'], name_of(e))]
        uses = e['use']['S7']
        prim = uses[0]
        for u in uses:
            f, key = u.split(' ', 1)
            if r['parity'] == 'zero':
                files[f][key] = REC.entry_record(None, None, T_REF, 'zero', alias_of=None if u == prim else prim)
            else:
                files[f][key] = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=r['a0_exact'], laws=r['laws'],
                                                 alias_of=None if u == prim else prim)
    # C-SCOPE, C-KR4, C-REP-B
    want = {f: set(pk10_items(f)) for f in FILES}
    okscope = all(set(files[f]) == want[f] for f in FILES)
    gate('C-SCOPE', okscope, '(the five files hold exactly pk10\'s keys: %s)' % ', '.join('%s %d' % (f, len(files[f])) for f in FILES))
    plant('PLANT-SCOPE', not all(set(list(files[f])[1:] if f == 'b5' else files[f]) == want[f] for f in FILES), '(b5 without one key)')
    kr4 = []
    for f in FILES:
        si = pk10_items(f)
        for key, it in files[f].items():
            d = si[key]
            e170 = d['err'] if 'err' in d else sum(d['B'].values())
            kr4.append((Fraction(it['err']) <= Fraction(1186, 1000) * Fraction(e170), f, key, it['err'] / e170))
    worst = max(kr4, key=lambda x: x[3])
    gate('C-KR4', all(x[0] for x in kr4), '(err <= 1.186 x pk10 J170 err for %d keys; largest ratio %.3e at %s %s)' % (len(kr4), worst[3], worst[1], worst[2]))
    e170w = Fraction(files[worst[1]][worst[2]]['err']) / Fraction(worst[3])
    plant('PLANT-KR4', not (Fraction(12, 10) * e170w <= Fraction(1186, 1000) * e170w), '(an err set to 1.2 x its J170 err must fail C-KR4)')
    rep = []
    for e in S7:
        r = res[(e['graph'], name_of(e))]
        if r['parity'] == 'zero':
            continue
        it = files[e['use']['S7'][0].split(' ')[0]][e['use']['S7'][0].split(' ', 1)[1]]
        fb = refs[name_of(e)]['B']
        for p in ('rem', 'tail', 'ann', 'far'):
            if fb[p] > 0:
                rep.append((it['B'][p] / fb[p], name_of(e), p))
    lo_, hi_ = min(rep), max(rep)
    gate('C-REP-B', 1 - 1e-6 <= lo_[0] and hi_[0] <= 1.15, '(%d bar parts against m3ref_v1_2 z9sym: certified/float in [%.9f (%s %s), %.6f (%s %s)])' % (
        len(rep), lo_[0], lo_[1], lo_[2], hi_[0], hi_[1], hi_[2]))
    plant('PLANT-REPB', not (1 - 1e-6 <= lo_[0] * 0.5), '(the smallest ratio times 0.5)')
    rak = []
    for e in S7:
        r = res[(e['graph'], name_of(e))]
        if r['parity'] == 'zero':
            continue
        for k, (a, fa) in enumerate(zip(r['ak'], refs[name_of(e)]['ak'])):
            rak.append((abs(float(a.mid) - fa) / max(1.0, abs(fa)), name_of(e), k))
    wr = max(rak)
    gate('C-REP-AK', wr[0] <= 1e-9, '(%d a_k against m3ref_v1_2 z9sym: largest |certified mid - float| / max(1, |float|) %.2e at %s a_%d)' % (
        len(rak), wr[0], wr[1], wr[2]))
    plant('PLANT-REPAK', not (wr[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')
    # the texts, C-FMT on the texts, the plants, and only then the write
    tag = TAG
    eng = {'m3_run_v1_7': SELF_SHA, 'modules': dict(OWNMOD)}
    kern = {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}
    fams = {gr: {k: ref_prep(gr)[k] for k in ('a_v', 'ap', 'theta0')} for gr in ('D', 'N', 'mix', 'free2')}
    texts, paths = {}, {}
    for f in FILES:
        extra = {}
        if f == 'm2':
            extra = {'kbar': KBAR, 'kbar_exact': REC.kbar_exact(KBAR), 'kbar_used_by': ['Nw', 'I3p', 'I3c', 'Ip3', 'A0w'],
                     'kbar_statement': 'w~ = xi+ - kbar_exact in every entry of this file that uses w~'}
        if f == 'endw':
            extra = {'r_main': float(rmain.mid), 'r_main_lo': S.down(rmain), 'r_main_hi': S.up(rmain)}
        top = REC.top_level(NN, 300, fams, TRIAL, eng, tag, kern, extra=extra)
        rec = dict(top, **({'I_N': files[f]['I_N']} if f == 'binding4' else {'items': files[f]}))
        texts[f] = json.dumps(rec)
        paths[f] = os.path.join(OUTD, 'm3_%s_N%d_J300%s_v1_7.json' % (f, NN, tag))
        rd = RDR.check_text(texts[f], 300, NN, name=os.path.basename(paths[f]))
        okf = all(rd['entries'][k] == (files[f][k]['ak'], files[f][k]['err']) for k in files[f])
        gate('C-FMT', okf, '(%s: %d keys read back exactly from the text by m3_reader_v4_4; %d bytes; sha256 %s)' % (
            os.path.basename(paths[f]), len(files[f]), len(texts[f]), tsha(texts[f])))
    dd = json.loads(texts['b5'])
    k0 = sorted(dd['items'])[0]
    dd['items'][k0]['B'].pop('rnd')
    try:
        RDR.check_text(json.dumps(dd), 300, NN)
        plant('PLANT-FMT', False, '(b5 copy without one rnd)')
    except ValueError:
        plant('PLANT-FMT', True, '(b5 copy without one rnd)')
    dd2 = json.loads(texts['b5'])
    kr = max((k for k in dd2['items'] if dd2['items'][k]['parity'] == 'free'), key=lambda k: sum(dd2['items'][k]['ak_rad']))
    dd2['items'][kr]['B']['rnd'] = 0.0
    try:
        RDR.check_text(json.dumps(dd2), 300, NN)
        plant('PLANT-RND', False, '(b5 copy with %s rnd = 0)' % kr)
    except ValueError:
        plant('PLANT-RND', sum(dd2['items'][kr]['ak_rad']) > 0, '(b5 copy with %s rnd = 0; its ak_rad sum %.1e)' % (kr, sum(dd2['items'][kr]['ak_rad'])))
    deny = dict(DENY)
    nx = 3 if NN == 4 else 4
    for lab, mut, jref, nexp in (('PLANT-READER-PRECERT', 'precert', 300, NN), ('PLANT-READER-KERNEL', 'kernel', 300, NN),
                                 ('PLANT-READER-PREC', 'prec', 300, NN), ('PLANT-LAYER-V1_1', 'arbeng_ma_v1_1.py', 300, NN),
                                 ('PLANT-LAYER-V1_2', 'arbeng_ma_v1_2.py', 300, NN), ('PLANT-CLAIM', 'claim', 300, NN),
                                 ('PLANT-ARBK', 'arbk', 300, NN), ('PLANT-ARBB', 'arbb', 300, NN), ('PLANT-JREF', None, 150, NN),
                                 ('PLANT-N', None, 300, nx), ('PLANT-KIND', 'kind', 300, NN)):
        dd3 = json.loads(texts['b5'])
        if mut == 'precert':
            dd3['format'] = 'M3_RECORD_v1_PRECERT'
            dd3['claim'] = 'NOT CERTIFIED (PRECERT): ' + dd3['claim']
        elif mut == 'kernel':
            dd3['kernel_sha256'] = dd3['kernel_sha256'][:-1] + ('0' if dd3['kernel_sha256'][-1] != '0' else '1')
        elif mut == 'prec':
            dd3['kernel_prec'] = 256
        elif mut in deny:
            dd3['kernel_file'], dd3['kernel_sha256'] = mut, deny[mut]
        elif mut == 'claim':
            dd3['claim'] = dd3['claim'] + ' '
        elif mut == 'arbk':
            dd3['arb_kernel_sha256'] = dd3['arb_kernel_sha256'][:-1] + ('0' if dd3['arb_kernel_sha256'][-1] != '0' else '1')
        elif mut == 'arbb':
            dd3['arb_base_sha256'] = flip(dd3['arb_base_sha256'])
        elif mut == 'kind':
            dd3['items'][sorted(dd3['items'])[0]].pop('kind')
        what = mut or ('expected J_REF %d' % jref if jref != 300 else 'expected N %d' % nexp)
        try:
            RDR.check_text(json.dumps(dd3), jref, nexp)
            plant(lab, False, '(m3_reader_v4_4 must refuse the mutated b5 copy: %s)' % what)
        except ValueError:
            plant(lab, True, '(m3_reader_v4_4 refuses the mutated b5 copy: %s)' % what)
    # the bound load's checks, in memory: the consumers bind a record to the asm output that names it
    b5n, b5h = os.path.basename(paths['b5']), tsha(texts['b5'])
    try:
        RDR.loads(texts['b5'], 'RECORD %s %s\nVERDICT VALID\n' % (b5n, b5h), 300, NN, b5n)
        gate('C-BOUND-RT', True, '(m3_reader_v4_4.loads accepts the b5 text under an output that names it and ends VALID)')
    except ValueError as ex:
        gate('C-BOUND-RT', False, '(refused: %s)' % ex)
    for lab, otext in (('PLANT-BOUND-VERDICT', 'RECORD %s %s\nVERDICT VALID-PRECERT\n' % (b5n, b5h)),
                       ('PLANT-BOUND-INVALID', 'RECORD %s %s\nVERDICT INVALID (C-REP-B)\n' % (b5n, b5h)),
                       ('PLANT-BOUND-TWO', 'RECORD %s %s\nVERDICT VALID\nVERDICT VALID\n' % (b5n, b5h)),
                       ('PLANT-BOUND-SHA', 'RECORD %s %s\nVERDICT VALID\n' % (b5n, flip(b5h))),
                       ('PLANT-BOUND-NONE', 'VERDICT VALID\n')):
        try:
            RDR.loads(texts['b5'], otext, 300, NN, b5n)
            plant(lab, False, '(m3_reader_v4_4.loads must refuse this asm output)')
        except ValueError:
            plant(lab, True, '(m3_reader_v4_4.loads refuses this asm output)')
    gate('C-KBAR', Decimal(json.loads(texts['m2'])['kbar_exact']) == Decimal(KBAR), '(kbar_exact is the binary64 kbar exactly)')
    gate('C-PREC-ASM', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d before the write)' % flint.ctx.prec)
    opened = []

    def no_open(p, mode):
        opened.append(p)
        raise OSError('PLANT-NOWRITE: the writer opened %s' % p)
    refused = 0
    for fl, nf, tg in ((FAILS + ['PLANT-FORCED'], NOFIRE, tag), (FAILS, NOFIRE + ['PLANT-FORCED'], tag), (FAILS, NOFIRE, '_PRECERT')):
        try:
            if write_records(texts, paths, fl, nf, tg, opener=no_open) == []:
                refused += 1
        except OSError:
            pass
    plant('PLANT-NOWRITE', refused == 3 and not opened, '(write_records under a failed gate, an unfired plant and a PRECERT tag: %d of 3 refused, %d files opened)' % (
        refused, len(opened)))
    written = write_records(texts, paths, FAILS, NOFIRE, tag)
    if not written:
        out('RECORDS NOT WRITTEN (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE] + ([] if tag == '' else ['TAG %r' % (tag,)])))
    for f, path in written:
        gate('C-WRITE', sha(path) == tsha(texts[f]), '(%s holds exactly its C-FMT text)' % os.path.basename(path))
        out('RECORD %s %s' % (os.path.basename(path), sha(path)))


try:
    if FAM in ('D', 'mix', 'free2'):
        run_small(FAM)
    elif FAM in ('Nu', 'Nc'):
        run_prep_stage(FAM[1])
    elif FAM.startswith('Nk'):
        run_nk(int(FAM[2:]))
    else:
        run_asm()
    finish()
except SystemExit:
    raise
except BaseException:
    out('EXCEPTION in stage %s:' % STAGE[0])
    for ln in traceback.format_exc().rstrip().split('\n'):
        out('  ' + ln)
    out('VERDICT INVALID (EXCEPTION)')
    sys.exit(1)
