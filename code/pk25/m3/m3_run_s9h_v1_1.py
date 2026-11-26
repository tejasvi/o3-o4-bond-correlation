#!/usr/bin/env python3
"""m3_run_s9h_v1_1.py -- pk25 (code/pk25/m3/). REVISION of m3_run_s9h_v1.py (sha256 57d66456251737acb9b5265453f87e1bb9806fe2b1bb19516ad724a7939c7b25), one change of substance:
compute_entry is the parent's again. m3_run_s9h_v1 restricted the a_0-exact rule to products of the vacuum state, on the claim that
the parent's rule would reject Sh,1 and Sh,3; that was a misreading, since m3_entries_v3.TrialSet.cp encodes [cp, a, c] as a 'p'
factor only for a = 0 (a >= 1 gives an 'xi' factor), so the parent's rule already means vacuum products. Outputs, hand-offs and
records carry the name m3_run_s9h_v1_1; made by pk25/m3/make_m3_run_s9h_v1_1.py. m3_run_s9h_v1's docstring follows, with its name
and its a_0 line updated.
m3_run_s9h_v1_1.py -- pk25 (code/pk25/m3/). A FORK of pk03/m3_run_v1_10_4.py (sha256 7091a12185443623e8e1cbc56e42c0029508b84f8feac62fd72780ab77f997a6) for pk25's G5 entries
(S9(b)-h and S9(c)-h: G5_PLAN_v1 sect. 2.1 and 3, ADD1_1 sect. 6; the conditional approval, P0_LOG row 4126), made by
pk25/m3/make_m3_run_s9h_v1_1.py by exact replacements with asserted counts. C-CORE checks that every top-level def of the parent is
byte-identical here but CORE_CHANGED, and that the fork adds only CORE_NEW. What changes:
- the list: S9H_RUN_LIST_v1_1.json (sha256 df4212e17a659b03f061c88b6fd0603005a8122a8789f28df1a0867fd8a7b312: S9H_RUN_LIST_v1 without the withdrawn Gxxh,1,1 and Gxxh,3,3),
  pinned in INPUTS; C-LIST counts its 17 keys and its sets needed and control; FAMS NIH, NHT, DH; VG NIH, NHT -> VN, DH -> VD;
  RULE_OF std for Ih, IhTh, Sh and G,0,0 and col for Gxh and GxhR (the float twin's rules); PARITY_ZERO empty (C-PARITY-SET; the parity
  plants run on Ih,1 with [cp, 2, 0], the parent's IhZh); AKCPU empty; RULE_A the parent's default; no exemption file (EXF in pk25/m3,
  absent); no resume items;
- items: <X>a (smoke), <X>k1..<X>k30 (entry pieces) for X = NIH, NHT, DH, and asm. There are no prep items: the families read the
  parent's certified prep hand-offs VNu, VNc, VDu, VDc (pk03/hand, producer outputs in pk03/out, all pinned) through read_parent,
  which uses pk03's own hand-off module (HO_IN) and binds each header to the parent's sha256. C-PREP-SHARE: the smoke and every entry
  piece run C-PREP-GRAPH of the family graph against the graph the parent's prep ran on (parent_prep_graph: P2_RUN_LIST_v1_10's NTB for
  VN, DT for VD), with its plants; C-PREP-STAGES also checks that the parent's hand-offs name that family first;
- written paths: pk25/m3/out (outputs, records) and pk25/m3/hand (hand-offs, through the copy m3_handoff_v3_s9h.py, sha256 3c664ad2ea83f2b4824bdbdc70656ef69873c718f744ec6626d48e3671b7c453,
  pinned in OWNMOD and loaded from pk25/m3 through MODDIR); pk03's pinned files are read in place (OUTD_IN, HANDD_IN);
- float twins: pk25's m3ref_s9h_v1 outputs (families S9HNIH, S9HNHT, S9HDH), which also hold the withdrawn pair (C-REF-KEYS names it);
- a_0 exact: the parent's rule, unchanged since v1_1: an entry whose factor tuples are all 'p' takes a0_exact 1, and m3_entries_v3
  encodes [cp, a, c] as a 'p' factor only for a = 0, so the rule covers exactly the vacuum products (G,0,0 and Sh,0 here);
- controls (s9h_controls, in place of C-ZFLIP; in each smoke on the family's own keys and in asm on all keys): C-H0, C-IHT0, C-GXSYM,
  C-HX0 and C-G00-S9, with PLANT-ROW, PLANT-IHT0, PLANT-GXSYM, PLANT-HX0 and PLANT-G00-S9 (s9h_controls' docstring);
- asm: the three records m3_s9h_<G>_N<N>_J300_v1.json, with entry_list S9H_RUN_LIST_v1_1 and the prep's producer; the reader plants on
  the DH text (PLANT-PARZERO marks a free item zero); C-RESUME-INFO in place of C-RESUME-CHAIN.
The parent's prep-stage, resume and C-ZFLIP functions stay byte-identical and unreachable: ITEM_RE and the dispatch have no V or r items.
Docstrings inside unchanged defs still name the parent's twin (m3ref_v1_18_1) and families; here the twin is m3ref_s9h_v1.
Run (under the core-h guard): D=/mnt/g2/release/root/code/pk25; OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
  OMP_NUM_THREADS=1 TMPDIR=$D/tmp timeout 580 nice -n 10 prlimit --as=25769803776 -- python3 -I -B $D/m3/m3_run_s9h_v1_1.py
  ITEM LIM > $D/m3/out/m3_run_s9h_v1_1_ITEM.out 2> $D/m3/out/m3_run_s9h_v1_1_ITEM.err
The parent's docstring follows.
m3_run_v1_10_4.py -- pk03 (code/pk03/). REVISION of m3_run_v1_10_3.py (8344a43e) for the v1_10_4 approval (2026-11-08 14:58Z):
- the bar is m3_bar_v16_1: before each free entry's bound, declare_big fixes the big-rule set from each norm's own table (BIGRULE-SET;
  set once per norm); C-BIGCAP refuses a big-rule inflation over INFL_CAP and an exempt key whose e passes 1.1 x its declared e;
- the exemption (main c1' cc75cc3e) is BIGRULE_EXEMPT_v1_10_4_N<N>.json, read-only, its sha256 in every entry piece (C-EXEMPT;
  C-EXEMPT-SAME at asm); exempt factors stay in the bound and out of the per-part line;
- REP-B-INFO and asm's C-REP-B use the per-part line; the rule plants come from the bar; names m3_run_v1_10_4;
- for size, four docstrings point to m3_run_v1_10_2.py (2a70084f) by line.
The rest is v1_10_3's: its docstring l.2-7; v1_10_2's l.2-12; v1_10_1's l.2-22 (cb38907e); v1_10's l.2-44 (d8459b63).
Arguments: ITEM LIM (5..540). Output: stdout (out/m3_run_v1_10_4_<ITEM>.out); hand-offs in hand/; records in out/.
Run: D=/mnt/g2/release/root/code/pk03; OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=$D/tmp
  timeout 580 nice -n 10 prlimit --as=25769803776 -- python3 -I -B $D/m3_run_v1_10_4.py ITEM LIM
  > $D/out/m3_run_v1_10_4_ITEM.out 2> $D/out/m3_run_v1_10_4_ITEM.err
"""
import resource, sys, time, math, hashlib, signal, os, json, re, traceback

ITEM_RE = r'((NIH|NHT|DH)(a|k([1-9]|[12][0-9]|30))|asm)\.(4|3)'   # m3_run_s9h_v1_1: pk25's families; no prep or resume items
if len(sys.argv) != 3 or not re.fullmatch(ITEM_RE, sys.argv[1]):
    print('usage: m3_run_s9h_v1_1.py ITEM LIM   (ITEM = <X>a|<X>k1..<X>k30|asm . 4|3, X = NIH|NHT|DH; '
          'LIM = RLIMIT_CPU soft limit in s, 5..540)')
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
W18 = '/mnt/g2/release/root/code'
OWN = W18 + '/pk03'
C2B = W18 + '/pk02'
INP = W18 + '/pk10/scratch'
W4 = W18 + '/pk11/out'
MYD = W18 + '/pk25/m3'   # m3_run_s9h_v1_1: the folder of every written path
OUTD = MYD + '/out'   # m3_run_s9h_v1_1: outputs and records here; the float twins m3ref_s9h_v1 sit here too
OUTD_IN = OWN + '/out'   # m3_run_s9h_v1_1: pk03's pinned outputs, read in place (prep producers, V3N/V3D references, S9 records)
HANDD = MYD + '/hand'   # m3_run_s9h_v1_1: hand-offs here
HANDD_IN = OWN + '/hand'   # m3_run_s9h_v1_1: pk03's pinned prep hand-offs, read by HO_IN
MODDIR = {'m3_handoff_v3_s9h.py': MYD}   # m3_run_s9h_v1_1: the one module read from pk25/m3/
KERNEL = 'arbeng_ma_v1_4_1'   # m3_run_v1_9: the layer of every table, prep and entry here
ARBK = 'arbeng_ma_stub_v1_1'
ARBB = 'arbeng_c2b_v2'   # the arb base under ARBK (pinned in KFILES)
KFILES = {
    'arbeng_ma_v1_4_1.py': '1f58ad80ceb1c0992f08f894c0f6af26ef18d397627020a5a5fe7130818375d9',
    'arbeng_ma_stub_v1_1.py': '794fabc7111555db2f6390a144d3f5af6deeb358d02da8b5705cf3ceaefd0af1',
    'arbeng_c2b_v2.py': '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0',
}
VALREC = [   # m3_run_v1_9: arbeng_ma_v1_4_1's validation records and the two closes, in order
    (C2B, 'MANIFEST_ARBENG_MA_v1_4_1.sha256', 'c172e15f42cad0278bdea3343ddea084327dbf89a4eef2561df7e5d23140f5fc'),
    (C2B, 'MANIFEST_KT_MA_VAL_v1_6_RUN.sha256', '7ec00dc5d98d64c06e345d80b4a0959e7ec6805239a4d03ba7be006882186314'),
    (C2B + '/out', 'out_kt_ma_val_v1_6_1_d.out', 'af1e3f66a88c27b0593b31e23f936986ecd04c813854ed4001cc601f7a6bef12'),
    (W18 + '/rv01', 'REVIEW_CODE_ARBENG_MA_V1_4_rv01.md', '8afbb958904ab2067d75b6876b2b6496dda7286ba99d4d00428e3cd7a4485335'),
    (W18 + '/rv01', 'DELTA_ARBENG_MA_V1_4_1_rv01.md', '3fd1bfa7dc00d4600aa3ff1d413807cb75e9ab9d910600d580ab48bd6b36fc4f'),
]
VALIDATED = {('arbeng_ma_v1_4_1.py', '1f58ad80ceb1c0992f08f894c0f6af26ef18d397627020a5a5fe7130818375d9', tuple(v[2] for v in VALREC))}
DENY = {('arbeng_ma_v1_1.py', '81f7fb89f863343149b1558bfc3c8ba3e09b3e6c36ec00db4c12197b11158e7f'),
        ('arbeng_ma_v1_2.py', '935f2ca77dbcb7de0670d43505044f9c12c086f69de2a30f7b8133522ffcec80'),
        ('arbeng_ma_v1_4.py', '9870e7f8d5dc33f0edca029f9945de4774a1eb572114aa385dd7b75d7506e017'),   # m3_run_v1_9: the unpinned predecessor
        ('mock_arbeng_v1_4.py', '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e')}   # pk03's mock (tmp/r16)


def tag_for(kfile, ksha, vshas, validated=None):
    """'' (certified) only for a (file, full sha256, validation sha256s) in VALIDATED and never for a denied (file, sha256)."""
    if (kfile, ksha) in DENY:
        return '_PRECERT'
    return '' if (kfile, ksha, tuple(vshas)) in (VALIDATED if validated is None else validated) else (
        '_STUB' if 'stub' in kfile else '_PRECERT')


TAG = None   # set by C-VALIDATED after the imports
V18_SHA = 'be0c1be3eadabf2f14f40d84f7a2482f2b75aada522b0e267146008cd700da3b'   # m3_run_v1_8.py, the producer of N's prep hand-offs (C-PREP-SAME)
OWNMOD = {
    'm3_scal_v2.py': 'd22d3ad696074d4235f0fd31b026477e87f96f5d4b5331e29ab8d399e1e8f054',
    'm3_graph_v3.py': '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    'm3_series_v2.py': '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    'm3_major_v2.py': '89dd5a2184a511d4dea39fb3c558501e9738af118be9d41f2ac4b2d4b8d7b016',
    'm3_bar_v16_1.py': '475184d4d4545ff0448fed553782c969bbaf6bd13a542605d83be73dc8154f47',   # m3_run_v1_10_4: the declared big set, part lines
    'm3_entries_v3.py': '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    'm3_record_v4.py': '2c8a53efb5170d6c6e320bd814c824e69d2ccdd73c57cf87a9130b796109e30f',
    'm3_reader_v6_3.py': '539b613f6a9c07a9bef3d0cbb408c1d41de276a6a59aede8b03149204ce28661',
    'm3_handoff_v3.py': 'e4f5bf0b111197d87e9659c89265c68fcfe39e564860c6e6b6eb91c9c48feb21',
    'm3_handoff_v3_s9h.py': '3c664ad2ea83f2b4824bdbdc70656ef69873c718f744ec6626d48e3671b7c453',   # m3_run_s9h_v1_1: pk25's copy (HAND pk25/m3/hand); the parent's module above is HO_IN
    'm3_run_v1_8.py': V18_SHA,
}
INPUTS = {
    (OWN, 'P2_RUN_LIST_v1_10.json'): '31b96a5376c3f074858c91784ebe719bdf732a0461f427fe075503e8a555e522',   # m3_run_v1_10
    (W4, 'ts_N4_J170_D_S_z9sym_v1.json'): 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    (W4, 'ts_N3_S_z9sym_v1.json'): 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    (W4, 'vacres_K3_N4_sym_v1.json'): 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    (W4, 'vacres_K3_N3_sym_v1.json'): 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    (INP, 'm2_N4_J170.json.b'): '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    (INP, 'm2_N3_J170.json.b'): '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    (OUTD_IN, 'm3ref_v1_10_V3N.4.all_z9sym.out'): '65a8145b6f2ce35aa3692ab3f89447aa52c4420220408f3c028ee67bf7fdf0c2',
    (OUTD_IN, 'm3ref_v1_10_V3N.3.all_z9sym.out'): 'd12836039cc0390feed5435486459530a781cc75865f1ecf8b95f497a0421945',
    (OUTD_IN, 'm3ref_v1_10_V3D.4.0-32_z9sym.out'): '7540647500f6c4368ad47967308b872224e08cbcaa645a1cf20acb469d9c5307',
    (OUTD_IN, 'm3ref_v1_10_V3D.3.all_z9sym.out'): '8a045f0bb2579e91f5a937761bacf0b54af6632b6e2a5b5307d3a652af74bc9a',
    (HANDD_IN, 'm3_run_v1_8_Nu.4.json'): 'c52047a361b4b82160d7fc2c2b52e198500db0c61040cf77bb1a3b8863219c6a',
    (HANDD_IN, 'm3_run_v1_8_Nc.4.json'): 'a6fcc9d0436955b3573cb5150e65fd78686e9f65e9a5a1ea813a45d6ac8fd665',
    (HANDD_IN, 'm3_run_v1_8_Nu.3.json'): 'b3b8801e4709fa8a5e56d232c2543838b276ba94c19d3c64b8b75b154d3afb23',
    (HANDD_IN, 'm3_run_v1_8_Nc.3.json'): '26f8b56a0786d0012622ca15b7079f6a381106b6ba1f52a68cb1171ec6fabbf1',
    (OWN + '/tmp/r16', 'mock_arbeng_v1_4.py'): '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e',   # PLANT-MOCK's file
    (MYD, 'S9H_RUN_LIST_v1_1.json'): 'df4212e17a659b03f061c88b6fd0603005a8122a8789f28df1a0867fd8a7b312',   # m3_run_s9h_v1_1: the certified list (C-LIST)
    (OWN, 'm3_run_v1_10_4.py'): '7091a12185443623e8e1cbc56e42c0029508b84f8feac62fd72780ab77f997a6',   # m3_run_s9h_v1_1: the parent (PARENT_SHA, the prep producer; C-CORE's source)
    (HANDD_IN, 'm3_run_v1_10_4_VNu.4.json'): '03367cad8d3e15328d5d2c7b6d6e8c8866069c8a161eb058319ab581e3bce90f',   # m3_run_s9h_v1_1: the parent's prep hand-off
    (OUTD_IN, 'm3_run_v1_10_4_VNu.4.out'): '6ab147b390b0badc41086bf53ec85603a5a093034050837c108b47d02c1096ba',   # m3_run_s9h_v1_1: its producer output
    (HANDD_IN, 'm3_run_v1_10_4_VNu.3.json'): '37119d972e6002ae60bbd0816a530fc2bfa2801b79bc36a7150f27948d5da414',   # m3_run_s9h_v1_1: the parent's prep hand-off
    (OUTD_IN, 'm3_run_v1_10_4_VNu.3.out'): 'ddf96f508eda111b6093ebb2bcc07a3d1f6062642ac60f5d4e3e3dd04f8406e2',   # m3_run_s9h_v1_1: its producer output
    (HANDD_IN, 'm3_run_v1_10_4_VNc.4.json'): 'f8444f98ef8c7358c1777cd436054b9d6b545e7a2761f0cc7b9fe6f47dd3b76b',   # m3_run_s9h_v1_1: the parent's prep hand-off
    (OUTD_IN, 'm3_run_v1_10_4_VNc.4.out'): 'b879ba8c45d37bd0f480f563f63d3260a9aeb56fc43230604b497b901343bccd',   # m3_run_s9h_v1_1: its producer output
    (HANDD_IN, 'm3_run_v1_10_4_VNc.3.json'): '7da8958c992b1ba5f90d58e1186207f2df2679692c77b61151e1619d4aaf633d',   # m3_run_s9h_v1_1: the parent's prep hand-off
    (OUTD_IN, 'm3_run_v1_10_4_VNc.3.out'): '30769533ef806d511efe73feeeb27bc0fbfadcc45b826af708c06f4f83e2186d',   # m3_run_s9h_v1_1: its producer output
    (HANDD_IN, 'm3_run_v1_10_4_VDu.4.json'): '172278ee3766566f39e2150b6cae9046d566f51c0c02954cb3bf653d1f4ea95a',   # m3_run_s9h_v1_1: the parent's prep hand-off
    (OUTD_IN, 'm3_run_v1_10_4_VDu.4.out'): '8bfb9875aa4907a447d81171e1a07bf97fa10e26b5891e50048c8d1bd69f0714',   # m3_run_s9h_v1_1: its producer output
    (HANDD_IN, 'm3_run_v1_10_4_VDu.3.json'): '2e2c1307742738ef44ba250775d6ca01d7924d3280927c1b882f69f123644e6c',   # m3_run_s9h_v1_1: the parent's prep hand-off
    (OUTD_IN, 'm3_run_v1_10_4_VDu.3.out'): 'd35f68223066136f824eaa941c4a2a163396ee90abe4106cd6b984d847d75eda',   # m3_run_s9h_v1_1: its producer output
    (HANDD_IN, 'm3_run_v1_10_4_VDc.4.json'): '1c9e53cd05849c02ea0957e942ac91b1b089e506e6cfbaaeb87dfbabd8992d41',   # m3_run_s9h_v1_1: the parent's prep hand-off
    (OUTD_IN, 'm3_run_v1_10_4_VDc.4.out'): 'b338b56d0ff087eb6114fdfab1428a184ac47989bf2026cc32e45b408f40bc3a',   # m3_run_s9h_v1_1: its producer output
    (HANDD_IN, 'm3_run_v1_10_4_VDc.3.json'): 'f957914ba70f8357085077e1a8e22ddb8f7287e88a35cb1212e95c902715dec6',   # m3_run_s9h_v1_1: the parent's prep hand-off
    (OUTD_IN, 'm3_run_v1_10_4_VDc.3.out'): '2b7269c6893e7ba96b9cbb68ee49a89a6f2635dd83c1abc9eef6257e8d2d92b6',   # m3_run_s9h_v1_1: its producer output
    (OUTD_IN, 'm3_s9_N4_J300_v1_8_3.json'): 'bcc6434c6a03eecb232f10504b63f1ce10a94a489d5a2ba9cf3fe09c8018b831',   # m3_run_s9h_v1_1: C-G00-S9 and PLANT-ROW
    (OUTD_IN, 'm3_run_v1_8_3_asm9.4.out'): 'a41763a35f405668c748cdd1aaccfff681aacf5fb096342a791659ccb49c07a7',   # m3_run_s9h_v1_1: C-G00-S9 and PLANT-ROW
    (OUTD_IN, 'm3_s9_N3_J300_v1_8_3.json'): 'd287d3dcbd4bd988aa8061fbe11b3da1609e0ab4d27ae1a619eadcee963e8fa5',   # m3_run_s9h_v1_1: C-G00-S9 and PLANT-ROW
    (OUTD_IN, 'm3_run_v1_8_3_asm9.3.out'): 'e7f09f7381919a8aef322adfae9ada7506bda4db527faba01b8deacdf6542655',   # m3_run_s9h_v1_1: C-G00-S9 and PLANT-ROW
}
TWINS = {   # m3_run_s9h_v1_1: pk25's float twins m3ref_s9h_v1 (TRIAL z9sym; S9H_RUN_LIST_v1, the withdrawn pair included) per (family, N): (file, sha256)
    ('NIH', 4): [('m3ref_s9h_v1_S9HNIH.4.all_z9sym.out', '49d25ccaa3bd0dfe05ee361c8c25aed024ce0afb799fafab150f8a02778783f5')],
    ('NIH', 3): [('m3ref_s9h_v1_S9HNIH.3.all_z9sym.out', 'dd938663c3ccd67b3d9cd4ed1521e1324f5ae79e4f043ed6f14d84a5b8b5886d')],
    ('NHT', 4): [('m3ref_s9h_v1_S9HNHT.4.all_z9sym.out', '007de48c518917290ede4ba7e56e736ba41c64d14abecf3bb09d4678afb169a7')],
    ('NHT', 3): [('m3ref_s9h_v1_S9HNHT.3.all_z9sym.out', '8bf09a45c5dc7db7dfc144f7be1ee513c22ba3ad356a2ad51846be6024fd1839')],
    ('DH', 4): [('m3ref_s9h_v1_S9HDH.4.all_z9sym.out', '87d2dac6d8dd9b3b1b5fa62d1c13009ca4b13fe8c72386d0a8bf9ee45b6dd9c3')],
    ('DH', 3): [('m3ref_s9h_v1_S9HDH.3.all_z9sym.out', 'b20820458bccdc252175fea702288cf128bc19c3d46b76bdca2276db58702fee')],
}
for _k, _v in TWINS.items():
    for _f, _h in _v:
        INPUTS[(OUTD, _f)] = _h

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


SELF_SHA = sha(os.path.abspath(__file__))
out('m3_run_s9h_v1_1 item %s LIM %d; script sha256 %s; python %s' % (ITEM, LIM, SELF_SHA, sys.version.split()[0]))
stage('C-HASH')
bad = [f for f, h in OWNMOD.items() if sha(os.path.join(MODDIR.get(f, OWN), f)) != h]   # m3_run_s9h_v1_1: MODDIR
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
import importlib.util
GENERIC = [('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_major', 'm3_major_v2.py'),
           ('m3_bar', 'm3_bar_v16_1.py'), ('m3_entries', 'm3_entries_v3.py'), ('m3_record', 'm3_record_v4.py'), ('m3_reader', 'm3_reader_v6_3.py'),
           ('m3_handoff', 'm3_handoff_v3_s9h.py')]   # m3_run_s9h_v1_1: pk25's copy


def load_as(name, fname):
    """a pinned file of pk03/ loaded under its generic module name (dependencies first)."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(MODDIR.get(fname, OWN), fname))   # m3_run_s9h_v1_1: MODDIR
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


MODS = {name: load_as(name, fname) for name, fname in GENERIC}
S, GR, SER, BAR, ENT, REC, RDR, HO = (MODS[k] for k in ('m3_scal', 'm3_graph', 'm3_series', 'm3_bar', 'm3_entries', 'm3_record', 'm3_reader',
                                                         'm3_handoff'))
sys.path.append(C2B)
import arbeng_ma_v1_4_1 as K
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
HO_IN = load_as('m3_handoff_in', 'm3_handoff_v3.py')   # m3_run_s9h_v1_1: pk03's own hand-off module (HAND pk03/hand), reads only
assert HO.HAND == HANDD and HO_IN.HAND == HANDD_IN and os.path.abspath(HO_IN.__file__) == os.path.join(OWN, 'm3_handoff_v3.py'), (
    HO.HAND, HO_IN.HAND)   # m3_run_s9h_v1_1: this fork's hand-offs in pk25/m3/hand; the parent's are read from pk03/hand
import flint
from mpmath import iv
badw = [n for n, m in MODS.items() if os.path.abspath(m.__file__) != os.path.join(MODDIR.get(dict(GENERIC)[n], OWN), dict(GENERIC)[n])]   # m3_run_s9h_v1_1
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
# m3_run_v1_9: C-VALREC-RUN, PLANT-MOCK, C-CALLER and PLANT-CALLER
RUNMAN = [v for v in VALREC if v[1] == 'MANIFEST_KT_MA_VAL_v1_6_RUN.sha256'][0]
rbad, nrun, nvo = [], 0, 0
with open(os.path.join(RUNMAN[0], RUNMAN[1])) as fh:
    for ln in fh:
        h_, p_ = ln.split()
        nrun += 1
        if not os.path.exists(p_) or sha(p_) != h_:
            rbad.append('%s missing or changed' % os.path.basename(p_))
        elif os.path.basename(p_).startswith('out_kt_ma_val') and p_.endswith('.out'):
            nvo += 1
            with open(p_) as fo:
                vl = [x.rstrip('\n') for x in fo if x.startswith('VERDICT')]
            if vl != ['VERDICT VALID']:
                rbad.append('%s: VERDICT lines %r' % (os.path.basename(p_), vl))
gate('C-VALREC-RUN', not rbad and nrun > 0 and nvo > 0, '(%s: %d files re-hashed against it, %d validation outputs with exactly ["VERDICT '
     'VALID"])%s' % (RUNMAN[1], nrun, nvo, (': ' + '; '.join(rbad)) if rbad else ''))
MOCK = os.path.join(OWN, 'tmp', 'r16', 'mock_arbeng_v1_4.py')
msha = sha(MOCK)
plant('PLANT-MOCK', tag_for(KERNEL + '.py', msha, [v[2] for v in VALREC]) != '' and tag_for('mock_arbeng_v1_4.py', msha, [v[2] for v in VALREC]) != '',
      '(pk03\'s mock tmp/r16/mock_arbeng_v1_4.py, sha256 %s, offered as %s.py and under its own name, must be refused the certified '
      'tag)' % (msha[:8], KERNEL))
NFB = ('E2_ma', 'lp_moment_ma', 'lp_ma', 'pos_ma', 'E2_ball', 'e2')   # m3_run_v1_10_3: the bar's defs whose layer calls pass fallback=False


def caller_scan(text):
    """C-CALLER's scan of a source text, comments aside: the offending call lines (E2_combine without plan= or fallback=False, load_view
    without a second argument, MomTableU without block=; m3_run_v1_10_3: a layer call .tab.E( or .tab.E2( in a def named in NFB without
    fallback=False) and the count of those layer calls."""
    bad, fn, nfb = [], '', 0
    for i, ln in enumerate(text.split('\n')):
        code = ln.split('#')[0]
        m = re.match(r'\s*def (\w+)\(', code)
        fn = m.group(1) if m else fn
        if re.search(r'\.E2_combine\(', code) and not ('plan=' in code and 'fallback=False' in code):
            bad.append('l.%d E2_combine' % (i + 1))
        if re.search(r'\.load_view\(', code) and not re.search(r'\.load_view\([^,()]+,\s*[^)\s]', code):
            bad.append('l.%d load_view' % (i + 1))
        if re.search(r'\.MomTableU\(', code) and 'block=' not in code:
            bad.append('l.%d MomTableU' % (i + 1))
        if fn in NFB and re.search(r'\.tab\.E2?\(', code):
            nfb += 1
            if 'fallback=False' not in code:
                bad.append('l.%d %s' % (i + 1, fn))
    return bad, nfb


with open(os.path.join(OWN, 'm3_bar_v16_1.py')) as fh:
    BARSRC = fh.read()
ncall = len(re.findall(r'\.E2_combine\(|\.load_view\(|\.MomTableU\(', '\n'.join(ln.split('#')[0] for ln in BARSRC.split('\n'))))
cbad, nfb = caller_scan(BARSRC)
gate('C-CALLER', ncall >= 3 and nfb == 6 and not cbad, '(m3_bar_v16_1: %d kernel calls; every E2_combine passes plan= and fallback=False, every '
     'load_view an expected sha256, every MomTableU block=; %d layer calls in %s, each with fallback=False, 6 wanted)%s' % (
         ncall, nfb, '/'.join(NFB), (': ' + ', '.join(cbad)) if cbad else ''))
cmut = BARSRC.replace('E2_combine(parts, plan=plan, fallback=False)', 'E2_combine(parts, fallback=False)', 1)
plant('PLANT-CALLER', cmut != BARSRC and bool(caller_scan(cmut)[0]), '(m3_bar_v16_1 with one E2_combine call\'s plan= removed)')
fmut = BARSRC.replace('return self.tab.E(P.power(p), fallback=False)', 'return self.tab.E(P.power(p))', 1)
plant('PLANT-CALLER-FLAG', fmut != BARSRC and bool(caller_scan(fmut)[0]), '(m3_bar_v16_1 with pos_ma\'s fallback=False dropped)')
SER_RE = re.compile(r'[A-Za-z0-9]' + '_series' + r'\s*\(')
ser_hits = []
for p_ in [os.path.join(MODDIR.get(f, OWN), f) for f in OWNMOD] + [os.path.join(C2B, f) for f in KFILES] + [os.path.abspath(__file__)]:
    with open(p_) as fh:
        ser_hits += ['%s:%d' % (os.path.basename(p_), i + 1) for i, ln in enumerate(fh) if SER_RE.search(ln)]
gate('C-SERIES', not ser_hits, '(no *_series( call in %d modules, the kernel files and this script)%s' % (len(OWNMOD), (': ' + ', '.join(ser_hits)) if ser_hits else ''))
plant('PLANT-SERIES', bool(SER_RE.search('x = acb' + '_series(1)')), '(a planted *_series( call must be flagged)')
# m3_run_s9h_v1_1, C-CORE (G5_PLAN_v1 sect. 3): every top-level def of the parent m3_run_v1_10_4.py (pinned in INPUTS) is byte-identical
# here (ast source segments) but CORE_CHANGED, changed on purpose (the docstring lists why); CORE_NEW are the fork's own defs.
# PLANT-CORE: a copy of this script with one operator changed inside meets must fail the comparison.
import ast
CORE_CHANGED = ('list_check', 'parity_set', 'load_as', 'ref_prep_vg', 'header', 'write_handoff', 'read_handoff', 'prep_scalars', 'piece_state', 'run_smoke', 'run_nk', 'rep_checks', 'reader_plants', 'run_asm')
CORE_NEW = ('core_defs', 'core_diff', 'read_parent', 'parent_prep_graph', 's9h_controls')


def core_defs(text):
    """the top-level function defs of a source text: name -> its exact source segment (ast.get_source_segment)."""
    tree = ast.parse(text)
    return {n.name: ast.get_source_segment(text, n) for n in tree.body if isinstance(n, ast.FunctionDef)}


def core_diff(ptext, stext):
    """(identical, changed, dropped, added): the sorted top-level def names of stext against those of ptext."""
    pd, sd = core_defs(ptext), core_defs(stext)
    return (sorted(k for k in pd if k in sd and pd[k] == sd[k]), sorted(k for k in pd if k in sd and pd[k] != sd[k]),
            sorted(k for k in pd if k not in sd), sorted(k for k in sd if k not in pd))


with open(os.path.join(OWN, 'm3_run_v1_10_4.py')) as fh:
    PARENT_TEXT = fh.read()
with open(os.path.abspath(__file__)) as fh:
    SELF_TEXT = fh.read()
_cs, _cc, _cd, _ca = core_diff(PARENT_TEXT, SELF_TEXT)
gate('C-CORE', bool(_cs) and _cc == sorted(CORE_CHANGED) and not _cd and _ca == sorted(CORE_NEW), '(the parent m3_run_v1_10_4.py, sha256 %s: '
     '%d top-level defs byte-identical here; changed on purpose %s; added %s; dropped %s)' % (
         INPUTS[(OWN, 'm3_run_v1_10_4.py')][:8], len(_cs), _cc, _ca, _cd))
_mut = SELF_TEXT.replace('return x.a <= y.b ' + 'and y.a <= x.b', 'return x.a <= y.b ' + 'or y.a <= x.b', 1)
_mc = core_diff(PARENT_TEXT, _mut)[1]
plant('PLANT-CORE', _mut != SELF_TEXT and _mc != sorted(CORE_CHANGED), '(a copy of this script with "and" changed to "or" in meets: changed '
      'defs %s)' % _mc)
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


with open(os.path.join(MYD, 'S9H_RUN_LIST_v1_1.json')) as fh:   # m3_run_s9h_v1_1: pk25's certified list (pinned in INPUTS)
    LIST = json.load(fh)
with open(os.path.join(OWN, 'P2_RUN_LIST_v1_10.json')) as fh:   # m3_run_s9h_v1_1: the parent's list, for the graphs its prep stages ran on
    LISTP2 = json.load(fh)
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]
TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)
TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)])}
FAMS = ('NIH', 'NHT', 'DH')   # m3_run_s9h_v1_1: S9H_RUN_LIST_v1_1's graphs, each one family
VG = {'NIH': 'VN', 'NHT': 'VN', 'DH': 'VD'}   # the vertex graph whose prep serves a family (m3_run_s9h_v1_1: the parent's VN and VD preps)
VGP2 = {'VN': 'NTB', 'VD': 'DT'}   # m3_run_s9h_v1_1: the parent's first family served by each vertex graph, whose graph its prep stages ran on
EDGES = {g: 'N' for g in FAMS}   # only for m3_entries_v3.factor's column lookup: every factor here names its column by index or triple
PARITY_ZERO = set()   # m3_run_s9h_v1_1: S9H_RUN_LIST_v1_1 has no parity zero (C-PARITY-SET checks that no entry passes C-ODD)
V3 = [{'id': '%s:%s' % (e['graph'], e['key']), 'key': e['key'], 'graph': e['graph'], 'factors': e['factors'],
       'parity': 'zero' if (e.get('parity_zero') or e['key'] in PARITY_ZERO) else 'free'}
      for e in LIST['entries'] if e['graph'] in FAMS]
FAMREF = {g: 'S9H' + g for g in FAMS}   # m3_run_s9h_v1_1: the float twins' families (m3ref_s9h_v1)
REFOUT = {g: [f for f, h in TWINS[(g, NN)]] for g in FAMS}
REFVG = {'VN': {4: 'm3ref_v1_10_V3N.4.all_z9sym.out', 3: 'm3ref_v1_10_V3N.3.all_z9sym.out'},
         'VD': {4: 'm3ref_v1_10_V3D.4.0-32_z9sym.out', 3: 'm3ref_v1_10_V3D.3.all_z9sym.out'}}   # the prep's radii, rho'^2 and theta0
VGFAM = {'VN': 'V3N', 'VD': 'V3D'}
RULE = (80.0, 0.6, 0.7)   # the float references' radii sqrt(min(80 G_vv/J, 0.6)) and rho' (m3ref_v1_10's default for V3N and V3D)
PFX = {g: g for g in FAMS}   # item prefixes of the families' pieces
MAXP = {g: 30 for g in FAMS}   # entry pieces (m3_run_v1_10_3: 30)
RULE_A = {g: (10 ** 6, 1.2e-4, 450.0) for g in FAMS}   # m3_run_v1_10_3: bigtab, arb s per moment, arb_max s (m3_run_s9h_v1_1: the default)
INFL_CAP = 0.10   # m3_run_v1_10_4: the per-norm inflation cap (main 051e1a64 (c))
EXF = os.path.join(MYD, 'BIGRULE_EXEMPT_s9h_v1_N%d.json' % NN)   # m3_run_s9h_v1_1: absent (no key exempt; an exemption would need the word)
EXEMPT, EXSHA, EXSEEN = {}, None, set()
if os.path.exists(EXF):
    EXSHA = sha(EXF)
    with open(EXF) as fh:
        _x = json.load(fh)
    EXEMPT = {k: float(v) for k, v in _x['keys'].items()}
    gate('C-EXEMPT', _x.get('N') == NN and not os.stat(EXF).st_mode & 0o222 and all(k.count(':') == 2 and v > 0 for k, v in EXEMPT.items()),
         '(%s, sha256 %s, read-only, N %r: %s)' % (os.path.basename(EXF), EXSHA, _x.get('N'), sorted(EXEMPT.items())))
else:
    out('C-EXEMPT-INFO (%s absent: no key is exempt at N%d)' % (os.path.basename(EXF), NN))
RESUME_FAMS = ()   # m3_run_s9h_v1_1: no resume items (the parent's NTBr1 and NTBr2 checked the checkpoint code, which C-CORE pins)
RESUME_KEY = {}
WITHDRAWN = ('Gxxh,1,1', 'Gxxh,3,3')   # m3_run_s9h_v1_1: S9H_RUN_LIST_v1's entries left out of v1_1 (ADD1_1 sect. 6); the twins still hold them
PARENT_SHA = INPUTS[(OWN, 'm3_run_v1_10_4.py')]   # m3_run_s9h_v1_1: the producer of the prep hand-offs that read_parent reads
XH_NAMED = {('T', 0, 1): (0, 3, 1), ('M', 0, 2): (1, 4, 2), ('T', 1, 7): (3, 6, 7), ('M', 1, 8): (4, 7, 8), ('B', 1, 7): (5, 8, 7)}   # the list's xh note
CLAIM_BALL = ('for every J >= J_REF, t = 1/J, t = 0 included: I(J)/main(J) lies in sum_k [ak_k - ak_rad_k, ak_k + ak_rad_k] t^k + '
              '[-sum Bp, sum Bp] (Lemma U: PLAN_M3_CODE_v1 l.125, v1_2 U4)')   # 


def name_of(e):
    return e['key']


def qcap_of(pr, p):
    """R1: (qcap, qmax), qcap = max(6, qmax), qmax the largest pair degree of the entry's F_i, the truncated product of its partition's
    groups' series (the same for any partition), from the group cache bound reads."""
    gds = [pr.gdata(gf) for gf in p['groups']]
    if not gds:
        return 6, 0
    Fi = pr.series_product([d['ser'] for d in gds], p['scal'], 3)
    qmax = max(BAR.qdeg(P, pr.g.V) for P in Fi)
    return max(6, qmax), qmax


def entries_of(graph, names=None):
    out_ = [e for e in V3 if e['graph'] == graph and (names is None or name_of(e) in names)]
    if names is not None:
        assert sorted(name_of(e) for e in out_) == sorted(names), (names, [name_of(e) for e in out_])
    return out_


def enc_of(enc, rows='TMB'):
    """a list factor encoding as m3_entries_v3 reads it: [xh, R, gap, w] becomes [xia, [u, v, w]] with (u, v) = (3 gap + r, 3 (gap + 1) + r),
    r the row's index in rows (T 0, M 1, B 2); every other encoding is unchanged."""
    if enc[0] == 'xh':
        r, gap, w = rows.index(enc[1]), int(enc[2]), int(enc[3])
        return ['xia', [3 * gap + r, 3 * (gap + 1) + r, w]]
    return list(enc)


def facs_of(e, ts=None):
    """an entry's riglap factor tuples (m3_entries_v3.factor of enc_of of each encoding)."""
    return [ENT.factor(TS if ts is None else ts, EDGES[e['graph']], enc_of(enc)) for enc in e['factors']]


def list_check():
    """C-LIST (m3_run_s9h_v1_1: S9H_RUN_LIST_v1_1): the list holds 17 entries with distinct keys, each with K 3 on one of the three
    graphs, none of them withdrawn, and its sets needed and control cover exactly those keys; PLANT-LIST: the keys without the first must
    not cover the sets."""
    keys = [e['key'] for e in LIST['entries']]
    sets = sorted(k for s_ in ('needed', 'control') for k in LIST['sets'][s_])
    ok = (len(keys) == 17 and len(set(keys)) == 17 and all(e['K'] == 3 and e['graph'] in FAMS for e in LIST['entries'])
          and sets == sorted(keys) and sorted(LIST['graphs']) == sorted(FAMS) and not set(keys) & set(WITHDRAWN))
    gate('C-LIST', ok, '(S9H_RUN_LIST_v1_1: %d entries, %d distinct keys, K %s, graphs %s; sets needed %d, control %d; withdrawn %s absent: '
         '%s)' % (len(keys), len(set(keys)), sorted(set(e['K'] for e in LIST['entries'])), sorted(LIST['graphs']), len(LIST['sets']['needed']),
                  len(LIST['sets']['control']), list(WITHDRAWN), not set(keys) & set(WITHDRAWN)))
    plant('PLANT-LIST', sets != sorted(keys[1:]), '(the keys without %s must not cover the sets)' % keys[0])


def xh_check():
    """C-XH: enc_of gives the list's five named triples, [xh, T, 1, 7] becomes ('xi', (3, 6, 7), 0.0, e_1), and every xh bond (u, v) is
    among its graph's pairs; PLANT-XH: with T and B swapped the named triples must be missed."""
    got = {k: tuple(enc_of(['xh'] + list(k))[1]) for k in XH_NAMED}
    fac = ENT.factor(TS, 'N', enc_of(['xh', 'T', 1, 7]))
    bonds = []
    for e in V3:
        prs = [sorted(p) for p in LIST['graphs'][e['graph']]['pairs']]
        for enc in e['factors']:
            if enc[0] == 'xh':
                u, v, w = enc_of(enc)[1]
                bonds.append(sorted((u, v)) in prs)
    ok = got == XH_NAMED and fac == ('xi', (3, 6, 7), 0.0, [1.0] + [0.0] * 8) and bool(bonds) and all(bonds)
    gate('C-XH', ok, '(the named triples %s; [xh, T, 1, 7] gives %r; %d xh factors, each bond among its graph\'s pairs: %s)' % (
        sorted(got.items()), fac, len(bonds), all(bonds)))
    swp = {k: tuple(enc_of(['xh'] + list(k), rows='BMT')[1]) for k in XH_NAMED}
    plant('PLANT-XH', swp != XH_NAMED, '(T and B swapped must miss the named triples)')


def family_graph(graph):
    """the family's GraphIV (m3_graph_v3.strip of the list's columns, the list's pairs). C-GRAPH-LIST: V = 3 x columns, F = V + pairs =
    the list's F, pairs distinct, every pair form the entries use among them (PLANT-GRAPH-LIST: without the first one used)."""
    spec = LIST['graphs'][graph]
    V, E = GR.strip(spec['columns'])
    want = sorted(tuple(sorted(p)) for p in spec['pairs'])
    used = set()
    for e in V3:
        if e['graph'] == graph:
            for f in facs_of(e):
                used |= {tuple(sorted(p)) for p in ENT.pairs_of(f)}
    g = GR.GraphIV(V, E, want, NN)
    ok = V == 3 * len(spec['columns']) and g.F == spec['F'] and g.F == V + len(want) and len(set(want)) == len(want) and bool(used) and used <= set(want)
    gate('C-GRAPH-LIST', ok, '(%s: the columns %s give V %d and %d edges; the list\'s %d pairs %s, F %d (the list: %d); the entries use %d of them%s)' % (
        graph, spec['columns'], V, len(E), len(want), want, g.F, spec['F'], len(used & set(want)),
        '' if used <= set(want) else ('; NOT in the list: %s' % sorted(used - set(want)))))
    first = sorted(used)[0] if used else None
    plant('PLANT-GRAPH-LIST', first is not None and not (used <= set(want) - {first}), '(%s: the list\'s pairs without %r, a pair an entry uses)' % (graph, first))
    return g


def ref_files(graph):
    return [os.path.join(OUTD, fn) for fn in REFOUT[graph]]


def ref_prep(graph):
    """the family's float twin's PREPJSON (its first piece)."""
    return read_lines(ref_files(graph)[0], 'PREPJSON')[0]


def twin_keys(graph):
    """R1: the family's float twin's KEYJSON lines over all its pieces, by key (each with its rule, G, partition and qcap)."""
    return {d['key']: d for p in ref_files(graph) for d in read_lines(p, 'KEYJSON')}


def ref_prep_vg(vg):
    """the vertex graph's reference PREPJSON, m3ref_v1_10's V3N or V3D record at this N: the prep's radii, rho'^2 and theta0."""
    return read_lines(os.path.join(OUTD_IN, REFVG[vg][NN]), 'PREPJSON')[0]   # m3_run_s9h_v1_1: pk03's V3N and V3D records


def make_prep(vg, g, stages, scalars=None):
    """C-RULE (PLANT-RULE) on g's certified G_vv against the vertex graph's reference radii, m3_bar_v12's Prep (v10's, dmaxH 18) on g with
    the given stages or the restored scalars, C-TILT and C-PREP-REF."""
    rp = ref_prep_vg(vg)
    mid = [(S.up(gv) + S.down(gv)) / 2 for gv in g.Gvv]
    want = [min(RULE[0] * m / 300, RULE[1]) for m in mid]
    drule = max([abs(a - w) / w for a, w in zip(rp['a_v'], want)] + [abs(rp['ap'] - RULE[2] ** 2) / RULE[2] ** 2])
    gate('C-RULE', len(want) == len(rp['a_v']) and drule <= 1e-12, '(%s: the reference radii^2 = min(%g G_vv/300, %g) and rho\'^2 = %g^2, '
         'G_vv the certified mids: max relative difference %.1e (tol 1e-12))' % (vg, RULE[0], RULE[1], RULE[2], drule))
    bad = [min(1.01 * RULE[0] * m / 300, 1.01 * RULE[1]) for m in mid]
    plant('PLANT-RULE', not (max(abs(a - w) / w for a, w in zip(rp['a_v'], bad)) <= 1e-12), '(%s: 80 and 0.6 times 1.01)' % vg)
    pr = BAR.Prep(K, g, 300, rp['a_v'], rp['ap'], rp['theta0'], 6, log=out, dmaxH=18, stages=stages, scalars=scalars)
    encl = [-iv.log(1 - S.I(a)) / (2 * S.I(a)) * (1 / S.I(300)) for a in rp['a_v']]
    gate('C-TILT', pr.ok and all(S.I(r) >= x.b for r, x in zip(pr.rates, encl)),
         '(a) %d tilt rates rounded up from their mp.iv enclosures; (b) both tilts certainly positive definite (lowest pivots %s, %s)' % (
             len(pr.rates), None if not pr.tilt_c else S.down(pr.tilt_c['low']), None if not pr.tilt_p else S.down(pr.tilt_p['low'])))
    gate('C-PREP-REF', rp['family'] == VGFAM[vg] and rp['N'] == NN and rp['J'] == 300, '(%s: %s PREPJSON of family %s, N %r, J %r)' % (
        vg, REFVG[vg][NN], rp['family'], rp['N'], rp['J']))
    return pr, rp


def prep_twin(graph):
    """C-PREP-TWIN: the family's float twin (m3ref_v1_18_1, its family, N and J) has the prep reference's radii, rho'^2 and theta0 to
    1e-12 relative; PLANT-PREP-TWIN: the reference's rho'^2 times 1 + 1e-9 must exceed that tolerance."""
    rp, tw = ref_prep_vg(VG[graph]), ref_prep(graph)
    flat = lambda d: [d['ap'], d['theta0']] + list(d['a_v'])
    rel = lambda x, y: max(abs(p - q) / abs(q) for p, q in zip(x, y)) if len(x) == len(y) else math.inf
    a, b = flat(rp), flat(tw)
    d = rel(a, b)
    gate('C-PREP-TWIN', tw['family'] == FAMREF[graph] and tw['N'] == NN and tw['J'] == 300 and d <= 1e-12, '(%s: %s of family %s, N %r, '
         'J %r: radii, rho\'^2 and theta0 against %s, largest relative difference %.1e (tol 1e-12))' % (
             graph, REFOUT[graph][0], tw['family'], tw['N'], tw['J'], REFVG[VG[graph]][NN], d))
    plant('PLANT-PREP-TWIN', not (rel([a[0] * (1 + 1e-9)] + a[1:], b) <= 1e-12), '(%s: the reference\'s rho\'^2 times 1 + 1e-9)' % graph)


def is_column(f):
    T, M, B = f[1]
    return M == T + 1 and B == T + 2 and T % 3 == 0


def parity_h(f):
    """m3_entries_v3.parity_class on a column triple; a 'xi' factor on any other triple (the list's xh) is 'even' when every pair form it
    uses is fixed by T <-> B as an unordered pair (it is c0 plus a polynomial in those forms alone); else None."""
    if is_column(f):
        return ENT.parity_class(f)
    if f[0] == 'xi' and all({ENT.sigma(u), ENT.sigma(v)} == {u, v} for u, v in ENT.pairs_of(f)):
        return 'even'
    return None


def c_odd_h(graph, facs):
    """C-ODD on the family's own graph with parity_h: T <-> B is an automorphism of its couplings, every factor is exactly even or odd
    and exactly one is odd. Returns (ok, reason)."""
    V, E = GR.strip(LIST['graphs'][graph]['columns'])
    if not ENT.edges_map_onto(E, ENT.sigma):
        return False, 'T <-> B is not an automorphism of the couplings of %s' % graph
    cls = [parity_h(f) for f in facs]
    if any(c is None for c in cls):
        return False, 'a factor is neither exactly even nor exactly odd: %s' % cls
    if cls.count('odd') != 1:
        return False, '%d odd factors' % cls.count('odd')
    return True, 'one exactly odd factor, the rest exactly even (%s), T <-> B an automorphism of %s' % (cls, graph)


def parity_set():
    """C-PARITY-SET: the entries passing c_odd_h on their own graph are exactly PARITY_ZERO, and exactly those are marked 'zero'.
    m3_run_s9h_v1_1: PARITY_ZERO is empty, so the plants run on a planted entry, Ih,1 with [cp, 1, 0] replaced by [cp, 2, 0] (the parent's
    IhZh: the odd trial state 2 next to the M bond), which must pass c_odd_h on NIH (C-ODD-PLANT-BASE). PLANT-ODD: the planted entry with
    S[1][2] + 1e-12 must fail c_odd_h; PLANT-ODD-H: the planted entry with its bond moved to the T row ([xh, T, 1, 8]) too."""
    import copy
    passing = sorted(e['key'] for e in V3 if c_odd_h(e['graph'], facs_of(e))[0])
    marked = sorted(e['key'] for e in V3 if e['parity'] == 'zero')
    gate('C-PARITY-SET', passing == sorted(PARITY_ZERO) and marked == sorted(PARITY_ZERO), '(the entries whose factors pass C-ODD on their own '
         'graph: %s; marked zero: %s; PARITY_ZERO %s)' % (passing, marked, sorted(PARITY_ZERO)))
    e1 = entries_of('NIH', ['Ih,1'])[0]
    e = dict(e1, factors=[['cp', 2, 0] if enc == ['cp', 1, 0] else enc for enc in e1['factors']])
    ok0, why0 = c_odd_h('NIH', facs_of(e))
    gate('C-ODD-PLANT-BASE', ok0 and e['factors'] != e1['factors'], '(Ih,1 with [cp, 1, 0] replaced by [cp, 2, 0], %s: %s)' % (e['factors'], why0))
    ts2 = copy.deepcopy(TS)
    ts2.S[1][2] = ts2.S[1][2] + 1e-12
    ok, why = c_odd_h('NIH', facs_of(e, ts2))
    plant('PLANT-ODD', not ok, '(the planted entry with S[1][2] + 1e-12: %s)' % why)
    e2 = dict(e, factors=[['xh', 'T', 1, 8] if enc[0] == 'xh' else enc for enc in e['factors']])
    ok2, why2 = c_odd_h('NIH', facs_of(e2))
    plant('PLANT-ODD-H', not ok2, '(the planted entry with its bond moved to the T row, [xh, T, 1, 8]: %s)' % why2)


# ------------------------------------------------------------------ R1: partitions per entry (PLAN_M3_P2_R1 66e85e8b)
RULE_OF = dict([(k, 'std') for k in ('Ih,0', 'Ih,1', 'Ih,3', 'IhTh,1', 'IhTh,3', 'IhTh,0', 'Sh,0', 'Sh,1', 'Sh,3', 'G,0,0')]
               + [(k, 'col') for k in ('Gxh,0,0', 'Gxh,0,1', 'Gxh,0,3', 'Gxh,1,1', 'Gxh,1,3', 'Gxh,3,3', 'GxhR,1,0')])   # m3_run_s9h_v1_1: m3ref_s9h_v1's rules
RULES = ('std', 'col', 'colxh')
PPL = {'exp': True, 'akdrop': True}   # PLANT-PART-EXP and PLANT-AK-DROP, each once per item
AKCPU = {}   # m3_run_s9h_v1_1: no pinned fresh a_k CPU for the S9H keys; the smokes print AK-ONLY-INFO, and akest falls back on the slow estimate


def rule_of_check():
    """C-RULE-OF: RULE_OF names exactly the list's keys, each with a known rule; PLANT-RULE-OF: without its first key it must not."""
    lk = sorted(e['key'] for e in LIST['entries'])
    vals = list(RULE_OF.values())
    gate('C-RULE-OF', sorted(RULE_OF) == lk and set(vals) <= set(RULES), '(RULE_OF names the list\'s %d keys exactly; std %d, col %d, '
         'colxh %d)' % (len(lk), vals.count('std'), vals.count('col'), vals.count('colxh')))
    plant('PLANT-RULE-OF', sorted(RULE_OF)[1:] != lk, '(RULE_OF without its first key must not name the list\'s keys)')


def part_idx(rule, facs):
    """(scal, index groups) of factor tuples under a rule: std is m3_bar_v12.group_factors mapped back to positions by object identity (a
    repeated object takes its next position); col keys a factor by the column of its triple's first vertex, colxh by (that column, 0 for a
    column triple, else 1), groups in key order; col and colxh place only 'p' and 'xi' factors (C1), anything else is refused."""
    if rule == 'std':
        scal, groups = BAR.group_factors(facs)
        used, idx = set(), []
        for gf in groups:
            gi = []
            for f in gf:
                i = next(j for j in range(len(facs)) if facs[j] is f and j not in used)
                used.add(i)
                gi.append(i)
            idx.append(gi)
        return scal, idx
    if rule not in ('col', 'colxh'):
        raise ValueError('partition rule %r' % (rule,))
    if any(f[0] not in ('p', 'xi') for f in facs):
        raise ValueError('rule %s places only p and xi factors, not %s' % (rule, sorted(set(f[0] for f in facs))))
    grp = {}
    for i, f in enumerate(facs):
        k = (f[1][0] // 3,) if rule == 'col' else (f[1][0] // 3, 0 if is_column(f) else 1)
        grp.setdefault(k, []).append(i)
    return 1, [grp[k] for k in sorted(grp)]


def part_enc(rule, encs):
    """C-PART-RULE's independent recomputation from the list's encodings alone: triples [cp, a, c], [xi, R, c], [xic, R, k, c] -> (3c,
    3c + 1, 3c + 2), [xh, R, gap, w] -> (3 gap + r, 3 (gap + 1) + r, w), [xia, t] -> t; std merges overlapping vertex sets in riglap4's
    order (a factor joins the first group it meets, which absorbs the later ones it meets); col and colxh key as part_idx does. Returns
    the groups as lists of encodings."""
    def trip(enc):
        if enc[0] in ('cp', 'xi', 'xic'):
            c = int(enc[-1])
            return (3 * c, 3 * c + 1, 3 * c + 2)
        if enc[0] == 'xh':
            r, gap = 'TMB'.index(enc[1]), int(enc[2])
            return (3 * gap + r, 3 * (gap + 1) + r, int(enc[3]))
        if enc[0] == 'xia':
            return tuple(int(v) for v in enc[1])
        raise ValueError('factor encoding %r' % (enc,))
    ts = [trip(x) for x in encs]
    if rule == 'std':
        groups = []
        for i, t in enumerate(ts):
            vs = set(t)
            hit = [gi for gi, (gv, gl) in enumerate(groups) if gv & vs]
            if not hit:
                groups.append((vs, [i]))
                continue
            gv, gl = groups[hit[0]]
            gv |= vs
            gl.append(i)
            for gi in sorted(hit[1:], reverse=True):
                gv |= groups[gi][0]
                gl.extend(groups[gi][1])
                groups.pop(gi)
        idx = [gl for gv, gl in groups]
    elif rule in ('col', 'colxh'):
        grp = {}
        for i, t in enumerate(ts):
            colt = t[1] == t[0] + 1 and t[2] == t[0] + 2 and t[0] % 3 == 0
            k = (t[0] // 3,) if rule == 'col' else (t[0] // 3, 0 if colt else 1)
            grp.setdefault(k, []).append(i)
        idx = [grp[k] for k in sorted(grp)]
    else:
        raise ValueError('partition rule %r' % (rule,))
    return [[encs[i] for i in gp] for gp in idx]


def part_ok(idx, n):
    """C-PART-ID's index test: the index groups hold 0..n-1 exactly once each, none empty."""
    return bool(idx) and sorted(i for gp in idx for i in gp) == list(range(n)) and all(len(gp) > 0 for gp in idx)


def part_id(groups, facs):
    """C-PART-ID's multiset test (C1): the groups hold exactly the entry's factors, each repr with its multiplicity, none empty."""
    from collections import Counter
    return bool(groups) and all(len(gp) > 0 for gp in groups) and Counter(repr(f) for f in facs) == Counter(repr(f) for gp in groups for f in gp)


def partition_of(e, facs=None):
    """an entry's partition under RULE_OF: rule, G, idx, groups (factor tuples), enc (the list's encodings), scal and the grouping bound
    takes ('std', or ('partition', scal, groups))."""
    facs = facs_of(e) if facs is None else facs
    rule = RULE_OF[name_of(e)]
    scal, idx = part_idx(rule, facs)
    groups = [[facs[i] for i in gp] for gp in idx]
    return {'rule': rule, 'G': len(idx), 'idx': idx, 'groups': groups, 'enc': [[e['factors'][i] for i in gp] for gp in idx], 'scal': scal,
            'grouping': 'std' if rule == 'std' else ('partition', scal, groups)}


def part_line(name, p):
    """the PARTITION line in the float twin's format (m3ref_v1_18_1's p2_before)."""
    return 'PARTITION %s rule %s: G %d: %s' % (name, p['rule'], p['G'], ' | '.join('{' + ', '.join(json.dumps(x) for x in gp) + '}' for gp in p['enc']))


def part_checks(e, facs, p, twin):
    """the PARTITION line, C-PART-ID and C-PART-RULE for one entry; twin: the float twin's KEYJSON of the key."""
    name = name_of(e)
    out(part_line(name, p))
    gate('C-PART-ID', part_ok(p['idx'], len(facs)) and part_id(p['groups'], facs) and p['G'] == len(p['groups']) == len(p['enc']),
         '(%s rule %s: the %d groups hold exactly the entry\'s %d factors as a multiset, none empty; G %d)' % (
             name, p['rule'], len(p['groups']), len(facs), p['G']))
    ind = part_enc(p['rule'], e['factors'])
    tw = (twin.get('rule'), twin.get('G'), twin.get('partition'))
    gate('C-PART-RULE', ind == p['enc'] and tw == (p['rule'], p['G'], p['enc']), '(%s: the groups against the rule %s recomputed from the '
         'list\'s encodings: %s; against the float twin\'s KEYJSON rule %r, G %r, partition: %s)' % (
             name, p['rule'], 'equal' if ind == p['enc'] else 'DIFFERENT', tw[0], tw[1], 'equal' if tw[2] == p['enc'] else 'DIFFERENT'))


def part_plants(graph, parts):
    """the static partition plants, once per item: PLANT-PART-DROP, PLANT-PART-DUP and PLANT-PART-MOVE (m3_run_v1_10_2 l.763-766 gives
    their cases)."""
    names = list(parts)
    e, facs, p = parts[names[0]]
    gd = [list(gp) for gp in p['groups']]
    gd[0] = gd[0][1:]
    plant('PLANT-PART-DROP', not part_id(gd, facs), '(%s: its first group without its first factor %s)' % (names[0], p['enc'][0][0]))
    if graph == 'DT':
        e, facs, p = parts['SM4,2,0']
        xh = ['xh', 'T', 0, 1]
        gi = next(i for i, gp in enumerate(p['enc']) if gp.count(xh) == 2)
        gd = [list(gp) for gp in p['groups']]
        gd[gi].append(p['groups'][gi][p['enc'][gi].index(xh)])
        what = 'SM4,2,0 with a third xhT01 in group %d (its own two copies pass C-PART-ID)' % gi
    else:
        gd = [list(gp) for gp in p['groups']]
        gd[0].append(gd[0][0])
        what = '%s with its first factor %s doubled' % (names[0], p['enc'][0][0])
    plant('PLANT-PART-DUP', not part_id(gd, facs), '(%s)' % what)
    if graph == 'DT':
        name = 'Y4'
        e, facs, p = parts[name]
        s = next(i for i, gp in enumerate(p['enc']) if ['xi', 'MB', 0] in gp)
        j = p['enc'][s].index(['xi', 'MB', 0])
    else:
        name, s = next((n, gi) for n in names for gi, gp in enumerate(parts[n][2]['idx']) if parts[n][2]['G'] >= 2 and len(gp) >= 2)
        e, facs, p = parts[name]
        j = 0
    t = (s + 1) % p['G']
    idx2 = [list(gp) for gp in p['idx']]
    i0 = idx2[s].pop(j)
    idx2[t].append(i0)
    g2 = [[facs[i] for i in gp] for gp in idx2]
    enc2 = [[e['factors'][i] for i in gp] for gp in idx2]
    idok = part_ok(idx2, len(facs)) and part_id(g2, facs)
    plant('PLANT-PART-MOVE', idok and enc2 != part_enc(p['rule'], e['factors']), '(%s with %s moved from group %d to group %d: C-PART-ID %s, '
          'C-PART-RULE must fail)' % (name, e['factors'][i0], s, t, 'passes' if idok else 'FAILS'))


EXP_TARGET = {'ser': (Fraction(1, 2), Fraction(1, 4)), 'bar': (Fraction(1),), 'barp': (Fraction(1, 2),)}


def exp_ok(keys, G):
    """C-PART-EXP's test on an entry's unit keys 'g|gi|what|i|q|which': G >= 1, every gi < G, every q > 0 with G x 1/q exactly a target of
    its kind (ser: 1/2 at fnorm's 2G, 1/4 at nF4c's 4G; bar: 1 at EF4's G; barp: 1/2 at nF0p's 2G; a Hoelder product takes every group at
    one exponent, so G x 1/q is its sum of 1/q), and every group with its barp norm."""
    if G < 1:
        return False
    bp = set()
    for k in keys:
        if not k.startswith('g|'):
            continue
        _, gi, what, i, q, which = k.split('|')
        gi, q = int(gi), int(q)
        if gi >= G or what not in EXP_TARGET or q <= 0 or Fraction(G, q) not in EXP_TARGET[what]:
            return False
        if what == 'barp':
            bp.add(gi)
    return bp == set(range(G))


def exp_from(keys, G, H):
    """the unit keys with every group norm's exponent rewritten from H in place of G (2G -> 2H, 4G -> 4H, G -> H), for PLANT-PART-EXP."""
    res = []
    for k in keys:
        if not k.startswith('g|'):
            res.append(k)
            continue
        _, gi, what, i, q, which = k.split('|')
        res.append('g|%s|%s|%s|%d|%s' % (gi, what, i, (int(q) // G) * H, which))
    return res


def part_exp_check(name, p, keys):
    """C-PART-EXP on a finished free entry's unit keys (restored units included), with PLANT-PART-EXP once per item."""
    G = p['G']
    gk = [k for k in keys if k.startswith('g|')]
    kinds = sorted(set((k.split('|')[2], int(k.split('|')[4])) for k in gk))
    gate('C-PART-EXP', exp_ok(keys, G), '(%s: G %d; %d group norms at (kind, exponent) %s; G x 1/q exactly 1/2, 1/4, 1 and 1/2 for ser 2G, ser '
         '4G, bar G and barp 2G, every group with its barp)' % (name, G, len(gk), kinds))
    if PPL['exp']:
        PPL['exp'] = False
        plant('PLANT-PART-EXP', not exp_ok(exp_from(keys, G, G - 1), G), '(%s: the same norms with exponents from G - 1 = %d)' % (name, G - 1))


def ak_only(pr, facs, grouping, label):
    """the certified series-only a_k of facs under grouping, with bound's info and its CPU: m3_bar_v12's own bound with bars=False, run
    with the prep's ok False on an empty group cache with no budget and no unit callback, so only the groups' series are built; ok, group
    cache, unit state, budget and callback are restored after. The a_k table is the entry's own request (same forms, D and caps): a cache
    hit when the entry's 'ak' unit ran in this process, built afresh on a resumed entry and for PLANT-AK-DROP's product."""
    keep = (pr.ok, getattr(pr, 'gcache', {}), pr.ustate, pr.ubudget, pr.unit_done)
    pr.ok, pr.gcache, pr.ubudget, pr.unit_done = False, {}, None, None
    t0 = cpu()
    try:
        ak, _, info = pr.bound(facs, grouping, bars=False, entry=label)
    finally:
        pr.ok, pr.gcache, pr.ustate, pr.ubudget, pr.unit_done = keep
    return ak, info, cpu() - t0


def meets(x, y):
    """True iff two intervals overlap (exact comparisons of their ends)."""
    return x.a <= y.b and y.a <= x.b


def ak_same(pr, name, p, ak, info, facs):
    """C-AK-SAME (an entry off std): every a_k ball under the partition overlaps the standard grouping's series-only a_k ball (ak_only);
    AK-ONLY-INFO: its forms and Dn against the partition run's, the table count before and after, its CPU. Returns the
    standard a_k."""
    nt0 = len(pr.tables)
    akstd, inf2, dt = ak_only(pr, facs, 'std', name + ' (standard grouping, series only)')
    out('AK-ONLY-INFO %s: forms %s the partition run\'s, Dn %d (the partition run: %d), tables %d -> %d, %.2f s' % (
        name, 'equal to' if inf2['forms'] == info['forms'] else 'DIFFERENT from', inf2['Dn'], info['Dn'], nt0, len(pr.tables), dt))
    ov = [meets(x, y) for x, y in zip(ak, akstd)]
    w = max(abs(float(x.mid) - float(y.mid)) / max(1.0, abs(float(y.mid))) for x, y in zip(ak, akstd))
    gate('C-AK-SAME', len(ak) == len(akstd) == 4 and all(ov), '(%s rule %s: its a_k balls against the standard grouping\'s series-only a_k: '
         'overlap %s; largest mid difference / max(1, |a_k|) %.2e, INFO)' % (name, p['rule'], ov, w))
    return akstd


def ak_drop_plant(pr, e, facs, p, akstd):
    """PLANT-AK-DROP, once per item: the partition without its first xi factor must give a_k that miss the standard a_k at some k."""
    if not PPL['akdrop']:
        return
    PPL['akdrop'] = False
    gi, j = next((gi, j) for gi, gp in enumerate(p['groups']) for j, f in enumerate(gp) if f[0] == 'xi')
    enc0 = p['enc'][gi][j]
    gd = [list(gp) for gp in p['groups']]
    gd[gi].pop(j)
    gd = [gp for gp in gd if gp]
    ak2, _, dt = ak_only(pr, facs, ('partition', p['scal'], gd), name_of(e) + ' (planted: %s dropped)' % enc0)
    ov = [meets(x, y) for x, y in zip(ak2, akstd)]
    plant('PLANT-AK-DROP', not all(ov), '(%s: its partition without the factor %s: overlap with the standard a_k %s; %.2f s)' % (name_of(e), enc0, ov, dt))


def gcache_ok(gc, grs, pairs):
    """C-GCACHE's test: every group of grs [(name, gi, factor tuples)] has its entry in gc under the repr of its full factor tuples,
    distinct tuple lists have distinct entry objects, and each named pair of different lists has two different entries."""
    keys = {repr(gf) for _, _, gf in grs}
    if not keys or not all(k in gc for k in keys):
        return False
    if len({id(gc[k]) for k in keys}) != len(keys):
        return False
    return all(repr(a) != repr(b) and gc[repr(a)] is not gc[repr(b)] for a, b in pairs)


def gcache_check(graph, pr, parts):
    """C-GCACHE: gcache_ok on the family's groups and the prep's group cache, DT with the named pairs Y4/SM4,2,0 groups 0
    and 1. PLANT-GCACHE: a key by the column of a group's first factor merges two groups whose tuples differ (DT: the two groups 0;
    elsewhere the first group and a copy with c0 or q1 moved). PLANT-GCACHE-RUN: gcache_ok must refuse two bad copies
    of the cache, one where two different tuple lists share one entry object and one without a list's entry."""
    gc = getattr(pr, 'gcache', {})
    grs = [(n, gi, gf) for n, (e, facs, p) in parts.items() for gi, gf in enumerate(p['groups'])]
    keys = sorted({repr(gf) for _, _, gf in grs})
    pairs, named = [], ''
    if graph == 'DT':
        y, s = parts['Y4'][2], parts['SM4,2,0'][2]
        pairs = [(y['groups'][i], s['groups'][i]) for i in (0, 1)]
        named = '; named pairs Y4 and SM4,2,0 groups 0 (%s, %s) and 1 (%s, %s)' % (y['enc'][0], s['enc'][0], y['enc'][1], s['enc'][1])
    gate('C-GCACHE', gcache_ok(gc, grs, pairs), '(%s: %d groups of %d entries, %d distinct factor-tuple lists, each with its own entry under '
         'its repr%s)' % (graph, len(grs), len(parts), len(keys), named))
    colkey = lambda gf: gf[0][1][0] // 3
    if graph == 'DT':
        a, b = parts['Y4'][2]['groups'][0], parts['SM4,2,0'][2]['groups'][0]
        what = 'Y4 group 0 and SM4,2,0 group 0'
    else:
        a = grs[0][2]
        f = a[0]
        f2 = (f[0], f[1], f[2] + 1.0, f[3]) if f[0] == 'xi' else (f[0], f[1], [x + 1e-3 for x in f[2]], f[3], f[4])
        b = [f2] + list(a[1:])
        what = '%s group %d and a copy with its first factor moved' % (grs[0][0], grs[0][1])
    plant('PLANT-GCACHE', colkey(a) == colkey(b) and repr(a) != repr(b), '(%s: one column key %r, different factor tuples)' % (what, colkey(a)))
    bad1 = dict(gc)
    bad1[keys[1]] = gc.get(keys[0])
    bad2 = {k: v for k, v in gc.items() if k != keys[0]}
    r1, r2 = gcache_ok(bad1, grs, pairs), gcache_ok(bad2, grs, pairs)
    plant('PLANT-GCACHE-RUN', not r1 and not r2, '(%s: the gate\'s test on the cache with two different tuple lists sharing one entry: %s; '
          'without one list\'s entry: %s)' % (graph, 'accepted' if r1 else 'refused', 'accepted' if r2 else 'refused'))


BARPOS_PTS = ('X = 0', 'X = 1', 'X_f = 1 + (f mod 3)', 'X_f = 0 (f even), 2 (f odd)')


def barpos_points(nv):
    return [[0] * nv, [1] * nv, [1 + f % 3 for f in range(nv)], [0 if f % 2 == 0 else 2 for f in range(nv)]]


def poly_at(items, x):
    """a polynomial's value at an integer point as an mp.iv interval, from its (exponent, mp.iv coefficient) items (m3_scal.spoly_iv,
    converted once per polynomial)."""
    tot = iv.mpf(0)
    for ex_, c in items:
        t = c
        for i, k in enumerate(ex_):
            if k:
                t = t * (x[i] ** k)
        tot = tot + t
    return tot


def barpos_info(graph, pr, parts):
    """C-BARPOS-INFO and PLANT-BARPOS (m3_run_v1_10_2 l.966-970 gives the argument): odd-G bars are >= 0 by
    construction; INFO at BARPOS_PTS; X_0 - X_1 must be flagged."""
    seen, nev, flagged, nneg, ncoef, t0 = set(), 0, [], 0, 0, cpu()
    for n, (e, facs, p) in parts.items():
        if p['G'] % 2 == 0:
            continue
        for gi, gf in enumerate(p['groups']):
            if repr(gf) in seen:
                continue
            seen.add(repr(gf))
            for j, P in enumerate(pr.gdata(gf)['bar']):
                if BAR.is_zero(P):
                    continue
                items = list(S.spoly_iv(P).items())
                ncoef += len(items)
                nneg += sum(1 for ex_, c in items if c.a < 0)
                for lab, x in zip(BARPOS_PTS, barpos_points(P.nv)):
                    nev += 1
                    v = poly_at(items, x)
                    if v.b < 0:
                        flagged.append('%s group %d Fbar_%d at %s: upper end %s' % (n, gi, j, lab, v.b))
    out('C-BARPOS-INFO %s: %d distinct groups of odd-G entries, %d evaluations of Fbar_0..4 at %s; certainly negative: %s; coefficients with '
        'a negative lower end %d of %d (%.2f s)' % (graph, len(seen), nev, list(BARPOS_PTS), '; '.join(flagged[:10]) if flagged else 'none',
                                                   nneg, ncoef, cpu() - t0))
    nv = pr.g.F
    e0, e1 = [0] * nv, [0] * nv
    e0[0], e1[1] = 1, 1
    pm = list(S.spoly_iv(S.spoly(K, {tuple(e0): 1, tuple(e1): -1}, nv)).items())
    neg = [lab for lab, x in zip(BARPOS_PTS, barpos_points(nv)) if poly_at(pm, x).b < 0]
    plant('PLANT-BARPOS', bool(neg), '(X_0 - X_1 flagged at %s)' % neg)


def laws_of(pr, mF):
    """U3's laws (PLAN_M3_CODE_v1_2 sect. C) and Lemma U's far rate (lower end) for an entry with J-degree m_F."""
    g = pr.g
    cF = mF + Fraction(g.n * (g.V - 1), 2)
    rate = pr.alpha_lo - S.I(cF) / 300
    return {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, g.Gvv)]},
            'ann': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, pr.tilt_p['Gvv'])]},
            'far_rate': S.down(rate), 'far_cF': str(cF)}, rate


def has0(ak):
    """C-ODD-AK's test (m3_run_v1_10_1: a function, for PLANT-AK-ZERO): every a_k ball contains 0 (exact comparisons of its ends)."""
    return all(a.a <= 0 <= a.b for a in ak)


def ak_total_plants():
    """m3_run_v1_10_1, once per smoke: PLANT-AK-TOTAL, m3_bar_v13.ak_failing at the layer's FALLBACK_REL must refuse a total of radius
    3e-3 |mid| and one of midpoint 0 and pass one of radius 1e-7 |mid|; PLANT-AK-ZERO, has0 must fail on [1e-9, 2e-9] and pass on
    [-1e-9, 2e-9]."""
    bad = BAR.ak_failing([iv.mpf(['0.997', '1.003']), iv.mpf(['-1e-9', '1e-9']), iv.mpf(['0.9999999', '1.0000001'])], K.FALLBACK_REL)
    plant('PLANT-AK-TOTAL', bad == [0, 1], '(ak_failing at FALLBACK_REL %g on totals of radius 3e-3 |mid|, midpoint 0 and radius 1e-7 |mid|: '
          'refused %s, [0, 1] wanted)' % (K.FALLBACK_REL, bad))
    plant('PLANT-AK-ZERO', not has0([iv.mpf(['1e-9', '2e-9'])]) and has0([iv.mpf(['-1e-9', '2e-9'])]), '(has0 on [1e-9, 2e-9] must fail and '
          'on [-1e-9, 2e-9] pass)')


def norm_rel_plants():
    """m3_run_v1_10_4, once per smoke and entry piece: m3_bar_v16_1.rule_plants (its docstring lists them)."""
    for n_, f_, l_ in BAR.rule_plants(K):
        plant(n_, f_, l_)


def compute_entry(pr, e, twin, state=None):
    """one entry under its partition (R1): PARTITION, C-PART-ID, C-PART-RULE, QCAP (qcap_of timed, printed, and in pieces
    given to the slow estimate); parity zeros: C-ODD and a_k balls containing 0, no bars; free entries: the bars, C-PART-EXP and, off std,
    C-AK-SAME with AK-ONLY-INFO (PLANT-AK-DROP once per item), which a budget refusal defers to the next piece by a checkpoint holding every
    unit of the entry. The result carries rule, G, groups and qcap. m3_run_v1_10_1: a parity zero's bound takes ak_zero=True; a resumed
    off-std entry whose 'ak' unit was restored defers C-AK-SAME the same way unless pr.akest allows its fresh table (AKCPU)."""
    name = name_of(e)
    t0 = cpu()
    STAGE[0] = 'entry %s' % name
    facs = facs_of(e)
    p = partition_of(e, facs)
    part_checks(e, facs, p, twin)
    tq = cpu()
    pr.qcap, qmax = qcap_of(pr, p)
    dq = cpu() - tq
    if pr.unit_done is not None:
        pr.unit_done(dq, False)
    out('QCAP %s: the largest pair degree of its F_i %d; qcap %d (the float twin\'s %r); qcap_of %.2f s (the groups\' series, majorants and '
        'F_i)' % (name, qmax, pr.qcap, twin.get('qcap'), dq))
    pf = {'rule': p['rule'], 'G': p['G'], 'groups': p['enc'], 'qcap': pr.qcap}
    pr.maxrel = 0.0
    if e['parity'] == 'zero':
        ok, why = c_odd_h(e['graph'], facs)   # m3_run_v1_10: C-ODD with parity_h on the family's own graph
        gate('C-ODD', ok, '%s: %s' % (name, why))
        ak, _, info = pr.bound(facs, p['grouping'], bars=False, entry=name, state=state, ak_zero=True)   # m3_run_v1_10_1: no total test
        gate('C-ODD-AK', has0(ak), '%s: every a_k ball contains 0 (widest %.1e)' % (name, max(float((a.b - a.a).b) for a in ak)))
        out('STAGE-CPU entry %s %.2f s (parity zero)%s' % (name, cpu() - t0, resumed(state)))
        return dict({'name': name, 'parity': 'zero', 'ak': ak, 'cpu': cpu() - t0}, **pf)
    rows = pr.declare_big(p['groups'], p['scal'], *RULE_A[e['graph']])   # m3_run_v1_10_4: the big set, declared before the bound (F-1)
    out('BIGRULE-SET %s: %d norms declared; the big set %s' % (name, len(rows), ['%s forms %d D %d moments %d' % r[:4] for r in rows if r[4]]))
    ak, bars, info = pr.bound(facs, p['grouping'], entry=name, state=state)
    part_exp_check(name, p, list(pr.ustate['vals']))
    if p['rule'] != 'std':
        if pr.ubudget is not None and not pr.ubudget():   # every unit is done: the next piece restores them all and starts here
            pr.ustate['maxrel'] = pr.maxrel
            raise BAR.Checkpoint(pr.ustate)
        if state is not None and 'ak' in state['vals'] and getattr(pr, 'akest', None) is not None and not pr.akest(AKCPU.get(name, 0.0)):
            pr.ustate['maxrel'] = pr.maxrel   # m3_run_v1_10_1 (extra): ak_only builds the restored 'ak' table afresh; the next piece starts here
            raise BAR.Checkpoint(pr.ustate)
        akstd = ak_same(pr, name, p, ak, info, facs)
        ak_drop_plant(pr, e, facs, p, akstd)
    laws, rate = laws_of(pr, info['mF'])
    gate('C-MONO-FAR', rate.a > 0, '%s: far rate alpha_min - (m_F + n(V-1)/2)/J_REF = %.4e > 0 (m_F %d)' % (name, S.down(rate), info['mF']))
    a0 = 1 if all(f[0] == 'p' for f in facs) else None
    rec = REC.entry_record(ak, bars, T_REF, 'free', a0_exact=a0, laws=laws)
    barsum = rec['Bp']['rem'] + rec['Bp']['tail'] + rec['Bp']['ann'] + rec['Bp']['far']
    okb = BAR.budget_ok(pr.maxrel, rec['B']['rnd'], barsum)   # m3_run_v1_10_2: the norm limit is the bar's NORM_REL
    gate('C-BUDGET', okb, '%s: largest relative radius of a norm %.3e (<= NORM_REL %g; big-rule norms out), rnd %.2e <= 0.1 x bar %.3e' % (
        name, pr.maxrel, BAR.NORM_REL, rec['B']['rnd'], barsum))
    exk = {k.split(':', 2)[2]: v for k, v in EXEMPT.items() if k.split(':', 2)[:2] == [e['graph'], name]}
    over, exo = BAR.cap_over(info['big'], INFL_CAP, tuple(exk)), BAR.exempt_over(info['big'], exk)
    gate('C-BIGCAP', not over and not exo, '%s: big-rule inflations at most %g but the exempt %s, whose e is at most 1.1 x declared: over %s, '
         'exempt over %s' % (name, INFL_CAP, sorted(exk.items()), over, exo))
    out('BIGRULE-INFO %s: %d norms by the big-table rule, largest inflation %s' % (name, len(info['big']), BAR.infl_str(info['big_max'])))
    ln = BAR.part_lines(info['big'], 1.15, tuple(exk))
    rr = [(q, rec['B'][q] / twin['B'][q]) for q in ('rem', 'tail', 'ann', 'far') if twin.get('B', {}).get(q, 0) > 0]
    rb = sorted((r / ln[q], r, ln[q], q) for q, r in rr)
    out('REP-B-INFO %s: certified/float bar parts / their lines %s; largest ratio %s; margin %s (asm\'s C-REP-B: ratio <= line)' % (
        name, ', '.join('%s %.6f/%.6f' % (q, r, L) for m, r, L, q in rb), ('%.6f (%s)' % max((r, q) for q, r in rr)) if rr else 'none',
        ('%.6f (%s)' % (rb[-1][0], rb[-1][3])) if rb else 'none'))
    out('AKRAD-INFO %s: largest relative radius of an a_k %.2e' % (name, info.get('ak_relrad', 0.0)))
    out('ENTRY %s ak %s err %.9e parts rem %.9e tail %.9e ann %.9e far %.9e rnd %.3e groups %d Dn %d forms %d' % (
        name, ['%.12g' % x for x in rec['ak']], rec['err'], rec['B']['rem'], rec['B']['tail'], rec['B']['ann'], rec['B']['far'], rec['B']['rnd'],
        info['groups'], info['Dn'], len(info['forms'])))
    out('STAGE-CPU entry %s %.2f s%s' % (name, cpu() - t0, resumed(state)))
    return dict({'name': name, 'parity': 'free', 'ak': ak, 'bars': bars, 'a0_exact': a0, 'laws': laws, 'maxrel': pr.maxrel, 'big': info['big'],
                 'cpu': cpu() - t0}, **pf)


def plant_mono(pr):
    """PLANT-MONO: with theta0 = 1e-3 the far rate must not be certainly positive."""
    g = pr.g
    alpha = min((S.I(1e-3) * S.I(pr.ap) / (2 * gv)).a for gv in g.Gvv)
    rate = alpha - S.I(Fraction(g.n * (g.V - 1), 2)) / 300
    plant('PLANT-MONO', not (rate.a > 0), '(theta0 = 1e-3: far rate %.3e)' % S.down(rate))


def header(fam):
    return {'script': SELF_SHA, 'item': ITEM, 'family': fam, 'N': NN, 'kernel': '%s:%s' % (KERNEL, KFILES[KERNEL + '.py'][:8]),
            'arb_kernel': '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), 'trial': TRIAL, 'format': 'm3_run_s9h_v1_1 hand-off'}


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
    name = 'm3_run_s9h_v1_1_%s.json' % ITEM
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
    name = 'm3_run_s9h_v1_1_%s.json' % item
    hdr, body = HO.read(name, os.path.join(OUTD, 'm3_run_s9h_v1_1_%s.out' % item), {'script': SELF_SHA, 'item': item, 'N': NN, 'family': fam},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (name, valid_verdict()))
    return body


def read_handoff_v18(item):
    """m3_run_v1_8_3's reader of m3_run_v1_8's N prep hand-offs (C-PREP-SAME), bound to V18_SHA and to its producer output."""
    name = 'm3_run_v1_8_%s.json' % item
    hdr, body = HO.read(name, os.path.join(OUTD, 'm3_run_v1_8_%s.out' % item), {'script': V18_SHA, 'item': item, 'N': NN, 'family': 'N'},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: m3_run_v1_8\'s producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (
        name, valid_verdict()))
    return body


def read_parent(item, fam):
    """m3_run_s9h_v1_1: pk03's hand-off m3_run_v1_10_4_<item>.json (a prep stage VNu, VNc, VDu or VDc of the parent), read by pk03's
    own m3_handoff_v3 (HO_IN, HAND pk03/hand) against its producer output in pk03/out: VERDICT lines exactly [VERDICT VALID], the
    HANDOFF line's sha256, the END checksum, and the header bound to the parent's sha256 (PARENT_SHA), the item, N and the vertex graph."""
    name = 'm3_run_v1_10_4_%s.json' % item
    hdr, body = HO_IN.read(name, os.path.join(OUTD_IN, 'm3_run_v1_10_4_%s.out' % item), {'script': PARENT_SHA, 'item': item, 'N': NN,
                           'family': fam}, valid_verdict())
    gate('C-HANDOFF', True, '(%s, pk03\'s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header with the parent\'s '
         'sha256 %s)' % (name, valid_verdict(), PARENT_SHA[:8]))
    return body


def parent_prep_graph(vg):
    """m3_run_s9h_v1_1, C-PREP-SHARE: the graph the parent's prep stages of vg ran on, prep_graph of P2_RUN_LIST_v1_10's graph of VGP2[vg]
    (the parent's first family served by vg), built as the parent's family_graph builds it. prep_same(graph, g, parent_prep_graph(vg), pr)
    then runs C-PREP-GRAPH of this family's graph against it: the inputs, and exactly the C-1 and C-4 values at pr's rate vectors."""
    spec = LISTP2['graphs'][VGP2[vg]]
    V, E = GR.strip(spec['columns'])
    return prep_graph(GR.GraphIV(V, E, sorted(tuple(sorted(p)) for p in spec['pairs']), NN))


def iv_leaves(v, lab=''):
    """the (label, interval) leaves of a scalar container: dicts by sorted key, lists by index."""
    if isinstance(v, dict):
        return sum((iv_leaves(v[k], '%s[%s]' % (lab, k)) for k in sorted(v, key=str)), [])
    if isinstance(v, (list, tuple)):
        return sum((iv_leaves(x, '%s[%d]' % (lab, i)) for i, x in enumerate(v)), [])
    return [(lab, v)]


def prep_cross(stg, scal):
    """C-PREP-SAME (VN only): every scalar of this stage must overlap m3_run_v1_8's N hand-off of the same stage (same vertices,
    couplings and radii; arbeng_ma_v1_3); bit-identical leaves and the largest relative mid difference are INFO. PLANT-PREP-SAME: N's
    first scalar moved by ten times both widths plus 1e-12 of its size must stop overlapping."""
    ref = read_handoff_v18('N%s.%d' % (stg, NN))['scal']
    la, lb = iv_leaves(scal), iv_leaves(ref)
    labs = [k for k, _ in la] == [k for k, _ in lb]
    ok, nsame, worst = labs, 0, (0.0, '-')
    if labs:
        for (k, x), (_, y) in zip(la, lb):
            ok = ok and meets(x, y)
            nsame += x._mpi_ == y._mpi_
            worst = max(worst, (abs(float(x.mid) - float(y.mid)) / max(abs(float(y.mid)), 1e-300), k))
    gate('C-PREP-SAME', ok, '(VN stage %s against m3_run_v1_8\'s N%s.%d: %d scalars, labels %s, every one overlapping: %s; %d bit-identical; '
         'largest relative mid difference %.1e at %s)' % (stg, stg, NN, len(la), 'equal' if labs else 'DIFFERENT', ok, nsame, worst[0], worst[1]))
    (k0, x0), (_, y0) = la[0], lb[0]
    y1 = y0 + 10 * ((x0.b - x0.a) + (y0.b - y0.a)) + abs(y0.mid) * iv.mpf('1e-12') + iv.mpf('1e-300')
    plant('PLANT-PREP-SAME', not meets(x0, y1), '(%s: N\'s value moved by ten times both widths plus 1e-12 of its size)' % k0)


def prep_rep(vg, pr, rp, stg):
    """PREP-REP (INFO): a finished stage's scalars against the reference record's PREPJSON, upper end / float."""
    keys = {'u': ('rE', 'rE_parts', 'nE', 'nE4'), 'c': ('nC8', 'nC6', 'Pout', 'Pout_p', 'farbase')}[stg]
    rows = []
    for k in keys:
        for lab, x in iv_leaves(getattr(pr, k)):
            f = rp[k]
            for part in [p for p in re.findall(r'\[([^\]]*)\]', lab)]:
                f = f[int(part)] if isinstance(f, list) else f[part]
            if isinstance(f, (int, float)) and f > 0:
                rows.append((S.up(x) / f, k + lab))
    rows.sort()
    if not rows:
        out('PREP-REP %s stage %s: no scalar with a positive float value' % (vg, stg))
        return
    out('PREP-REP %s stage %s: %d scalars, certified upper end / float in [%.6f (%s), %.6f (%s)]; %s' % (
        vg, stg, len(rows), rows[0][0], rows[0][1], rows[-1][0], rows[-1][1], '; '.join('%s %.6f' % (lab, r) for r, lab in rows)))


def prep_graph(g):
    """the graph the prep stages run on: GraphIV(V, E, [], N, S_gauge) with the family graph
    g's V, N, edge list (pairs and tags, in order) and S_gauge, so F = V; prep_same checks it (C-PREP-GRAPH)."""
    return GR.GraphIV(g.V, list(g.edges), [], g.N, list(g.S_gauge))


def prep_view(G, pr):
    """what the prep reads of a graph object (C-PREP-GRAPH): the inputs (V, N, S_gauge, the edges with tags in order); C-1's values (the
    vertex block of Gam, G_vv, log_tau, log_det_Lr, W_int's vertex columns, and at pr.rates and pr.ratesp tilted()'s vertex Gam, Gvv and
    N); C-4's values (Pout, Pout_p, tree(), farbase, alpha_lo, formed as Prep.stage_c forms them), or 'not formed (<error>)' when they are
    not finite (S_gauge [0] makes vertex 0's G_vv exactly 0)."""
    V = G.V
    vb = lambda M: [list(r[:V]) for r in M[:V]]
    tl = lambda T: None if T is None else {'Gam': vb(T['Gam']), 'Gvv': list(T['Gvv']), 'N': T['N']}
    tc, tp = G.tilted(pr.rates), G.tilted(pr.ratesp)
    ins = {'V': G.V, 'N': G.N, 'S_gauge': list(G.S_gauge), 'edges': [(tuple(e), c) for e, c in G.edges]}
    c1 = {'Gam': vb(G.Gam), 'Gvv': list(G.Gvv), 'log_tau': G.log_tau, 'log_det_Lr': G.log_det_Lr, 'W_int': [list(r[:V]) for r in G.W_int],
          'tilt_c': tl(tc), 'tilt_p': tl(tp)}
    c4 = None
    if tp is not None:
        th, ap = S.I(pr.theta0), S.I(pr.ap)
        try:   # m3_run_v1_9_3
            tree = G.tree()
            c4 = {'Pout': S.isum(S.chi_tail_up(pr.J * S.I(a) / gv, G.n) for a, gv in zip(pr.a_v, G.Gvv)),
                  'Pout_p': S.isum(S.chi_tail_up(pr.J * S.I(a) / gv, G.n) for a, gv in zip(pr.a_v, tp['Gvv'])),
                  'tree': tree, 'farbase': S.far_base(pr.J, th, ap, G.Gvv, tree, G.N, G.V, G.log_tau),
                  'alpha_lo': min((th * ap / (2 * gv)).a for gv in G.Gvv)}
        except (ArithmeticError, ValueError) as ex:
            c4 = 'not formed (%s)' % type(ex).__name__
    return ins, c1, c4


VIEW_PARTS = ('inputs', 'C-1 values', 'C-4 values')


def view_diff(a, b):
    """the parts of two prep_views that differ: the inputs by ==, the values by their raw interval ends (same(): equal _mpi_ tuples)."""
    return [n_ for n_, x, y in zip(VIEW_PARTS, a, b) if not same(x, y)]


def prep_same(graph, g, gp, pr):
    """C-PREP-GRAPH: the prep graph gp has no pair forms (pairs [], F = V) and its prep_view equals the
    family graph g's exactly at pr's rate vectors, both C-4 values formed. Plants (C-2), each must make that comparison fail: the first
    edge dropped (PLANT-PREP-EDGE), its tag changed (PLANT-PREP-TAG), S_gauge [0] (PLANT-PREP-GAUGE), and gp's view with vertex-block entry
    [0][1] moved up one unit of each end's last bit (PLANT-PREP-ULP: it still overlaps, so only an endpoint-exact test refuses it)."""
    import types
    vg, vp = prep_view(g, pr), prep_view(gp, pr)
    d0 = view_diff(vg, vp)
    formed = isinstance(vg[2], dict) and isinstance(vp[2], dict)
    ok = gp.pairs == [] and gp.F == gp.V and formed and not d0
    gate('C-PREP-GRAPH', ok, '(%s: the prep graph has V %d, F %d and pairs %r (the family graph: F %d); against the family graph, V, N, '
         'S_gauge and the %d edges with tags in order equal, and exactly (equal _mpi_ tuples) the %d x %d vertex block of Gam, %d G_vv, '
         'log_tau, log_det_Lr, W_int\'s vertex columns and tilted()\'s vertex Gam, G_vv and N at both rate vectors (C-1), and Pout, Pout_p, '
         'tree(), farbase and alpha_lo (C-4)%s%s)' % (graph, gp.V, gp.F, gp.pairs, g.F, len(g.edges), g.V, g.V, len(g.Gvv),
                                                      ('; differ: ' + ', '.join(d0)) if d0 else '',
                                                      '' if formed else '; C-4 values of the family and prep graphs: %r, %r' % (
                                                          vg[2] if not isinstance(vg[2], dict) else 'formed',
                                                          vp[2] if not isinstance(vp[2], dict) else 'formed')))
    E, S0 = list(g.edges), list(g.S_gauge)
    t1 = 'B' if E[0][1] == 'A' else 'A'
    for lab, what, gx in (('PLANT-PREP-EDGE', 'its first edge %r dropped' % (E[0],), GR.GraphIV(g.V, E[1:], [], g.N, S0)),
                          ('PLANT-PREP-TAG', 'its first edge\'s tag %r changed to %r' % (E[0][1], t1),
                           GR.GraphIV(g.V, [(E[0][0], t1)] + E[1:], [], g.N, S0)),
                          ('PLANT-PREP-GAUGE', 'S_gauge [0]', GR.GraphIV(g.V, E, [], g.N, [0]))):
        dx = view_diff(vg, prep_view(gx, pr))
        plant(lab, bool(dx), '(%s: the prep graph with %s, against the family graph: differs in %s)' % (graph, what, ', '.join(dx) or 'nothing'))
    x = vp[1]['Gam'][0][1]
    mv = types.SimpleNamespace(_mpi_=tuple(libmp.mpf_add(r, libmp.from_man_exp(1, r[2]), 0) for r in x._mpi_))
    (a0, b0), (a1, b1) = [_ef(r) for r in x._mpi_], [_ef(r) for r in mv._mpi_]
    c1m = dict(vp[1], Gam=[list(r) for r in vp[1]['Gam']])
    c1m['Gam'][0][1] = mv
    dx = view_diff(vg, (vp[0], c1m, vp[2]))
    lap = a1 <= b0 and a0 <= b1
    plant('PLANT-PREP-ULP', bool(dx) and lap, '(%s: a copy of the prep graph\'s view with its vertex-block entry [0][1] moved up by one unit '
          'of each end\'s last bit (overlapping the original: %s), against the family graph: differs in %s)' % (graph, lap, ', '.join(dx) or 'nothing'))


PACK_LIM = 9 * 10 ** 18   # the strictest table encoder: arbeng_c2b_v2's AllMom2A asserts float(D + 1)^F < 9.0e18 (the layer's _code_guard: 2^63)


def pack_ok(forms, D, lp):
    """C-PACK-PLAN's test of one table request: (D + 1)^forms below PACK_LIM in exact integers, and D <= 64 for an lp norm."""
    return (D + 1) ** forms < PACK_LIM and (not lp or D <= 64)


def pack_plan(pr, facs, grouping, info, bars):
    """C-PACK-PLAN's requests for one entry, (what, forms, D, lp), distinct, from the polynomials the smoke built (none built here): the a_k
    table and, for a free entry, m0u/m0c and every group norm as bound requests them (m3_bar_v16_1.declare_big lists the same norms)."""
    import numpy as np
    use = info['forms']
    reqs = [('a_k', len(use), max(info['Dn'], 1), False)]
    if not bars:
        return reqs
    if isinstance(grouping, tuple) and len(grouping) == 3 and grouping[0] == 'partition':
        scal, groups = grouping[1], [list(gf) for gf in grouping[2]]
    elif grouping == 'std':
        scal, groups = BAR.group_factors(facs)
    elif grouping == 'split':
        scal, groups = BAR.split_groups(facs)
    else:
        raise ValueError('grouping %r' % (grouping,))
    G_ = max(len(groups), 1)
    gds = [pr.gdata(gf) for gf in groups]
    d0 = 2 * BAR.deg(pr.series_product([d['ser'] for d in gds], scal, 0)[0]) if groups else 0
    reqs.append(('m0u m0c', len(use), max(d0, 1), False))
    shape = {}

    def req(lab, P, p, pos):
        if id(P) not in shape:
            shape[id(P)] = (int(np.count_nonzero(P.ex.any(axis=0))), int(P.ex.sum(axis=1).max())) if len(P.ex) else (0, 0)
        nf, dq = shape[id(P)]
        r = (lab, nf, dq * p if pos else 2 * dq * (p // 2), not pos)
        if nf and r not in reqs:
            reqs.append(r)
    for i in (1, 2, 3):
        for c in BAR.comps(i, len(groups)):
            for gi, ig in enumerate(c):
                req('group %d ser %d p %d' % (gi, ig, 2 * G_), gds[gi]['ser'][ig], 2 * G_, False)
    for c in BAR.comps(0, len(groups)):
        for gi, ig in enumerate(c):
            req('group %d ser %d p %d' % (gi, ig, 4 * G_), gds[gi]['ser'][ig], 4 * G_, False)
    for c in BAR.comps(4, len(groups)):
        for gi, jg in enumerate(c):
            req('group %d bar %d p %d' % (gi, jg, G_), gds[gi]['bar'][jg], G_, True)
    for gi in range(len(gds)):
        req('group %d barp p %d' % (gi, 2 * G_), gds[gi]['barp'], 2 * G_, False)
    return reqs


def pack_gate(graph, plans):
    """C-PACK-PLAN over a family's entries (plans: [(entry, (what, forms, D, lp))]) with PLANT-PACK-PLAN (D 16 over 16 forms refused,
    the control D 14 over 16 forms accepted)."""
    bad = [(nm, r) for nm, r in plans if not pack_ok(r[1], r[2], r[3])]
    nm, r = max(plans, key=lambda x: x[1][1] * math.log(x[1][2] + 1))
    lpm = max([x[1][2] for x in plans if x[1][3]] + [0])
    gate('C-PACK-PLAN', bool(plans) and not bad, '(%s: the bound of all %d entries asks the kernel for %d table requests, distinct within each '
         'entry; the largest code range (D + 1)^forms is %d^%d = %.3e (%s, %s), below %.1e; the largest lp-norm D is %d (<= 64))%s' % (
             graph, len(set(x[0] for x in plans)), len(plans), r[2] + 1, r[1], float(r[2] + 1) ** r[1], nm, r[0], PACK_LIM, lpm,
             (': refused ' + '; '.join('%s %s D %d over %d forms' % (x[0], x[1][0], x[1][2], x[1][1]) for x in bad[:10])) if bad else ''))
    plant('PLANT-PACK-PLAN', not pack_ok(16, 16, False) and pack_ok(16, 14, False), '(a request of D 16 over 16 forms, 17^16 = %.3e, must '
          'be refused, and the control D 14 over 16 forms, 15^16 = %.3e, accepted)' % (17.0 ** 16, 15.0 ** 16))


def run_prep_stage(vg, stg):
    """VGu.N / VGc.N: one stage of m3_bar_v12's Prep (v10's, dmaxH 18) on the vertex graph's prep graph (pairs [], F = V), built from the
    first family graph it serves; stage u runs C-PREP-GRAPH against every family graph served; PREP-REP (INFO); VN: C-PREP-SAME; stage c:
    PLANT-MONO. The hand-off holds the stage's scalars."""
    stage('%s prep stage %s' % (vg, stg))
    fams = [f for f in FAMS if VG[f] == vg]
    gs = {f: family_graph(f) for f in fams}
    gp = prep_graph(gs[fams[0]])
    pr, rp = make_prep(vg, gp, (stg,))
    if stg == 'u':
        for f in fams:
            prep_same(f, gs[f], gp, pr)
    prep_rep(vg, pr, rp, stg)
    body = {'vgraph': vg, 'stage': stg, 'families': fams, 'scal': pr.scalars_out(stg)}
    if stg == 'c':
        plant_mono(pr)
        out('PREP %s N=%d stage c: V %d, F %d; nC8 %.6e nC6 %.6e farbase %.6e alpha_lo %.6e' % (
            vg, NN, gp.V, gp.F, float(pr.nC8.mid), float(pr.nC6.mid), float(pr.farbase.b), float(pr.alpha_lo)))
    else:
        out('PREP %s N=%d stage u: V %d, F %d, radii from %s, theta0 %r; rE %.6e nE %s nE4 %s' % (
            vg, NN, gp.V, gp.F, REFVG[vg][NN], rp['theta0'], float(pr.rE.mid), ['%.6e' % float(x.mid) for x in pr.nE],
            ['%.6e' % float(x.mid) for x in pr.nE4]))
    if vg == 'VN':
        prep_cross(stg, body['scal'])   # C-PREP-SAME against m3_run_v1_8's N stage
    body['fallbacks'] = fb_info()
    write_handoff(vg, body)


def prep_scalars(vg):
    """C-PREP-STAGES: the vertex graph's two prep hand-offs (each bound to its producer output) are of that vertex graph and stage and
    hold the stage's scalar names; returns both stages' scalars. m3_run_s9h_v1_1: they are the parent's (pk03's m3_run_v1_10_4 VGu.N and
    VGc.N, read by read_parent), and both name VGP2's family first, the family whose graph parent_prep_graph rebuilds."""
    su = read_parent('%su.%d' % (vg, NN), vg)
    sc = read_parent('%sc.%d' % (vg, NN), vg)
    ok = (su['vgraph'] == vg and sc['vgraph'] == vg and su['stage'] == 'u' and sc['stage'] == 'c' and set(su['scal']) == set(BAR.Prep.UK)
          and set(sc['scal']) == set(BAR.Prep.CK) and su['families'][0] == sc['families'][0] == VGP2[vg])
    gate('C-PREP-STAGES', ok, '(%s: %su.%d and %sc.%d, of %s and %s, scalars %s and %s; the parent\'s families served %s, first %s wanted)' % (
        vg, vg, NN, vg, NN, su['vgraph'], sc['vgraph'], sorted(su['scal']), sorted(sc['scal']), su['families'], VGP2[vg]))
    return dict(su['scal'], **sc['scal'])


def order_of(graph):
    """a piece family's entries in the list's order (the resumable pieces walk it)."""
    return [name_of(e) for e in entries_of(graph)]


CAPPED = 'VERDICT INCOMPLETE (CAP-STOP)'


def piece_state(graph, piece):
    """'valid' (its hand-off exists; read_handoff checks it), 'capped' (no hand-off; the output's first line names this script and item,
    and its VERDICT lines are exactly [CAPPED]) or 'missing' (no output); anything else raises ValueError."""
    item = '%sk%d.%d' % (PFX[graph], piece, NN)
    po = os.path.join(OUTD, 'm3_run_s9h_v1_1_%s.out' % item)
    ho = os.path.join(HANDD, 'm3_run_s9h_v1_1_%s.json' % item)
    if not os.path.exists(po):
        if os.path.exists(ho):
            raise ValueError('%s: a hand-off without its producer output' % item)
        return 'missing'
    if os.path.exists(ho):
        return 'valid'
    with open(po) as fh:
        lines = fh.read().split('\n')
    m = re.fullmatch(r'm3_run_s9h_v1_1 item (\S+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)', lines[0])
    if m and m.group(1) == item and m.group(3) == SELF_SHA and HO.verdict_ok(lines, CAPPED):
        return 'capped'
    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)


def resumed(state):
    return (' (this piece; %d units of the entry restored)' % len(state['vals'])) if state else ''


def family_parts(graph):
    """R1: the family's partitions, name -> (entry, factors, partition), in the list's order."""
    res = {}
    for e in entries_of(graph):
        facs = facs_of(e)
        res[name_of(e)] = (e, facs, partition_of(e, facs))
    return res


def run_nk(graph, piece):
    stage('%s keys piece %d' % (graph, piece))
    order = order_of(graph)
    g = family_graph(graph)
    scal = prep_scalars(VG[graph])   # m3_run_v1_10: the scalars of the family's vertex graph (C-PREP-STAGES)
    refs = twin_keys(graph)   # R1: the twin's rule, G, partition and qcap per key (C-PART-RULE)
    part_plants(graph, family_parts(graph))
    norm_rel_plants()   # m3_run_v1_10_2
    start, caps, partial = 0, 0, None
    for j in range(piece - 1, 0, -1):
        st = piece_state(graph, j)
        if st == 'capped':
            caps += 1
            continue
        if st != 'valid':
            raise ValueError('%sk%d.%d is %s, so piece %d cannot start' % (PFX[graph], j, NN, st, piece))
        prev = read_handoff('%sk%d.%d' % (PFX[graph], j, NN), graph)
        start, partial = prev['next'], prev['partial']
        break
    factor = 1.5 * 2 ** caps
    nin = len(partial['vals']) if partial else 0
    out('PIECE-START %s piece %d resumes at entry %d%s after %d capped piece(s); stop factor %.1f' % (
        graph, piece, start, (' with %d units of %s restored' % (nin, partial['entry'])) if partial else '', caps, factor))
    pr, rp = make_prep(VG[graph], g, (), scalars=scal)   # v10's Prep on the restored scalars
    prep_same(graph, g, parent_prep_graph(VG[graph]), pr)   # m3_run_s9h_v1_1: C-PREP-SHARE on the restored prep
    slow, units = [60.0], [0]

    def budget():
        return units[0] == 0 or cpu() + factor * slow[0] <= LIM - 20

    def akest(est):
        """m3_run_v1_10_1: budget() with the slow estimate raised to est, a key's pinned fresh a_k CPU (AKCPU)."""
        return units[0] == 0 or cpu() + factor * max(slow[0], est) <= LIM - 20

    def done(dt, progress):
        slow[0] = max(slow[0], dt)
        if progress:
            units[0] += 1
    pr.ubudget, pr.unit_done, pr.akest = budget, done, akest
    res, i, part = [], start, None
    while i < len(order):
        if i > start and not akest(AKCPU.get(order[i], 0.0)):   # with its pinned a_k estimate of the next entry
            break
        try:
            res.append(compute_entry(pr, entries_of(graph, [order[i]])[0], refs[order[i]], state=partial))
        except BAR.Checkpoint as cp:
            part = cp.state
            break
        partial = None
        pr.tables.clear()   # R1: the entry's moment tables are dropped before the next entry (memory)
        i += 1
    pr.ubudget = pr.unit_done = pr.akest = None
    nout = len(part['vals']) if part else 0
    prog = i > start or (part is not None and nout > nin)
    gate('C-PIECE', prog, '(%s piece %d: entries %d..%d of %d done, next %d; %d units computed%s)' % (
        graph, piece, start, i - 1, len(order), i, units[0], (', %d units of %s carried' % (nout, part['entry'])) if part else ''))
    write_handoff(graph, {'family': graph, 'piece': piece, 'start': start, 'next': i, 'partial': part, 'stop_factor': factor,
                          'entries': res, 'fallbacks': fb_info(), 'exempt_sha': EXSHA})


def write_records(texts, paths, fails, nofire, tag, opener=open):
    """writes asm's record texts (open 'x', inside out/, no file there yet) only when no gate has failed, every
    plant so far has fired and the TAG is certified; returns [(key, path)] written, or [] when it refuses."""
    if fails or nofire or tag != '':
        return []
    for f in paths:
        if os.path.dirname(os.path.abspath(paths[f])) != OUTD or os.path.exists(paths[f]):
            raise ValueError('record path %s: outside out/ or already there' % paths[f])
    done = []
    for f in sorted(paths):
        with opener(paths[f], 'x') as fh:
            fh.write(texts[f])
        done.append((f, paths[f]))
    return done


def walk_pieces(graph, res):
    """C-PIECES: the pieces of a family cover its entries in order, each advancing, none left in progress; their entries go into res."""
    order, nxt, piece, nin = order_of(graph), 0, 1, 0
    while nxt < len(order) and piece <= MAXP[graph]:
        st = piece_state(graph, piece)
        if st == 'missing':
            break
        if st == 'capped':
            out('PIECE-CAPPED %sk%d.%d: a clean CAP-STOP of this script, no hand-off; skipped and kept' % (PFX[graph], piece, NN))
            piece += 1
            continue
        body = read_handoff('%sk%d.%d' % (PFX[graph], piece, NN), graph)
        pt = body['partial']
        EXSEEN.add(body.get('exempt_sha'))
        nout = len(pt['vals']) if pt else 0
        okp = body['start'] == nxt and (body['next'] > nxt or nout > nin) and (pt is None or (body['next'] < len(order) and pt['entry'] == order[body['next']]))
        gate('C-PIECES', okp, '(%sk%d.%d: entries %d..%d complete%s)' % (PFX[graph], piece, NN, body['start'], body['next'] - 1,
                                                                          (', %d units of %s carried' % (nout, pt['entry'])) if pt else ''))
        for r in body['entries']:
            res[(graph, r['name'])] = r
        nxt, piece, nin = body['next'], piece + 1, nout
    gate('C-PIECES', nxt == len(order) and nin == 0, '(the %s pieces cover all %d %s entries, in order, none left in progress)' % (
        graph, len(order), graph))


def run_smoke(graph):
    """Xa, the smoke piece (m3_run_v1_10_2 l.1545-1551 lists its gates and plants): the list, partition, a_k, plant, cache, BARPOS and pack
    checks of every entry of the family; no hand-off, no record."""
    stage('smoke %s' % graph)
    list_check()
    rule_of_check()
    xh_check()
    parity_set()
    g = family_graph(graph)
    pr, rp = make_prep(VG[graph], g, ())
    prep_same(graph, g, prep_graph(g), pr)
    prep_same(graph, g, parent_prep_graph(VG[graph]), pr)   # m3_run_s9h_v1_1: C-PREP-SHARE, against the graph of the parent's prep
    prep_twin(graph)
    refs = twin_keys(graph)
    parts = family_parts(graph)
    worst, n, path, zpath, plans, akd = (0.0, '-', 0), 0, None, None, [], None
    akx = {}   # m3_run_s9h_v1_1: the smoke's a_k by key
    for e in entries_of(graph):
        name = name_of(e)
        STAGE[0] = 'smoke %s' % name
        e_, facs, p = parts[name]
        part_checks(e, facs, p, refs[name])
        tq = cpu()
        pr.qcap, qmax = qcap_of(pr, p)
        out('QCAP %s: the largest pair degree of its F_i %d; qcap %d (the float twin\'s %r); qcap_of %.2f s (the groups\' series, majorants '
            'and F_i)' % (name, qmax, pr.qcap, refs[name].get('qcap'), cpu() - tq))
        t0 = cpu()
        STAGE[0] = 'smoke a_k %s' % name
        ak, _, info = pr.bound(facs, p['grouping'], bars=False, entry=name, ak_zero=e['parity'] == 'zero')
        for k, (a, fa) in enumerate(zip(ak, refs[name]['ak'])):
            worst = max(worst, (abs(float(a.mid) - fa) / max(1.0, abs(fa)), name, k))
        akx[name] = ak   # m3_run_s9h_v1_1
        n += 1
        out('SMOKE %s ak %s Dn %d forms %d: %.2f s' % (name, ['%.12g' % float(a.mid) for a in ak], info['Dn'], len(info['forms']), cpu() - t0))
        if p['rule'] != 'std':
            STAGE[0] = 'smoke C-AK-SAME %s' % name
            akstd = ak_same(pr, name, p, ak, info, facs)
            if akd is None:
                akd = (e, facs, p, akstd)
        if path is None and e['parity'] == 'free' and any(f[0] == 'xi' and f[2] == 0.0 for f in facs):
            path = (name, facs)
        if zpath is None and e['parity'] == 'zero':
            zpath = (name, facs)
        STAGE[0] = 'smoke pack plan %s' % name
        pl = pack_plan(pr, facs, p['grouping'], info, e['parity'] == 'free')
        top = max(pl, key=lambda r: r[1] * math.log(r[2] + 1))
        out('PACK-PLAN %s: %d table requests; largest code range %d^%d (%s)' % (name, len(pl), top[2] + 1, top[1], top[0]))
        plans += [(name, r) for r in pl]
        pr.tables.clear()   # R1: the entry's tables are dropped before the next entry
    s9h_controls(akx, 'smoke %s' % graph)   # m3_run_s9h_v1_1: the controls whose keys are all in this family
    gate('C-SMOKE-AK', n == len(entries_of(graph)) and n > 0 and worst[0] <= 1e-9, '(the a_k of %d %s entries against m3ref_s9h_v1 %s: largest '
         '|certified mid - float| / max(1, |float|) %.2e at %s a_%d)' % (n, graph, FAMREF[graph], worst[0], worst[1], worst[2]))
    plant('PLANT-SMOKE-AK', not (worst[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')
    if path is not None:
        name, facs = path
        i0 = next(i for i, f in enumerate(facs) if f[0] == 'xi' and f[2] == 0.0)
        f0 = facs[i0]
        facs2 = list(facs)
        facs2[i0] = (f0[0], f0[1], f0[2], [c * (1 + 1e-6) for c in f0[3]])
        what = 'its xi factor\'s c9 times 1 + 1e-6'
    else:
        name, facs = zpath
        i0 = next(i for i, f in enumerate(facs) if parity_h(f) == 'odd')
        f0 = facs[i0]
        facs2 = list(facs)
        facs2[i0] = (f0[0], f0[1], 1e-3, list(f0[3]))
        what = 'its odd factor\'s c0 set to 1e-3'
    STAGE[0] = 'smoke plant %s' % name
    pr.qcap = qcap_of(pr, parts[name][2])[0]
    ak2, _, _ = pr.bound(facs2, 'std', bars=False, entry=name + ' (planted)')
    w2 = max(abs(float(a.mid) - fa) / max(1.0, abs(fa)) for a, fa in zip(ak2, refs[name]['ak']))
    plant('PLANT-SMOKE-PATH', not (w2 <= 1e-9), '(%s with %s: largest difference %.2e)' % (name, what, w2))
    STAGE[0] = 'smoke partition plants'
    part_plants(graph, parts)
    if akd is not None:
        pr.qcap = qcap_of(pr, akd[2])[0]
        ak_drop_plant(pr, *akd)
    gcache_check(graph, pr, parts)
    STAGE[0] = 'smoke C-BARPOS-INFO'
    barpos_info(graph, pr, parts)
    STAGE[0] = 'smoke a_k total plants'
    ak_total_plants()
    STAGE[0] = 'smoke norm rule plants'
    norm_rel_plants()   # m3_run_v1_10_2
    pack_gate(graph, plans)
    fb_info()


def rep_checks(news, res, refs):
    """C-REP-B (m3_run_v1_10_4: every part against its line, BAR.part_lines with the exempt keys out) and C-REP-AK with their plants on the
    computed free entries news [(graph, key, record item)] against the float twins."""
    rep, rak = [], []
    for graph, key, it in news:
        r, d = res[(graph, key)], refs[graph][key]
        ln = BAR.part_lines(r.get('big', []), 1.15, tuple(k.split(':', 2)[2] for k in EXEMPT if k.split(':', 2)[:2] == [graph, key]))
        for p in ('rem', 'tail', 'ann', 'far'):
            if d['B'][p] > 0:
                rep.append((it['B'][p] / d['B'][p] / ln[p], it['B'][p] / d['B'][p], ln[p], key, p))
        for k, (a, fa) in enumerate(zip(r['ak'], d['ak'])):
            rak.append((abs(float(a.mid) - fa) / max(1.0, abs(fa)), key, k))
    w, lo_ = max(rep), min(rep, key=lambda x: x[1])
    gate('C-REP-B', all(BAR.part_ok(x[1], x[2]) for x in rep), '(%d bar parts against m3ref_s9h_v1 z9sym, each on the entry\'s own partition '
         'and against its line, 1.15 x its non-exempt big-rule factors: ratio/line at most %.6f (%s %s, line %.6f); smallest ratio %.9f (%s %s))' % (
             len(rep), w[0], w[3], w[4], w[2], lo_[1], lo_[3], lo_[4]))
    plant('PLANT-REPB', not BAR.part_ok(lo_[1] * 0.5, lo_[2]), '(the smallest ratio times 0.5)')
    wr = max(rak)
    gate('C-REP-AK', wr[0] <= 1e-9, '(%d a_k against m3ref_s9h_v1 z9sym: largest |certified mid - float| / max(1, |float|) %.2e at %s a_%d)' % (
        len(rak), wr[0], wr[1], wr[2]))
    plant('PLANT-REPAK', not (wr[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')


def part_rec_ok(field, graph, refs_g):
    """C-PART-REC's test of one record's partition field: exactly the graph's list keys, each with RULE_OF's rule, the groups part_enc
    recomputes from the list's encodings, G = len(groups), the float twin's KEYJSON partition and an int qcap >= 6."""
    want = set(e['key'] for e in LIST['entries'] if e['graph'] == graph)
    if set(field) != want:
        return False
    for k, v in field.items():
        e = entries_of(graph, [k])[0]
        q = v.get('qcap')
        if (v.get('rule') != RULE_OF[k] or v.get('groups') != part_enc(RULE_OF[k], e['factors']) or v.get('G') != len(v.get('groups') or [])
                or refs_g[k].get('partition') != v.get('groups') or isinstance(q, bool) or not isinstance(q, int) or q < 6):
            return False
    return True


def zflip(res):
    """C-ZFLIP and PLANT-ZFLIP (row 3: IhZb = -IhZ exactly; m3_run_v1_10_2 l.1669-1671 gives the argument)."""
    fa, fb = facs_of(entries_of('NIT', ['IhZ'])[0]), facs_of(entries_of('NIB', ['IhZb'])[0])
    En, Eb = GR.strip(LIST['graphs']['NIT']['columns'])[1], GR.strip(LIST['graphs']['NIB']['columns'])[1]
    ca, cb = [f for f in fa if is_column(f)], [f for f in fb if is_column(f)]
    ha, hb = [f for f in fa if not is_column(f)], [f for f in fb if not is_column(f)]
    cls = [parity_h(f) for f in ca]
    img = lambda f: (frozenset(frozenset((ENT.sigma(u), ENT.sigma(v))) for u, v in ENT.pairs_of(f)), f[2], tuple(f[3]))
    key = lambda f: (frozenset(frozenset(p) for p in ENT.pairs_of(f)), f[2], tuple(f[3]))
    e1 = [1.0] + [0.0] * 8
    pre = (En == Eb and ENT.edges_map_onto(En, ENT.sigma) and ca == cb and None not in cls and cls.count('odd') == 1 and len(ha) == 1
           and len(hb) == 1 and ha[0][0] == hb[0][0] == 'xi' and list(ha[0][3]) == e1 and list(hb[0][3]) == e1 and img(ha[0]) == key(hb[0]))
    a, b = res[('NIT', 'IhZ')]['ak'], res[('NIB', 'IhZb')]['ak']
    ov = [meets(y, -x) for x, y in zip(a, b)]
    gate('C-ZFLIP', pre and len(a) == len(b) and all(ov), '(T <-> B: couplings equal and fixed, column factors %s, bond %s -> %s: %s; IhZb a_k '
         '%s against -IhZ a_k %s: overlap %s)' % (cls, sorted(ENT.pairs_of(ha[0])) if ha else '-', sorted(ENT.pairs_of(hb[0])) if hb else '-', pre,
                                                  ['%.12g' % float(y.mid) for y in b], ['%.12g' % -float(x.mid) for x in a], ov))
    ov2 = [meets(y, x) for x, y in zip(a, b)]
    plant('PLANT-ZFLIP', not all(ov2), '(IhZb against +IhZ: overlap %s)' % ov2)


def s9h_controls(akd, where):
    """m3_run_s9h_v1_1, in place of the parent's C-ZFLIP: exact relations between this list's certified a_k and with the S9 record (G5_PLAN_v1
    sect. 4), each control run when all its keys are in akd (key -> a_k balls: a smoke's family, or every key at asm), each with a plant
    that must fail; balls are compared by meets.
    C-H0: the a_0 balls of Ih,0, IhTh,0 and Gxh,0,0 meet h_0 = (N - 1)(1 - 2/sqrt 21)/2, the bond's harmonic amplitude between vacuum states
    (kt_s9b_v2's float Ih,0 matches it); PLANT-ROW: the S9 record's Iht,0 (the bond on the T row) must miss h_0.
    C-IHT0: IhTh,0 = Ih,0: the reflection of [vac, int, vac] (columns 0 <-> 2) maps NHT's couplings onto NIH's, [cp 0 0] onto [cp 0 2] and
    the M bond (1, 4) onto (7, 4); PLANT-IHT0: Ih,1 in place of Ih,0 must miss.
    C-GXSYM: GxhR,1,0 = Gxh,0,1: the column swap of DH maps the M bond (1, 4) onto itself and [cp 1 0][cp 0 1] onto [cp 1 1][cp 0 0];
    PLANT-GXSYM: Gxh,0,3 in place of Gxh,0,1 must miss.
    C-HX0: Ih,1's a_0 ball lies in [-1e-9, 1e-9]: the h source has no harmonic amplitude between states 0 and 1, up to the trial states'
    binary64 coefficients (for the same reason the S9 record's certified G,0,1 a_0 ball does not hold 0); PLANT-HX0: Ih,0's a_0 must fail.
    C-G00-S9: G,0,0 on DH = the S9 record's G,0,0 (S8 D's g,0,0 on D's graph, read by m3_reader_v6_3.load with the asm output that wrote it,
    both pinned): every a_k ball meets the record's [ak - ak_rad, ak + ak_rad]; PLANT-G00-S9: the record's G,0,1 in place must miss."""
    s9 = RDR.load(os.path.join(OUTD_IN, 'm3_s9_N%d_J300_v1_8_3.json' % NN), os.path.join(OUTD_IN, 'm3_run_v1_8_3_asm9.%d.out' % NN), 300, NN)
    sb = lambda k: [iv.mpf([S.I(lo).a, S.I(hi).b]) for lo, hi in zip(s9['balls'][k][0], s9['balls'][k][1])]
    allm = lambda x, y: len(x) == len(y) == 4 and all(meets(a, b) for a, b in zip(x, y))
    ovl = lambda x, y: [meets(a, b) for a, b in zip(x, y)]
    have = lambda *ks: all(k in akd for k in ks)
    h0 = iv.mpf(NN - 1) * (1 - 2 / iv.sqrt(21)) / 2
    ks = [k for k in ('Ih,0', 'IhTh,0', 'Gxh,0,0') if k in akd]
    if ks:
        gate('C-H0', all(meets(akd[k][0], h0) for k in ks), '(%s: the a_0 balls of %s against h_0 = (N - 1)(1 - 2/sqrt 21)/2 = %s: meet %s)' % (
            where, ks, h0, [meets(akd[k][0], h0) for k in ks]))
        plant('PLANT-ROW', not meets(sb('Iht,0')[0], h0), '(%s: the S9 record\'s Iht,0, the bond on the T row, a_0 %s against h_0)' % (
            where, sb('Iht,0')[0]))
    if have('Ih,0', 'IhTh,0', 'Ih,1'):
        gate('C-IHT0', allm(akd['IhTh,0'], akd['Ih,0']), '(%s: IhTh,0 against Ih,0, the reflection: meet %s)' % (
            where, ovl(akd['IhTh,0'], akd['Ih,0'])))
        plant('PLANT-IHT0', not allm(akd['IhTh,0'], akd['Ih,1']), '(%s: IhTh,0 against Ih,1: meet %s)' % (where, ovl(akd['IhTh,0'], akd['Ih,1'])))
    if have('GxhR,1,0', 'Gxh,0,1', 'Gxh,0,3'):
        gate('C-GXSYM', allm(akd['GxhR,1,0'], akd['Gxh,0,1']), '(%s: GxhR,1,0 against Gxh,0,1, the column swap: meet %s)' % (
            where, ovl(akd['GxhR,1,0'], akd['Gxh,0,1'])))
        plant('PLANT-GXSYM', not allm(akd['GxhR,1,0'], akd['Gxh,0,3']), '(%s: GxhR,1,0 against Gxh,0,3: meet %s)' % (
            where, ovl(akd['GxhR,1,0'], akd['Gxh,0,3'])))
    if have('Ih,1', 'Ih,0'):
        tol = iv.mpf(['-1e-9', '1e-9'])
        inside = lambda x: tol.a <= x.a and x.b <= tol.b
        gate('C-HX0', inside(akd['Ih,1'][0]), '(%s: Ih,1\'s a_0 ball %s inside %s)' % (where, akd['Ih,1'][0], tol))
        plant('PLANT-HX0', not inside(akd['Ih,0'][0]), '(%s: Ih,0\'s a_0 ball %s inside %s)' % (where, akd['Ih,0'][0], tol))
    if have('G,0,0'):
        gate('C-G00-S9', allm(akd['G,0,0'], sb('G,0,0')), '(%s: G,0,0 on DH against the S9 record %s G,0,0: meet %s)' % (
            where, s9['name'], ovl(akd['G,0,0'], sb('G,0,0'))))
        plant('PLANT-G00-S9', not allm(akd['G,0,0'], sb('G,0,1')), '(%s: G,0,0 on DH against the record\'s G,0,1: meet %s)' % (
            where, ovl(akd['G,0,0'], sb('G,0,1'))))


def reader_plants(text, name, ztext):
    """the reader plants on the DH record's text through m3_reader_v6_3 (_check_text, the writer's parse; loads, the bound entry point),
    with the layer plants of the v1_4_1 pin, then C-BOUND-RT with the bound-load plants; PLANT-PARZERO on a copy of the same text with a
    free item marked parity zero (m3_run_s9h_v1_1: the S9H records have no parity zero)."""
    dd = json.loads(text)
    k0 = sorted(k for k in dd['items'] if dd['items'][k]['parity'] == 'free')[0]
    dd['items'][k0]['B'].pop('rnd')
    try:
        RDR._check_text(json.dumps(dd), 300, NN)
        plant('PLANT-FMT', False, '(DH copy without one rnd)')
    except ValueError:
        plant('PLANT-FMT', True, '(DH copy without one rnd)')
    dd2 = json.loads(text)
    kr = max((k for k in dd2['items'] if dd2['items'][k]['parity'] == 'free'), key=lambda k: sum(dd2['items'][k]['ak_rad']))
    dd2['items'][kr]['B']['rnd'] = 0.0
    try:
        RDR._check_text(json.dumps(dd2), 300, NN)
        plant('PLANT-RND', False, '(DH copy with %s rnd = 0)' % kr)
    except ValueError:
        plant('PLANT-RND', sum(dd2['items'][kr]['ak_rad']) > 0, '(DH copy with %s rnd = 0; its ak_rad sum %.1e)' % (kr, sum(dd2['items'][kr]['ak_rad'])))
    deny = dict(DENY)
    nx = 3 if NN == 4 else 4
    for lab, mut, jref, nexp in (('PLANT-READER-PRECERT', 'precert', 300, NN), ('PLANT-READER-KERNEL', 'kernel', 300, NN),
                                 ('PLANT-READER-PREC', 'prec', 300, NN), ('PLANT-LAYER-V1_1', 'arbeng_ma_v1_1.py', 300, NN),
                                 ('PLANT-LAYER-V1_2', 'arbeng_ma_v1_2.py', 300, NN), ('PLANT-LAYER-V1_4', 'arbeng_ma_v1_4.py', 300, NN),
                                 ('PLANT-READER-MOCK', 'mock_arbeng_v1_4.py', 300, NN), ('PLANT-LAYER-MIX', 'mix', 300, NN),
                                 ('PLANT-VALREC', 'valrec', 300, NN), ('PLANT-CLAIM', 'claim', 300, NN), ('PLANT-ARBK', 'arbk', 300, NN),
                                 ('PLANT-ARBB', 'arbb', 300, NN), ('PLANT-JREF', None, 150, NN), ('PLANT-N', None, 300, nx),
                                 ('PLANT-KIND', 'kind', 300, NN), ('PLANT-CLAIM-BALL', 'claimball', 300, NN),
                                 ('PLANT-CLAIM-BALL-MISSING', 'noclaimball', 300, NN)):
        dd3 = json.loads(text)
        if mut == 'precert':
            dd3['format'] = 'M3_RECORD_v1_PRECERT'
            dd3['claim'] = 'NOT CERTIFIED (PRECERT): ' + dd3['claim']
        elif mut == 'kernel':
            dd3['kernel_sha256'] = flip(dd3['kernel_sha256'])
        elif mut == 'prec':
            dd3['kernel_prec'] = 256
        elif mut in deny:
            dd3['kernel_file'], dd3['kernel_sha256'] = mut, deny[mut]
        elif mut == 'mix':
            dd3['kernel_file'], dd3['kernel_sha256'] = 'arbeng_ma_v1_3.py', '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be'
        elif mut == 'valrec':
            dd3['validation'] = dd3['validation'][:-1] + [flip(dd3['validation'][-1])]
        elif mut == 'claim':
            dd3['claim'] = dd3['claim'] + ' '
        elif mut == 'arbk':
            dd3['arb_kernel_sha256'] = flip(dd3['arb_kernel_sha256'])
        elif mut == 'arbb':
            dd3['arb_base_sha256'] = flip(dd3['arb_base_sha256'])
        elif mut == 'kind':
            dd3['items'][sorted(dd3['items'])[0]].pop('kind')
        elif mut == 'claimball':
            dd3['claim_ball'] = dd3['claim_ball'] + ' '
        elif mut == 'noclaimball':
            dd3.pop('claim_ball')
        what = mut or ('expected J_REF %d' % jref if jref != 300 else 'expected N %d' % nexp)
        try:
            RDR._check_text(json.dumps(dd3), jref, nexp)
            plant(lab, False, '(m3_reader_v6_3 must refuse the mutated DH copy: %s)' % what)
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3 refuses the mutated DH copy: %s)' % what)
    dz = json.loads(ztext)
    kz = sorted(k for k in dz['items'] if dz['items'][k]['parity'] == 'free')[0]   # m3_run_s9h_v1_1: no parity zero in the S9H records
    dz['items'][kz]['parity'] = 'zero'   # m3_run_s9h_v1_1: a free item marked zero (its a_k are not zero)
    try:
        RDR._check_text(json.dumps(dz), 300, NN)
        plant('PLANT-PARZERO', False, '(m3_reader_v6_3 must refuse the DH copy with the free item %s marked parity zero)' % kz)
    except ValueError:
        plant('PLANT-PARZERO', True, '(m3_reader_v6_3 refuses the DH copy with the free item %s marked parity zero)' % kz)
    dh = tsha(text)
    try:
        RDR.loads(text, 'RECORD %s %s\nVERDICT VALID\n' % (name, dh), 300, NN, name)
        gate('C-BOUND-RT', True, '(m3_reader_v6_3.loads accepts the DH text under an output that names it and ends VALID)')
    except ValueError as ex:
        gate('C-BOUND-RT', False, '(refused: %s)' % ex)
    for lab, otext in (('PLANT-BOUND-VERDICT', 'RECORD %s %s\nVERDICT VALID-PRECERT\n' % (name, dh)),
                       ('PLANT-BOUND-INVALID', 'RECORD %s %s\nVERDICT INVALID (C-REP-B)\n' % (name, dh)),
                       ('PLANT-BOUND-TWO', 'RECORD %s %s\nVERDICT VALID\nVERDICT VALID\n' % (name, dh)),
                       ('PLANT-BOUND-SHA', 'RECORD %s %s\nVERDICT VALID\n' % (name, flip(dh))),
                       ('PLANT-BOUND-NONE', 'VERDICT VALID\n')):
        try:
            RDR.loads(text, otext, 300, NN, name)
            plant(lab, False, '(m3_reader_v6_3.loads must refuse this asm output)')
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3.loads refuses this asm output)')


def resume_chain():
    """C-RESUME-CHAIN: Xr1 and Xr2 of every family in RESUME_FAMS are valid, each with resume_ok, and Xr1 with plant_fired."""
    ok, why = True, []
    for graph in RESUME_FAMS:
        b1 = read_handoff('%sr1.%d' % (PFX[graph], NN), graph)
        b2 = read_handoff('%sr2.%d' % (PFX[graph], NN), graph)
        ok = ok and b1['resume_ok'] is True and b1['plant_fired'] is True and b2['resume_ok'] is True and b1['entry'] == b2['entry'] == RESUME_KEY[graph]
        why.append('%s on %s: part 1 cut %s resumed %s, PLANT-RESUME %s; part 2 cut after %d of %d units resumed %s' % (
            graph, b1['entry'], b1['cut'], 'identical' if b1['resume_ok'] else 'DIFFERENT', 'FIRES' if b1['plant_fired'] else 'DOES NOT FIRE',
            b2['cut'], b2['units'], 'identical' if b2['resume_ok'] else 'DIFFERENT'))
    gate('C-RESUME-CHAIN', ok, '(%s)' % '; '.join(why))


def run_resume(graph, part):
    """Xr1 / Xr2: C-RESUME on RESUME_KEY[graph] after the entry pieces, against the record's entry (walk_pieces), on v10's Prep with the
    vertex graph's scalars, under the entry's partition and qcap. Part 1: the checkpoint after stage a (units ak, m0u, m0c), through a
    hand-off round trip, resumed with fresh caches, must give the record's a_k and bars exactly (C-RESUME); PLANT-RESUME: m0u doubled must
    change the bars. Part 2: a straight run (C-RESUME-SAME), then the checkpoint before the first stage-c unit, resumed the same way."""
    stage('%s resume part %d' % (graph, part))
    if graph not in RESUME_FAMS:
        raise ValueError('%s is not in RESUME_FAMS %s' % (graph, RESUME_FAMS))
    res = {}
    walk_pieces(graph, res)
    scal = prep_scalars(VG[graph])
    g = family_graph(graph)
    pr, rp = make_prep(VG[graph], g, (), scalars=scal)
    e = entries_of(graph, [RESUME_KEY[graph]])[0]
    name = name_of(e)
    src = res[(graph, name)]
    facs = facs_of(e)
    p = partition_of(e, facs)
    gr = p['grouping']
    pr.qcap = qcap_of(pr, p)[0]
    pr.declare_big(p['groups'], p['scal'], *RULE_A[graph])   # m3_run_v1_10_4: the production entry's declared big set

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
    body = {'family': graph, 'part': part, 'entry': name}
    if part == 1:
        t0 = cpu()
        _, st = run(cut=3)
        keys = list(st['vals']) if st else []
        r1, _ = run(state=st) if st else (None, None)
        ok = keys == ['ak', 'm0u', 'm0c'] and r1 is not None and same(src['ak'], r1[0]) and same(src['bars'], r1[1])
        gate('C-RESUME', ok, '(%s part 1: cut after stage a, units %s, resumed with fresh caches: a_k and bars %s the record\'s; %.2f s)' % (
            name, keys, 'identical to' if ok else 'NOT identical to', cpu() - t0))
        r2 = None
        if st:
            bad = dict(st, vals=dict(st['vals']))
            bad['vals']['m0u'] = 2 * bad['vals']['m0u']
            r2, _ = run(state=bad)
        fired = r2 is not None and not same(src['bars'], r2[1])
        plant('PLANT-RESUME', fired, '(%s: the stage-a state with m0u doubled must change the bars; rem %s -> %s)' % (
            name, '%.9e' % S.up(src['bars']['rem']), ('%.9e' % S.up(r2[1]['rem'])) if r2 else 'no result'))
        body.update({'cut': keys, 'resume_ok': ok, 'plant_fired': fired})
    else:
        t0 = cpu()
        (ak0, b0, _), _ = run()
        seq = list(pr.ustate['vals'])
        oks = same(src['ak'], ak0) and same(src['bars'], b0)
        gate('C-RESUME-SAME', oks, '(%s straight, %d units, %.2f s: a_k and bars %s the record\'s)' % (
            name, len(seq), cpu() - t0, 'identical to' if oks else 'NOT identical to'))
        cutb = next(i for i, k in enumerate(seq) if k.endswith('|c'))
        t0 = cpu()
        _, st = run(cut=cutb)
        r3, _ = run(state=st) if st else (None, None)
        ok = st is not None and len(st['vals']) == cutb and r3 is not None and same(src['ak'], r3[0]) and same(src['bars'], r3[1])
        gate('C-RESUME', ok, '(%s part 2: cut after %d of %d units, before the first stage-c unit, resumed with fresh caches: a_k and bars %s '
             'the record\'s; %.2f s)' % (name, cutb, len(seq), 'identical to' if ok else 'NOT identical to', cpu() - t0))
        body.update({'cut': cutb, 'units': len(seq), 'resume_ok': ok and oks})
    pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0
    body['fallbacks'] = fb_info()
    write_handoff(graph, body)


def run_asm():
    stage('asm')
    list_check()
    rule_of_check()
    parity_set()
    res = {}
    for graph in FAMS:
        walk_pieces(graph, res)
    gate('C-EXEMPT-SAME', EXSEEN == {EXSHA}, '(every entry piece ran with the exemption %s: %s)' % (EXSHA, sorted(map(str, EXSEEN))))
    out("C-RESUME-INFO (no resume family here: the parent's NTBr1 and NTBr2 checked the checkpoint code, which C-CORE pins)")   # m3_run_s9h_v1_1
    scals = {vg: prep_scalars(vg) for vg in ('VN', 'VD')}   # C-PREP-STAGES: the hand-offs the records name
    refs = {}
    for graph in FAMS:
        prep_twin(graph)
        refs[graph] = {}
        fl = ref_files(graph)
        for i, p in enumerate(fl):
            with open(p) as fh:
                lines = fh.read().split('\n')
            vl = [ln for ln in lines if ln.startswith('VERDICT')]
            okv = (vl == ['VERDICT VALID'] or (i < len(fl) - 1 and vl == [CAPPED])) and [ln for ln in lines if ln.startswith('TRIAL')] == ['TRIAL z9sym']
            gate('C-HASH-REF', okv, '(%s, sha256 %s, piece %d of %d: VERDICT lines %r (exactly [VERDICT VALID]; a clean CAP-STOP only before the '
                 'last piece), TRIAL lines exactly [TRIAL z9sym])' % (os.path.basename(p), sha(p), i + 1, len(fl), vl))
            for d in read_lines(p, 'KEYJSON'):
                refs[graph][d['key']] = d
        gate('C-REF-KEYS', sorted(k for k in refs[graph] if k not in WITHDRAWN) == sorted(order_of(graph)), '(%s: the float twin\'s KEYJSON keys %s, '
             'but the withdrawn %s, equal the family\'s entries)' % (graph, sorted(refs[graph]), sorted(k for k in refs[graph] if k in WITHDRAWN)))
    files, news, pz = {g: {} for g in FAMS}, [], []
    pfield = {g: {} for g in FAMS}
    for e in V3:
        r = res[(e['graph'], name_of(e))]
        pfield[e['graph']][name_of(e)] = {'rule': r['rule'], 'G': r['G'], 'groups': r['groups'], 'qcap': r['qcap']}
        if e['parity'] == 'zero':
            if r['parity'] != 'zero':
                raise ValueError('%s: marked zero, computed %s' % (name_of(e), r['parity']))
            files[e['graph']][name_of(e)] = REC.entry_record(None, None, T_REF, 'zero')
            pz.append(name_of(e))
            continue
        it = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=r['a0_exact'], laws=r['laws'])
        files[e['graph']][name_of(e)] = it
        news.append((e['graph'], name_of(e), it))
    out('PARITY-ZERO %s: written as exact zeros with parity zero (C-ODD and C-ODD-AK in their pieces)' % pz)
    want = {g: set(e['key'] for e in LIST['entries'] if e['graph'] == g) for g in FAMS}
    gate('C-SCOPE', all(set(files[g]) == want[g] for g in FAMS), '(the three records hold exactly the list\'s keys of their graphs: %s)' % (
        ', '.join('%s %d' % (g, len(files[g])) for g in FAMS)))
    plant('PLANT-SCOPE', not (set(list(files['DH'])[1:]) == want['DH']), '(DH without one key)')   # m3_run_s9h_v1_1
    gate('C-PART-REC', all(part_rec_ok(pfield[g], g, refs[g]) for g in FAMS), '(the partition fields of the three records: every key with '
         'RULE_OF\'s rule, the groups recomputed from the list\'s encodings, G = len(groups), the float twin\'s partition, qcap >= 6: %s)' % (
             ', '.join('%s %s' % (g, part_rec_ok(pfield[g], g, refs[g])) for g in FAMS)))
    kx = next(k for k, v in pfield['DH'].items() if v['G'] >= 2)   # m3_run_s9h_v1_1: DH
    badf = dict(pfield['DH'])
    badf[kx] = dict(badf[kx], groups=[badf[kx]['groups'][1], badf[kx]['groups'][0]] + badf[kx]['groups'][2:])
    plant('PLANT-PART-REC', not part_rec_ok(badf, 'DH', refs['DH']), '(DH\'s field with %s\'s groups 0 and 1 swapped)' % kx)
    rep_checks(news, res, refs)
    s9h_controls({name_of(e): res[(e['graph'], name_of(e))]['ak'] for e in V3}, 'asm')   # m3_run_s9h_v1_1: in place of C-ZFLIP
    # the texts, C-FMT, the plants, and only then the write
    tag = TAG
    eng = {'m3_run_s9h_v1_1': SELF_SHA, 'parent': 'm3_run_v1_10_4.py:%s' % PARENT_SHA, 'modules': dict(OWNMOD)}   # m3_run_s9h_v1_1
    kern = {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}
    radii = lambda d: {k: d[k] for k in ('a_v', 'ap', 'theta0')}
    texts, paths = {}, {}
    for g in FAMS:
        vg = VG[g]
        hs = {s: 'm3_run_v1_10_4_%s%s.%d.json' % (vg, s, NN) for s in ('u', 'c')}
        prep = {'vgraph': vg, 'radii_from': '%s:%s' % (REFVG[vg][NN], INPUTS[(OUTD_IN, REFVG[vg][NN])]),
                'stages': {s: '%s:%s' % (h, sha(os.path.join(HANDD_IN, h))) for s, h in hs.items()}, 'dmaxH': 18,
                'producer': 'm3_run_v1_10_4.py:%s' % PARENT_SHA, 'graph_of': VGP2[vg]}   # m3_run_s9h_v1_1: the parent's prep stages
        extra = {'entry_list': 'S9H_RUN_LIST_v1_1.json:%s' % INPUTS[(MYD, 'S9H_RUN_LIST_v1_1.json')], 'graph': g, 'dmaxH': 18, 'claim_ball': CLAIM_BALL,
                 'prep': prep, 'partition': pfield[g]}
        top = REC.top_level(NN, 300, {g: radii(ref_prep_vg(vg))}, TRIAL, eng, tag, kern, extra=extra)
        texts[g] = json.dumps(dict(top, items=files[g]))
        paths[g] = os.path.join(OUTD, 'm3_s9h_%s_N%d_J300%s_v1.json' % (g, NN, tag))   # m3_run_s9h_v1_1
        rd = RDR._check_text(texts[g], 300, NN, name=os.path.basename(paths[g]))
        okf = (all(rd['entries'][k] == (files[g][k]['ak'], files[g][k]['err']) for k in files[g]) and set(rd['entries']) == set(files[g])
               and rd['top'].get('partition') == pfield[g])
        gate('C-FMT', okf, '(%s: %d keys read back exactly from the text by m3_reader_v6_3, the partition field with them; %d bytes; sha256 %s)' % (
            os.path.basename(paths[g]), len(files[g]), len(texts[g]), tsha(texts[g])))
    reader_plants(texts['DH'], os.path.basename(paths['DH']), texts['DH'])   # m3_run_s9h_v1_1
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
    for b, path in written:
        gate('C-WRITE', sha(path) == tsha(texts[b]), '(%s holds exactly its C-FMT text)' % os.path.basename(path))
        out('RECORD %s %s' % (os.path.basename(path), sha(path)))


try:
    if FAM == 'asm':
        run_asm()
    else:
        m_ = re.fullmatch(r'(NIH|NHT|DH)(a|k)([0-9]*)', FAM)   # m3_run_s9h_v1_1: smoke and entry pieces only
        if m_.group(2) == 'a':
            run_smoke(m_.group(1))
        else:
            run_nk(m_.group(1), int(m_.group(3)))
    finish()
except SystemExit:
    raise
except BaseException:
    out('EXCEPTION in stage %s:' % STAGE[0])
    for ln in traceback.format_exc().rstrip().split('\n'):
        out('  ' + ln)
    out('VERDICT INVALID (EXCEPTION)')
    sys.exit(1)
