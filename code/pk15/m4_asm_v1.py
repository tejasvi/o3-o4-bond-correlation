#!/usr/bin/env python3
"""m4_asm_v1.py -- pk15 (code/pk15/). The evaluator of SPEC_M4_LAW_v1_3 (ff0e5e98): reads the pinned inputs (a)-(f) of the spec's
sect. 1, computes the law's parameters (sect. 2), runs the checks of sect. 5 and writes the record M4_KV_v1 (sect. 4), only if every check
passes, through m4_reader_v1's own parse and check (the reader is executed from its pinned bytes).
Inputs (PIN_GROUPS, each file pinned by full sha256; C-HASH reads every file once and checks its sha256 at every use; the record's PIN
lines list the groups):
  (a) PIN_KTCERT: kt_cert_v1_8.py, its run manifest (every entry checked, and equal to the pins it shares), the g records of t, am, e1,
      e3 and the c, tX0, tX1, tX2, tB records of t, e1, e3, at N = 4 and 3; the trade scan's outputs (C-SCAN-PIN: their pins equal
      kt_cert_v1_8's FIXREFS entries, l.273-280, exact text);
  (b) PIN_X: the x records (one EXPLICIT data line each, 'EXPLICIT N=%d %-3s: m0 ...': m_gj), tied to kt_cert_v1_8 by C-X-TIE;
  (c) PIN_M2B: M2B_KV_v1 through m2b_reader_v1.load(record, asm output, its sha256, the reader's sha256), eps_r(300) =
      law_v1(rec, N, 300)['eps_r']; the asm output's C-MHAT lines;
  (d) PIN_M3_S9: the S9 Ritz records through m3_reader_v4_4.load(path, asm output, 300, N) and entry_ball (G,0,0 for t and am, G,1,1
      for e1, G,3,3 for e3: Z_min), with their trial_set equal to the pinned ts and vacres files; PIN_M3_VAC: the vacuum records through
      m3_reader_v5.load(path, asm output, 150, N) and entry_ball(rec, 'G4R_r');
  (e) PIN_TRIAL: the z9sym trial files (supF_a's q_i and S);
  (f) PIN_FAR: FAR_CRUDE_v1 per N through far_crude_reader_v1.load(path, out_path, expected_sha256, N) (FAR_CRUDE below; SPEC sect. 8).
Checks (sect. 5; one line each, '-> PASS' or '-> FAIL'): C-HASH; C-KTCERT-SRC (kt_cert_v1_8's lines defining RHO_M, RHO_E, DELTA, a_m,
a_e, LAM_T and kappa_B equal the ones this law's constants copy, line by line); C-REC (each record's first-line tokens, FORMAT and VERDICT
by exact equality, the LAWBASE allow-list, one RESULT line, the EXPLICIT value counts); C-X-TIE (the x records' producers are kt_cert_v1_8's
PRODUCERS, l.2169, and each g record's HANDOFF-READ x line names the x record and its HANDOFF sha256); C-SCAN-PIN; C-LAW300-NEAR (every
C-NPK, C-NDK and C-TAILM line reads PASS, at least one per record); C-MHAT; C-S9-TRIAL; C-FAR-W; C-MONO (the Chernoff rates here; the
reader's c_mono on the record values); C-COPY (the written record parsed back: every copied key equals its source token re-read from the
pinned file, by exact string equality); C-LAW300 (hard: Q_lo (1 - 1e-4) <= L_k(300) <= Q_hi (1 + 0.03), Q the RESULT ball; each ratio printed
beside its expected value); C-LAW-SCAN (hard: L_k(J) D_k >= near_k^float(J) (1 - 1e-6) at J = 400, 500, 600, against the scan's JTERMS2
near); C-BUDGET (INFO, FLOAT: L_k(J) D_k over the scan's float near at J = 300, 400, 500, 600, and the A_t + A_am tally with the Z_min
costs against 2.7% (N4) and 3.0% (N3)).
Plants (each must fire): PLANT-SWAP, PLANT-ORDER, PLANT-SCAN, PLANT-MONO-KAPPA, PLANT-MONO-FAR, PLANT-MOCK, PLANT-PRECERT,
PLANT-VERDICT, PLANT-PIN, PLANT-LAWBASE-DUP, PLANT-LAWBASE-MISS, PLANT-EXPLICIT, PLANT-NEAR, PLANT-S9-TRIAL, PLANT-X-TIE, PLANT-FAR-W,
PLANT-Z-A0 (an entry claiming a0_exact "1" with a radius on a_0) and PLANT-Z-MID (an entry without a0_exact: the constant term must be LO_0,
not the midpoint).
C-Z-A0: Z_min's constant term is each S9 entry's LO_0 = ak_0 - ak_rad_0 (entry_ball, checked against the raw item);
it is a_0 itself only where a0_exact is "1" (G,0,0), which needs a_0 = 1 with radius 0. C-COPY also recomputes ZR (entry_ball), RATIO_MAIN,
ZMIN and SUPF and compares their strings.
Modes: 'cert' writes pk15/M4_KV_v1.txt; 'mock <pinned mock far kv>' takes the far items from a MOCK file (everything else as in cert,
the S9 records included) and writes pk15/mocks/out/M4_KV_v1_MOCK_<this file's name>.txt with FORMAT 'M4_KV_v1 MOCK' and the claim prefix 'MOCK ' (the
reader checks it with those two values swapped in; a value containing 'certified' in any case is refused). Neither overwrites a record.
Run (own folder): D=/mnt/g2/release/root/code/pk15; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/m4_asm_v1.py cert > $D/out/out_m4_asm_v1.out 2> $D/out/out_m4_asm_v1.err
"""
import sys, os, re, hashlib, json, time, types
from fractions import Fraction
from flint import arb, arb_mat, ctx

ctx.prec = 256
CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk15'
READER, READER_SHA = 'pk15/m4_reader_v1.py', '5cef440ae313eddd2e6bcf49aac835f2595e61b6a3e59b23fca0c15671ec6bcd'
PIN_GROUPS = {
    'PIN_KTCERT': {
        'pk02/kt_cert_v1_8.py': '2bd634d64511bf083a2104be0bdcffc7138a28a65125e4b50886245b5e2336f2',
        'pk02/MANIFEST_KT_CERT_v1_8_RUN.sha256': '3a94e240f01e831c180ab57a8508b3d9c7b0fea6ee7dbb51d6767a9e583df776',
        'pk02/out_kt_cert_v1_8_g.tn4.out': '58383b2280a046702385ff787358216214816cb91fb099e11e89c74be3a5b392',
        'pk02/out_kt_cert_v1_8_g.tn3.out': '4c029fa27519b78e20cecf869506f908055c4896ef7f046f228260e7c3461078',
        'pk02/out_kt_cert_v1_8_g.amn4.out': '66ffa2fa3169b0bce83d2388982c074232da0aa61d94322faab5bac2c87da7fd',
        'pk02/out_kt_cert_v1_8_g.amn3.out': '3aba707a3a4e1e2c99b5776c54e5d3cf114534e6363af5cb5eb4a130d24d61b7',
        'pk02/out_kt_cert_v1_8_g.e1n4.out': '121618dfc020678995a4d5f845504e1bd054a275af9ec257b28dc5e9c597e9c9',
        'pk02/out_kt_cert_v1_8_g.e1n3.out': 'a5eadde0a3c51b2f477aad55ecf0029607baf7487f5ed65cdbe152a69c913475',
        'pk02/out_kt_cert_v1_8_g.e3n4.out': 'bd071e8bcc0544a6a23abbac570b694de217210e7c3f8711a3cdcac5819c65b1',
        'pk02/out_kt_cert_v1_8_g.e3n3.out': '99ce07c7a930e4b130e4e083d814c9ea3657bdd64884a282bbe7c08c72dc7873',
        'pk02/out_kt_cert_v1_8_c.tn4.out': '295bd8435af458130a1e9c35ed6446a66987d55a16eecfbd3d7614576741a73e',
        'pk02/out_kt_cert_v1_8_c.tn3.out': '8abb8068a45ef8c2ecab7b62ecc5435b2c0c573340e72cb2655c5b0eb9108a28',
        'pk02/out_kt_cert_v1_8_c.e1n4.out': 'c3f0b0bde26a7f42b5bc0818da5f8e2e3f25e2955133dfdb88c30a3a65c43ad4',
        'pk02/out_kt_cert_v1_8_c.e1n3.out': '2d0359969b5431a55017fac9bd03907fd42e0f7f24fcff1cc25ae972bf96f4a0',
        'pk02/out_kt_cert_v1_8_c.e3n4.out': '6c31c32395b0b8d64f7d903686416b1c7b7dfa71dd0fcf4dcdf79715a847aa20',
        'pk02/out_kt_cert_v1_8_c.e3n3.out': '5662bdae132cadf3c5fe5a56e2826a05cc7e2eb91d6902af773b3b4051fe170b',
        'pk02/out_kt_cert_v1_8_tX0.tn4.out': 'b71c672de7f6ed7d665c19a8ae3783a6a5af42feefc2b9bb122636e75b42c2ea',
        'pk02/out_kt_cert_v1_8_tX0.tn3.out': '013eac94b5355ff3214ba9f7eae434b1f7179d9413a85a98648e721f7fc141bf',
        'pk02/out_kt_cert_v1_8_tX0.e1n4.out': '543abdac45c6f724b84c7b53adc590bf04ade761f53693f4ce27cf1e16832c85',
        'pk02/out_kt_cert_v1_8_tX0.e1n3.out': 'c9f8b79f37d8595e550e489330017ab35b58d9f03327d999e39933d44981aea4',
        'pk02/out_kt_cert_v1_8_tX0.e3n4.out': 'b26fdb86148a66759a551d103271cd70e9fc5c6f95531d402bbb2536dfe7aac7',
        'pk02/out_kt_cert_v1_8_tX0.e3n3.out': '028d86be723d7119e38f11a3ef873eec969c37211a123bdf59e13b054df86c99',
        'pk02/out_kt_cert_v1_8_tX1.tn4.out': '7c1c4704558b77739b94a06f073e121f5d3b157e7171e51d283775a8314ffca6',
        'pk02/out_kt_cert_v1_8_tX1.tn3.out': '52c49c05b083ec0b235124c662cc6604f106aa0d1db560975aeb2f1c7b2169b0',
        'pk02/out_kt_cert_v1_8_tX1.e1n4.out': 'c1aa3fa4850468f9e1f597852396ce938e3ce667d5297f112c9d3efeeb1f0fce',
        'pk02/out_kt_cert_v1_8_tX1.e1n3.out': '1a66a1bd813cfdf4b03281e7f31b66b6d3a3cd5552c06dfa9950cd2f6c7e6af0',
        'pk02/out_kt_cert_v1_8_tX1.e3n4.out': '518e4918d09e6365fc9e5f977088379266ba1dc878434e283c7666d263ff40c0',
        'pk02/out_kt_cert_v1_8_tX1.e3n3.out': 'd8b82c913246465da00aaa5d36a7292ae50555b61462b3c68f6a62d62db92f93',
        'pk02/out_kt_cert_v1_8_tX2.tn4.out': 'e135e1ec6757f2099fab5dd75740f9934c5c3bf813310049b3ca7ac9d39c4d11',
        'pk02/out_kt_cert_v1_8_tX2.tn3.out': '5e6c5a08135f5bfe33ced513b72a19bcc3cd162bf93186037dc029633a15e9a3',
        'pk02/out_kt_cert_v1_8_tX2.e1n4.out': '95785502521c7dd3accb414902cac9ff3de836b0f8bbc3a556c4a9f8512fce2c',
        'pk02/out_kt_cert_v1_8_tX2.e1n3.out': '8300a55a6a6f9819558dee7b6e16921362ca776e7575c961136b4cd1debc7df8',
        'pk02/out_kt_cert_v1_8_tX2.e3n4.out': 'c55052347f8482a637c9749d6a8f41edb85416a2964f02560f73dd6e95db0e3a',
        'pk02/out_kt_cert_v1_8_tX2.e3n3.out': 'da8fe36cdbcf412c6a99483c272a4773924100ad140cc0d8f4ea1171fd31dab3',
        'pk02/out_kt_cert_v1_8_tB.tn4.out': '9a4784421d04987af70d8fc8f27ef3258974f9f4ac394b4590960736a5f04b0a',
        'pk02/out_kt_cert_v1_8_tB.tn3.out': '2eb77cdbb9a3c4e65306c7fd8b13c39306e86f69ee274dbf7f88149e62f1ad03',
        'pk02/out_kt_cert_v1_8_tB.e1n4.out': '2a8572127dfe1ef2b0f2ca997a451cfd311ecb8fac8cc5a7d3166ef3b1c79f26',
        'pk02/out_kt_cert_v1_8_tB.e1n3.out': 'ee1a9a1b85c10b1aabcf0dee55aad159ab66f7389c2fd704c8217d97182b15ba',
        'pk02/out_kt_cert_v1_8_tB.e3n4.out': '7537af5adf84e2d842e00aa1493802ab3d0b9ee1a76baa3c4e1fc67becc74682',
        'pk02/out_kt_cert_v1_8_tB.e3n3.out': '591f930dd423b1ae471437192b510171e665d7504f67bb86a19d704788411d79',
        'pk02/out/out_kt_c_t_trade_v1_3_jtn4.out': '9ee9e865421e984c1fefca9deb972d66bc03400fef370f0d2741b4adea86ab1b',
        'pk02/out/out_kt_c_t_trade_v1_3_jtn3.out': '3a37de73933ad01f74a8a7f17ad73530317f1ee2871e43432cd55a6e035a840f',
        'pk02/out/out_kt_c_t_trade_v1_3_jamn4.out': 'e495bf279f25b92f78a02a28e79bacfa5ad454b41af552860a2361b342d156c1',
        'pk02/out/out_kt_c_t_trade_v1_3_jamn3.out': 'ef8eed45202f9ef85850f6ab35f4b354634b081d333c0e06b7b92f98911aa333',
        'pk02/out/out_kt_c_t_trade_v1_3_je1n4.out': '5f6d9b9b22621d66e999742c1de43ab77edc52d9fe9cbb24e155b96ea711f259',
        'pk02/out/out_kt_c_t_trade_v1_3_je1n3.out': '69e42a83cc46140b8688f0d538ec1d1812ea32c72a8c23e7f9f9d993cefd6e3f',
        'pk02/out/out_kt_c_t_trade_v1_3_je3n4.out': '864aa3929517e3bc7e822404685bfe8e70435af84c843685659a73175d2a1084',
        'pk02/out/out_kt_c_t_trade_v1_3_je3n3.out': '8e15beeae457c8fe8e835adf62ee996907b09c77b95c104fa8d214edca335611',
    },
    'PIN_X': {
        'pk02/out_kt_cert_v1_7_x.tn4.out': '357ca5b1c5cfa7bb8863f761e5d7a9b312f84dbf3b5572b40bda299c6b2acfb5',
        'pk02/out_kt_cert_v1_7_x.tn3.out': '931ee6b39d7b86280fa7d3e0b768cf2b0f6adde456193f34f3c88864ec517ed4',
        'pk02/out_kt_cert_v1_7_x.amn4.out': '9eb9ea6bd0b42c6a12935a615c92a6e9cab6432eecd9e02c0177e215d298b874',
        'pk02/out_kt_cert_v1_7_x.amn3.out': 'a7d563884b9da3b895bd7aca6863a0002532f9cae4a209bfdf04e6ba34e9d319',
        'pk02/out_kt_cert_v1_6_x.e1n4.out': '1e0aa13ee35d748c75c67e3af4f786f4df858d93f01e709933203a916e4b70aa',
        'pk02/out_kt_cert_v1_6_x.e1n3.out': 'dc9111f62519c3cce00eaa51c81845b5535b8aab8f9e6a69158ea8003e748b81',
        'pk02/out_kt_cert_v1_6_x.e3n4.out': '4bb4ba5694aad31c4596af291f1089d4b5074f00afec72da9d4089fbc83a708d',
        'pk02/out_kt_cert_v1_6_x.e3n3.out': '28cfd89dbba2b7d2be5cdcaa6c5010873b677ed3f97f9f4eb15475691a580817',
    },
    'PIN_M2B': {
        'pk02/M2B_KV_v1.txt': '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',
        'pk02/out/out_m2b_asm_v1.out': 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391',
        'pk02/m2b_reader_v1.py': 'a9f15db48e9fa51629448181d8a83679c1b93cd2b5696c8ed1e6b41d60df8b02',
    },
    'PIN_M3_S9': {
        'pk03/m3_reader_v4_4.py': 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0',
        'pk03/out/m3_s9_N4_J300_v1_8_3.json': 'bcc6434c6a03eecb232f10504b63f1ce10a94a489d5a2ba9cf3fe09c8018b831',
        'pk03/out/m3_run_v1_8_3_asm9.4.out': 'a41763a35f405668c748cdd1aaccfff681aacf5fb096342a791659ccb49c07a7',
        'pk03/out/m3_s9_N3_J300_v1_8_3.json': 'd287d3dcbd4bd988aa8061fbe11b3da1609e0ab4d27ae1a619eadcee963e8fa5',
        'pk03/out/m3_run_v1_8_3_asm9.3.out': 'e7f09f7381919a8aef322adfae9ada7506bda4db527faba01b8deacdf6542655',
    },
    'PIN_M3_VAC': {
        'pk03/out/m3_vac_N4_J150_v2_1.json': '5628ba351d2f0dbd0f36f463e3a3bc4c9c02b96d1c194e4f23098357988732a4',
        'pk03/out/m3_vac_v2_1_asm.4.out': '9cb620ecfba0ec3891455ef309e27c77bc666bdefb122b94061f582ae9a16473',
        'pk03/out/m3_vac_N3_J150_v2_1.json': '57fbe83fb2640831768f3bc10d736653e423a5a7177099746afbf7a3d0f9f97a',
        'pk03/out/m3_vac_v2_1_asm.3.out': '27600d6dcb634a3c00af82f47ee013fcb7e949dd216899330618db90cdfac1c7',
        'pk03/m3_reader_v5.py': '44b95cfdd4dbffdeb8e970a9ef5dc6cd94320f89e36790a215f7dc710746956c',
    },
    'PIN_TRIAL': {
        'pk11/out/vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
        'pk11/out/vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
        'pk11/out/ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
        'pk11/out/ts_N3_S_z9sym_v1.json': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    },
    'PIN_FAR': {
        'pk02/far_crude_reader_v1.py': 'd657eac2c432007ed12c24566f3c72a8d5aced995d3013bb878606845356daf8',
        'pk02/FAR_CRUDE_v1_N4.json': '7140b2a55eea6a9b433905ca834d050e3660bb69ee4cf8244667cd0c63c1a2ef',
        'pk02/out/far_crude_v1.N4.out': 'c859c361eb0a34be0a30bcfc57f73d4d1875b891b3f6bcd439c8277e0aa4c38f',
        'pk02/FAR_CRUDE_v1_N3.json': 'f174b2c3e05ca9b1e955678d04f1df1ff8cc8ad883bf61e9e96b266d7609279d',
        'pk02/out/far_crude_v1.N3.out': '283e4fe77f36789f7009bc3d4b52f388bc9f1e4a8101860c3fdb3dcdd1b45396',
        'pk02/MANIFEST_FAR_CRUDE_v1_RUN.sha256': 'cc7ef7e5b69daf3b0483255fab7397248f98330ee267ac5c5d292083294fef79',
    },
}
KTSRC = {   # kt_cert_v1_8.py line -> its exact text
    341: 'RHO_M, RHO_E = 0.55, 0.6                    # free radii (exact binary64)',
    342: 'DELTA = arb.pi() * 40 / 180                 # 40 degrees, in arb',
    818: 'a_m, a_e = RHO_M ** 2, RHO_E ** 2',
    1621: 'LAM_T = 0.45          # the Chernoff lambda of tailX, tailB and ann (free choice, exact binary64)',
    1719: 'def kappa_B():',
    1721: '    amax = max(a_m, a_e)',
    1722: '    kap = 2 * (1 - DELTA.cos()) - arb(amax) ** 2 / (4 * (1 - arb(amax)))',
    1723: '    assert kap > 0',
    1724: '    return kap',
}
S9_RITZ = {4: ('pk03/out/m3_s9_N4_J300_v1_8_3.json', 'pk03/out/m3_run_v1_8_3_asm9.4.out'),
           3: ('pk03/out/m3_s9_N3_J300_v1_8_3.json', 'pk03/out/m3_run_v1_8_3_asm9.3.out')}   # pk03's delivery
FAR_CRUDE = {4: ('pk02/FAR_CRUDE_v1_N4.json', 'pk02/out/far_crude_v1.N4.out'), 3: ('pk02/FAR_CRUDE_v1_N3.json', 'pk02/out/far_crude_v1.N3.out')}
FAR_READER = 'pk02/far_crude_reader_v1.py'
KINDS = ('t', 'am', 'e1', 'e3')
QNAME = {'t': 'A_t', 'am': 'A_am', 'e1': 'R_e1', 'e3': 'R_e3'}
ZKEY = {'t': 'G,0,0', 'am': 'G,0,0', 'e1': 'G,1,1', 'e3': 'G,3,3'}
TSF = {4: 'pk11/out/ts_N4_J170_D_S_z9sym_v1.json', 3: 'pk11/out/ts_N3_S_z9sym_v1.json'}
VRF = {4: 'pk11/out/vacres_K3_N4_sym_v1.json', 3: 'pk11/out/vacres_K3_N3_sym_v1.json'}
VAC = {4: ('pk03/out/m3_vac_N4_J150_v2_1.json', 'pk03/out/m3_vac_v2_1_asm.4.out'),
       3: ('pk03/out/m3_vac_N3_J150_v2_1.json', 'pk03/out/m3_vac_v2_1_asm.3.out')}
M2B = ('pk02/M2B_KV_v1.txt', 'pk02/out/out_m2b_asm_v1.out', 'pk02/m2b_reader_v1.py')
M3V, M3S = 'pk03/m3_reader_v5.py', 'pk03/m3_reader_v4_4.py'
KTCERT, KTMAN = 'pk02/kt_cert_v1_8.py', 'pk02/MANIFEST_KT_CERT_v1_8_RUN.sha256'
TAILS = ('tX0', 'tX1', 'tX2', 'tB')
BUDGET = {4: Fraction(27, 1000), 3: Fraction(3, 100)}
JSCAN = (300, 400, 500, 600)
JGATE = (400, 500, 600)                          # C-LAW-SCAN (SPEC_M4_LAW_v1_1 sect. 5)
SLACK_LO, SLACK_HI = Fraction(1, 10 ** 4), Fraction(3, 100)
SCAN_SLACK = Fraction(1, 10 ** 6)
EXPECT = {(4, 't'): '+0.34%', (3, 't'): '+0.32%', (4, 'am'): '+0.89%', (3, 'am'): '+1.68%'}   # (e1, e3: about 0.4-0.75%)
SCAN = 'pk02/out/out_kt_c_t_trade_v1_3_j%sn%d.out'
DEC = re.compile(r'[0-9]+(\.[0-9]+)?(e[-+]?[0-9]+)?')
SDEC = re.compile(r'-?[0-9]+(\.[0-9]+)?(e[-+]?[0-9]+)?')
DECE = r'[0-9]+\.[0-9]+e[-+][0-9]+'
HEX64 = re.compile(r'[0-9a-f]{64}')
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]   # kt_cert_v1_8 l.334
FAILS = []
R = None   # m4_reader_v1, executed from its pinned bytes in main


def sha(data):
    return hashlib.sha256(data).hexdigest()


def all_pins():
    out = {}
    for g in PIN_GROUPS.values():
        out.update(g)
    out[READER] = READER_SHA
    return out


_BYTES = {}


def pinned(rel, pins=None):
    """C-HASH: the bytes of a pinned file under code/, read once and checked against its full sha256 at every use."""
    pins = all_pins() if pins is None else pins
    if not pins.get(rel):
        raise ValueError('C-HASH: %s is not pinned' % rel)
    if rel not in _BYTES:
        with open(os.path.join(CODEDIR, rel), 'rb') as fh:
            _BYTES[rel] = fh.read()
    if sha(_BYTES[rel]) != pins[rel]:
        raise ValueError('C-HASH: %s does not match its pin' % rel)
    return _BYTES[rel]


def lines(rel):
    return pinned(rel).decode().splitlines()


def module(rel, name):
    """a pinned Python module, executed from its checked bytes (ctx.prec is set to 256 again afterwards)."""
    mod = types.ModuleType(name)
    mod.__file__ = os.path.join(CODEDIR, rel)
    exec(compile(pinned(rel), mod.__file__, 'exec'), mod.__dict__)
    ctx.prec = 256
    return mod


def gate(name, ok, msg):
    print('%s: %s -> %s' % (name, msg, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)
    return ok


def c_hash():
    """every pin, then every entry of kt_cert_v1_8's run manifest (absolute paths under code/pk02/), equal to the pins it shares."""
    pins = all_pins()
    for rel in sorted(pins):
        pinned(rel)
    n = shared = 0
    for ln in lines(KTMAN):
        mt = re.fullmatch(r'([0-9a-f]{64})  (/\S+)', ln)
        if mt is None or not mt.group(2).startswith(CODEDIR + '/pk02/'):
            raise ValueError('C-HASH: a kt_cert run manifest line is not "<sha256>  <path under code/pk02/>"')
        with open(mt.group(2), 'rb') as fh:
            if sha(fh.read()) != mt.group(1):
                raise ValueError('C-HASH: %s differs from the kt_cert run manifest' % os.path.basename(mt.group(2)))
        rel = mt.group(2)[len(CODEDIR) + 1:]
        if rel in pins:
            shared += 1
            if pins[rel] != mt.group(1):
                raise ValueError('C-HASH: the pin of %s differs from the kt_cert run manifest' % rel)
        n += 1
    return len(pins), n, shared


def src_check():
    """C-KTCERT-SRC: the defining lines of the constants this law copies from kt_cert_v1_8, by exact line equality."""
    L = lines(KTCERT)
    bad = [k for k, s in sorted(KTSRC.items()) if k > len(L) or L[k - 1] != s]
    return gate('C-KTCERT-SRC', not bad and len(KTSRC) == 9,
                'kt_cert_v1_8 l.%s (RHO_M, RHO_E; DELTA; a_m, a_e; LAM_T; kappa_B) equal the lines the reader\'s constants copy%s'
                % (','.join(str(k) for k in sorted(KTSRC)), '' if not bad else '; differing: %s' % bad))


def kt_rel(item, kind, n):
    return 'pk02/out_kt_cert_v1_8_%s.%sn%d.out' % (item, kind, n)


def kt_lines(L, item, kind, n):
    """a kt_cert_v1_8 record: the first line's tokens (producer, the pinned kt_cert_v1_8.py sha256, ITEM), FORMAT and VERDICT exactly."""
    tag = '%s.%sn%d' % (item, kind, n)
    if not L or L[0].split(' ')[:4] != ['kt_cert_v1_8', 'sha256', all_pins()[KTCERT], 'ITEM=' + tag]:
        raise ValueError('C-REC %s: the first line does not name kt_cert_v1_8 at its pin and ITEM=%s' % (tag, tag))
    if [ln for ln in L if ln.startswith('FORMAT')] != ['FORMAT KT_CERT_RECORD_v1_8 CERTIFIED']:
        raise ValueError('C-REC %s: FORMAT lines are not exactly [FORMAT KT_CERT_RECORD_v1_8 CERTIFIED]' % tag)
    if [ln for ln in L if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise ValueError('C-REC %s: VERDICT lines are not exactly [VERDICT VALID]' % tag)
    return L


def lawbase(L, kind, n):
    """the one LAWBASE line: the allow-listed keys, each once, each value a nonnegative decimal (kept as written)."""
    head = 'LAWBASE N=%d %s: ' % (n, kind)
    ll = [ln for ln in L if ln.startswith('LAWBASE')]
    if len(ll) != 1 or not ll[0].startswith(head):
        raise ValueError('C-REC LAWBASE N=%d %s: not exactly one LAWBASE line, with that head' % (n, kind))
    tok = ll[0][len(head):].split(' ')
    keys, vals = tok[0::2], tok[1::2]
    if len(keys) != len(vals) or len(set(keys)) != len(keys):
        raise ValueError('C-REC LAWBASE N=%d %s: a key twice or a key without its value' % (n, kind))
    if kind == 'am':
        want = ['M0', 'M1', 'M2', 'M3', 'nR']
    else:
        nk = len([k for k in keys if k.startswith('nD_k')])
        want = ['M0', 'M1', 'M2', 'M3', 'nD'] + ['nD_k%d' % i for i in range(nk)] + ['nR0', 'TXm', 'TBm', 'ann']
        if nk == 0:
            want = None
    if want is None or sorted(keys) != sorted(want):
        raise ValueError('C-REC LAWBASE N=%d %s: the keys are not the allow-list' % (n, kind))
    for k, v in zip(keys, vals):
        if not DEC.fullmatch(v):
            raise ValueError('C-REC LAWBASE N=%d %s: %s is not a nonnegative decimal' % (n, kind, k))
    return dict(zip(keys, vals))


def result(L, kind, n):
    """the one RESULT line: (Q_lo, Q_hi, bound_lo, bound_hi) as written."""
    ll = [ln for ln in L if ln.startswith('RESULT')]
    pat = r'RESULT N=%d J=300 %s: %s \[(%s), (%s)\] bound \[(%s), (%s)\] FLOAT-IN .*' % (n, kind, QNAME[kind], DECE, DECE, DECE, DECE)
    mt = re.fullmatch(pat, ll[0]) if len(ll) == 1 else None
    if mt is None:
        raise ValueError('C-REC RESULT N=%d %s: not exactly one RESULT line of that form' % (n, kind))
    return mt.groups()


def pass_lines(L, tag, n, kind, fam=False):
    """C-LAW300-NEAR: every line of the tag has the exact head and ends with ' -> PASS'; at least one."""
    head = re.compile(r'%s N=%d %s%s: ' % (re.escape(tag), n, kind, r' [A-Z][0-9]+' if fam else ''))
    ll = [ln for ln in L if ln.startswith(tag + ' ')]
    if not ll or any(head.match(ln) is None or not ln.endswith(' -> PASS') for ln in ll):
        raise ValueError('C-LAW300-NEAR %s N=%d %s: %d lines, not all of that head and reading PASS' % (tag, n, kind, len(ll)))
    return len(ll)


def explicit(L, kind, n, prod):
    """an x record: the first line's tokens, VERDICT exactly, one EXPLICIT data line, m0..m3 with one exact binary64 repr per basis vector."""
    t0 = L[0].split(' ') if L else []
    if len(t0) < 4 or t0[:2] != [prod, 'sha256'] or not HEX64.fullmatch(t0[2]) or t0[3] != 'ITEM=x.%sn%d' % (kind, n):
        raise ValueError('C-REC x.%sn%d: the first line does not name %s and the item' % (kind, n, prod))
    if [ln for ln in L if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise ValueError('C-REC x.%sn%d: VERDICT lines are not exactly [VERDICT VALID]' % (kind, n))
    head = 'EXPLICIT N=%d %-3s: m0 ' % (n, kind)          # the producer's data-line format (kt_cert_v1_6 l.634, kt_cert_v1_7 l.694)
    dl = [ln for ln in L if ln.startswith(head)]
    if len(dl) != 1:
        raise ValueError('C-REC x.%sn%d: not exactly one EXPLICIT data line' % (kind, n))
    groups = dl[0][len(head) - len('m0 '):].split(';', 1)[0].split(' | ')
    if len(groups) != 4:
        raise ValueError('C-REC x.%sn%d: %d orders, not m0..m3' % (kind, n, len(groups)))
    mg = {}
    for j, grp in enumerate(groups):
        tk = grp.split(' ')
        if tk[0] != 'm%d' % j or len(tk) != 1 + len(R.BASES[kind]):
            raise ValueError('C-REC EXPLICIT N=%d %s: m%d carries %d values, not %d' % (n, kind, j, len(tk) - 1, len(R.BASES[kind])))
        for g, val in zip(R.BASES[kind], tk[1:]):
            R.binrepr(val, 'C-REC EXPLICIT N=%d %s m%d' % (n, kind, j))
            mg[(g, j)] = val
    return mg


def producers():
    """kt_cert_v1_8's PRODUCERS table (l.2169), read by exact text: {producer: full sha256}."""
    L = lines(KTCERT)
    pat = r"PRODUCERS = \{'kt_cert_v1_7': '([0-9a-f]{64})', 'kt_cert_v1_6': '([0-9a-f]{64})'\}   # "
    mt = re.match(pat, L[2168]) if len(L) >= 2169 else None
    if mt is None:
        raise ValueError('C-X-TIE: kt_cert_v1_8 l.2169 is not the PRODUCERS table')
    return {'kt_cert_v1_7': mt.group(1), 'kt_cert_v1_6': mt.group(2)}


def x_tie(Lg, Lx, kind, n, prod, xrel, prods):
    """C-X-TIE (SPEC_M4_LAW_v1_1 sect. 1 (b)): the x record's producer and sha256 are kt_cert_v1_8's PRODUCERS entry; the g record's one
    HANDOFF-READ x line names the x record, and its hand-off and sha256 are those of the x record's one HANDOFF line. Returns the sha256."""
    t0 = Lx[0].split(' ') if Lx else []
    if len(t0) < 3 or t0[0] != prod or prods.get(prod) != t0[2]:
        raise ValueError('C-X-TIE x.%sn%d: the producer is not kt_cert_v1_8\'s PRODUCERS entry for %s' % (kind, n, prod))
    gre = r'HANDOFF-READ N=%d %s x: (\S+) sha256 ([0-9a-f]{64}) equals its record \((\S+)\); body checksum and header PASS' % (n, kind)
    gl = [mt for mt in (re.fullmatch(gre, ln) for ln in Lg) if mt]
    ng = len([ln for ln in Lg if ln.startswith('HANDOFF-READ N=%d %s x: ' % (n, kind))])
    xl = [mt for mt in (re.fullmatch(r'HANDOFF N=%d %s x: (\S+) sha256 ([0-9a-f]{64}) \(.*\)' % (n, kind), ln) for ln in Lx) if mt]
    nx = len([ln for ln in Lx if ln.startswith('HANDOFF N=%d %s x: ' % (n, kind))])
    if not (len(gl) == ng == 1 and len(xl) == nx == 1 and gl[0].group(3) == os.path.basename(xrel)
            and gl[0].group(1) == xl[0].group(1) and gl[0].group(2) == xl[0].group(2)):
        raise ValueError('C-X-TIE x.%sn%d: the g record\'s HANDOFF-READ x line does not match the x record\'s HANDOFF line' % (kind, n))
    return xl[0].group(2)


def scan_pins():
    """C-SCAN-PIN: every scan output is pinned at kt_cert_v1_8's FIXREFS sha256 (l.273-280, exact text)."""
    L = lines(KTCERT)
    fx = {}
    for ln in L[272:280]:
        mt = re.fullmatch(r"    '(out_kt_c_t_trade_v1_3_j[a-z0-9]+\.out)': '([0-9a-f]{64})',", ln)
        if mt is None:
            raise ValueError('C-SCAN-PIN: kt_cert_v1_8 l.273-280 are not the FIXREFS j entries')
        fx[mt.group(1)] = mt.group(2)
    pins = all_pins()
    for kind in KINDS:
        for n in (4, 3):
            if fx.get(os.path.basename(SCAN % (kind, n))) != pins.get(SCAN % (kind, n)):
                raise ValueError('C-SCAN-PIN: %s is not pinned at its FIXREFS sha256' % os.path.basename(SCAN % (kind, n)))
    return len(fx)


def mhat(atext, n):
    """C-MHAT: M2(b)'s one C-MHAT line at N reads PASS, with m1, m2, m3 >= 0 exactly."""
    ll = [ln for ln in atext.splitlines() if ln.startswith('C-MHAT N=%d:' % n)]
    pat = r'C-MHAT N=%d: m1\.\.m3 = \[(\S+), (\S+), (\S+)\] >= 0 exactly; .* -> PASS' % n
    mt = re.fullmatch(pat, ll[0]) if len(ll) == 1 else None
    if mt is None:
        raise ValueError('C-MHAT N=%d: not exactly one C-MHAT line of that form reading PASS' % n)
    m = [R.binrepr(x, 'C-MHAT N=%d' % n) for x in mt.groups()]
    if not all(x >= 0 for x in m):
        raise ValueError('C-MHAT N=%d: an m_k is negative' % n)
    return m


def dec_down(f, digits=17):
    """a decimal string at or below the Fraction f > 0 (rounded down exactly to the given significant digits)."""
    if f <= 0:
        raise ValueError('dec_down: %r is not > 0' % f)
    e = len(str(f.numerator)) - len(str(f.denominator))
    while Fraction(10) ** e > f:
        e -= 1
    while Fraction(10) ** (e + 1) <= f:
        e += 1
    sc = f * Fraction(10) ** (digits - 1 - e)
    s = str(sc.numerator // sc.denominator)
    return '%s.%se%+03d' % (s[0], s[1:], e)


def zmin_of(LO, eb):
    """Z_min = LO_0 + sum_{k>=1} min(LO_k, 0) 300^-k - err_b (SPEC sect. 2.4), exact; refused unless > 0."""
    lo = [Fraction(x) for x in LO]
    z = lo[0] + sum(min(lo[k], 0) * Fraction(1, 300) ** k for k in range(1, len(lo))) - Fraction(eb)
    if not z > 0:
        raise ValueError('Z_min is not > 0')
    return z


def s9_trial(r9, n):
    """C-S9-TRIAL: the S9 record's trial_set names the pinned ts and vacres files as basename:sha256 (item (v)'s check)."""
    ts = r9.get('trial_set') if isinstance(r9, dict) else None
    for k, p in (('ts', TSF[n]), ('vacres', VRF[n])):
        if not isinstance(ts, dict) or ts.get(k) != '%s:%s' % (os.path.basename(p), all_pins()[p]):
            raise ValueError('C-S9-TRIAL N=%d: trial_set %s is not the pinned %s' % (n, k, os.path.basename(p)))
    return True


def s9_cert(m3s, n):
    """(d) S9: Z_min per kind through m3_reader_v4_4 (load bound to the asm output), after C-S9-TRIAL and C-Z-A0."""
    path, aout = S9_RITZ[n]
    pinned(path)
    pinned(aout)
    rec = m3s.load(os.path.join(CODEDIR, path), os.path.join(CODEDIR, aout), 300, n)
    ctx.prec = 256
    raw = json.loads(pinned(path).decode())
    s9_trial(raw, n)
    z = {}
    for kind in KINDS:
        ball = m3s.entry_ball(rec, ZKEY[kind])
        z_const(raw['items'][ZKEY[kind]], ball, ZKEY[kind], n)
        z[kind] = zmin_of(ball[0], ball[2])
    return z


Z_A0 = {}   # C-Z-A0's findings: (N, entry key) -> a0_exact


def z_const(item, ball, key, n):
    """C-Z-A0: Z_min's constant term is the certified lower end LO_0 = a_0 - rad_0 of the entry; it is a_0 itself only
    when the record's a0_exact is "1", which then needs a_0 = 1 with radius 0. Checks entry_ball's LO_0 against the raw item; returns LO_0."""
    LO, HI, eb = ball
    a0x = item.get('a0_exact')
    if a0x not in ('1', None):
        raise ValueError('C-Z-A0 N=%d %s: a0_exact %r is neither "1" nor null' % (n, key, a0x))
    lo0, hi0, ak0, rad0 = Fraction(LO[0]), Fraction(HI[0]), Fraction(item['ak'][0]), Fraction(item['ak_rad'][0])
    if a0x == '1' and not (lo0 == hi0 == ak0 == 1 and rad0 == 0):
        raise ValueError('C-Z-A0 N=%d %s: a0_exact "1" but a_0 is not 1 with radius 0' % (n, key))
    if lo0 != ak0 - rad0:
        raise ValueError('C-Z-A0 N=%d %s: entry_ball LO_0 is not ak_0 - ak_rad_0 of the record' % (n, key))
    Z_A0[(n, key)] = a0x
    return lo0


def mock_far(rel):
    """the MOCK far items of the dry run: strict KEY = value, FORMAT 'MOCK_M4_FAR_v1 MOCK', CLAIM starting 'MOCK '; per N and kind the far
    tokens in the record's form. Returns {N: {kind: tokens}}."""
    kv = R.parse('\n'.join(lines(rel)))
    want = {'FORMAT', 'CLAIM'} | {'N%d_%s_FAR' % (n, R.KK[k]) for n in (4, 3) for k in KINDS}
    if set(kv) != want or kv['FORMAT'] != 'MOCK_M4_FAR_v1 MOCK' or not kv['CLAIM'].startswith('MOCK '):
        raise ValueError('mock far: keys, FORMAT or CLAIM not the MOCK form')
    return dict((n, dict((kind, kv['N%d_%s_FAR' % (n, R.KK[kind])]) for kind in KINDS)) for n in (4, 3))


def far_tokens(items, names, w, kind):
    """one kind's far tokens 'name:X300:p:c' from FAR_CRUDE_v1's items (X300 rounded up, c rounded down), with C-FAR-W: the record's w of a
    call is the largest J-power of the call's weight over the kinds that use it (pk02; E4:e1:e1 serves e1, hf = 1, and the hook kind h1,
    hf = 2J), so this kind's J-power must be at most w (and FAR_CRUDE_v1's own (w + p)/c <= 300 then covers this kind's)."""
    if not isinstance(names.get(kind), dict) or sorted(names[kind]) != sorted(R.far_names(kind)):
        raise ValueError('C-FAR %s: the record names are not the kind far items' % kind)
    out = []
    for name in R.far_names(kind):
        key = names[kind][name]
        x300, p, c = items[key]
        wk = w.get(key)
        if isinstance(wk, bool) or not isinstance(wk, int) or not (R.far_wpow(kind, name) <= wk <= 2):
            raise ValueError('C-FAR-W %s %s: the record w %r is below the weight J-power %d (or not an int <= 2)' % (kind, name, wk,
                                                                                                         R.far_wpow(kind, name)))
        if isinstance(p, bool) or not isinstance(p, int) or p < 0:
            raise ValueError('C-FAR %s %s: p is not a nonnegative int' % (kind, name))
        out.append('%s:%s:%d:%s' % (name, R.dec_up(Fraction(x300)), p, dec_down(Fraction(c))))
    return ' ; '.join(out)


def far_cert(frd, n):
    """(f) FAR_CRUDE_v1 at N through far_crude_reader_v1.load(path, out_path, expected_sha256, N): {kind: tokens}."""
    if n not in FAR_CRUDE or not FAR_READER:
        raise ValueError('C-FAR: FAR_CRUDE_v1 for N=%d is not pinned yet (SPEC_M4_LAW_v1_1 sect. 8)' % n)
    path, out = FAR_CRUDE[n]
    pinned(path)
    pinned(out)
    rec = frd.load(os.path.join(CODEDIR, path), os.path.join(CODEDIR, out), all_pins()[path], n)
    ctx.prec = 256
    return dict((kind, far_tokens(rec['items'], rec['names'], rec['w'], kind)) for kind in KINDS)


def supf(kind, n):
    """supF_a (kt_cert_v1_8 l.1394-1403) on the pinned trial files as {degree in J: coefficient ball}: t as h, 2J sup0 with
    sup0 = 1 + sum_i t^i sum |cb| (2J)^len(mono); e1, e3 as supb = |S[0, b]| + sum |S[1 + m, b]| (2J)^len(mono), b = 1, 3."""
    co = {}

    def add(d, x):
        co[d] = co.get(d, arb(0)) + x
    if kind == 't':
        r3 = json.loads(pinned(VRF[n]).decode())
        add(1, arb(2))
        for i in (1, 2, 3):
            q = r3['q%d' % i]
            if len(q) != len(BASIS):
                raise ValueError('supF N=%d: q%d has %d entries, not %d' % (n, i, len(q), len(BASIS)))
            for cb, mono in zip(q, BASIS):
                add(1 - i + len(mono), abs(arb(cb)) * 2 ** (1 + len(mono)))
    else:
        b = {'e1': 1, 'e3': 3}[kind]
        S = json.loads(pinned(TSF[n]).decode())['S']
        if len(S) != 1 + len(BASIS):
            raise ValueError('supF N=%d: S has %d rows, not %d' % (n, len(S), 1 + len(BASIS)))
        add(0, abs(arb(S[0][b])))
        for row, mono in zip(S[1:], BASIS):
            add(len(mono), abs(arb(row[b])) * 2 ** len(mono))
    return co


SQ5, SQ21 = arb(5).sqrt(), arb(21).sqrt()           # m2b_asm_v1 (6acd83d3) l.257-297 verbatim from here to ratio_main
TRI = [(3 + SQ21) / 6, (3 + SQ21) / 6, (3 * SQ5 - SQ21) / 12]
PAIRS = [(0, 1), (1, 2), (0, 2)]
E4 = [((r, s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((9 + r, 9 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((r, 3 + r), 1) for r in range(3)] + [((3 + r, 6 + r), 1) for r in range(3)] + [((6 + r, 9 + r), 1) for r in range(3)] + \
     [((3, 4), 1), ((4, 5), 1), ((6, 7), 1), ((7, 8), 1)]       # vacrig11f l.233-235 (the graph G4), couplings in arb


def lap_a(edges, V):
    L = arb_mat(V, V)
    for (u, v), c in edges:
        L[u, u] += c
        L[v, v] += c
        L[u, v] -= c
        L[v, u] -= c
    return L


def gauge_basis_a(V, S):
    """an exact basis of the orthogonal complement of 1_S (kt_cert_v1_7's)."""
    S = sorted(S)
    cols = [(s, S[0]) for s in S[1:]] + [(k, None) for k in range(V) if k not in S]
    Bm = arb_mat(V, len(cols))
    for j, (a_, b_) in enumerate(cols):
        Bm[a_, j] = 1
        if b_ is not None:
            Bm[b_, j] = -1
    return Bm


def ratio_main(r, nn):
    """vacrig11f l.393-395 in arb: (det(B^T L_E4 B)/det(B^T L_{E4 - (r, 3 + r)} B))^{nn/2}; the ratio does not depend on the basis B of
    the sum-zero subspace."""
    Bm = gauge_basis_a(12, range(12))
    edges_r = [(e_, c_) for (e_, c_) in E4 if e_ != (r, 3 + r)]
    d1 = (Bm.transpose() * lap_a(E4, 12) * Bm).det()
    d2 = (Bm.transpose() * lap_a(edges_r, 12) * Bm).det()
    if not (d1 > 0 and d2 > 0):
        raise ValueError('ratio_main: a determinant is not certainly positive')
    return ((d1 / d2).log() * nn / 2).exp()


def zr_strings(m3v, vrec, n):
    """N<N>_ZR_<r> as zR_r^up uses them: HI_0, max(HI_k, 0) for k = 1..3, err_b, all upper ends (a negative HI_0 or err_b is refused)."""
    out = []
    for r in range(3):
        LO, HI, eb = m3v.entry_ball(vrec, 'G4R_%d' % r)
        hi = [Fraction(x) for x in HI]
        if len(hi) != 4 or hi[0] < 0 or Fraction(eb) < 0:
            raise ValueError('G4R_%d N=%d: not four coefficients with HI_0 >= 0 and err_b >= 0' % (r, n))
        out.append(' ; '.join(R.dec_up(x) for x in [hi[0]] + [max(h, 0) for h in hi[1:]] + [Fraction(eb)]))
    return out


def supf_string(co):
    return ' ; '.join('%d:%s' % (d, R.dec_up(R.frac_upper(c))) for d, c in sorted(co.items()))


def chernoff_ok(a_e, kappa):
    """C-MONO's rates: 0.45 a_e/2 > 0 and 0.45 kappa_B/2 > 0, certainly."""
    return a_e > 0 and bool(kappa > 0)


def inputs(mode, mock_rel):
    """(a)-(f): every record value, with C-REC, C-X-TIE, C-LAW300-NEAR, C-MHAT, C-S9-TRIAL and C-FAR-W (as refusals). Returns the values,
    the counts and the reader handles (C-COPY reads the sources again)."""
    m2r = module(M2B[2], 'm2b_reader_v1')
    m2rec = m2r.load(os.path.join(CODEDIR, M2B[0]), os.path.join(CODEDIR, M2B[1]), all_pins()[M2B[0]], all_pins()[M2B[2]])
    ctx.prec = 256
    m2out = pinned(M2B[1]).decode()
    m3v = module(M3V, 'm3_reader_v5')
    m3s = module(M3S, 'm3_reader_v4_4')
    frd = module(FAR_READER, 'far_crude_reader_v1') if mode == 'cert' and FAR_READER else None
    mockf = mock_far(mock_rel) if mode == 'mock' else None
    prods = producers()
    hd = {'m2r': m2r, 'm2rec': m2rec, 'frd': frd, 'mockf': mockf, 'm3v': m3v, 'm3s': m3s}
    v, count = {}, {'rec': 0, 'near': 0, 'xtie': 0}
    for n in (4, 3):
        vn = v[n] = {}
        mhat(m2out, n)
        eps = m2r.law_v1(m2rec, n, 300)['eps_r']
        ctx.prec = 256
        vrec = m3v.load(os.path.join(CODEDIR, VAC[n][0]), os.path.join(CODEDIR, VAC[n][1]), 150, n)
        ctx.prec = 256
        vn['ZR'] = zr_strings(m3v, vrec, n)
        vn['RM'] = [R.dec_up(R.frac_upper(ratio_main(r, n - 1))) for r in range(3)]
        z = s9_cert(m3s, n)
        far = far_cert(frd, n) if mode == 'cert' else mockf[n]
        for kind in KINDS:
            g = kt_lines(lines(kt_rel('g', kind, n)), 'g', kind, n)
            e = {'lb': lawbase(g, kind, n), 'q': result(g, kind, n), 'z': z[kind], 'far': far[kind]}
            count['near'] += pass_lines(g, 'C-NPK', n, kind)
            count['rec'] += 1
            if kind != 'am':
                count['near'] += pass_lines(kt_lines(lines(kt_rel('c', kind, n)), 'c', kind, n), 'C-NDK', n, kind)
                for it in TAILS:
                    count['near'] += pass_lines(kt_lines(lines(kt_rel(it, kind, n)), it, kind, n), 'C-TAILM', n, kind, True)
                count['rec'] += 1 + len(TAILS)
                e['supf'] = supf(kind, n)
            prod = 'kt_cert_v1_7' if kind in ('t', 'am') else 'kt_cert_v1_6'
            xrel = 'pk02/out_%s_x.%sn%d.out' % (prod, kind, n)
            e['mg'] = explicit(lines(xrel), kind, n, prod)
            x_tie(g, lines(xrel), kind, n, prod, xrel, prods)
            count['rec'] += 1
            count['xtie'] += 1
            if kind in ('e1', 'e3'):
                e['eps'] = eps
            vn[kind] = e
    return v, count, hd


def kvlist(v, own, asm_rel, l300, stamp):
    """the record's (key, value) pairs in sect. 4's order; L300 = '0' until it is computed."""
    kv = [('FORMAT', R.FIXED['FORMAT']), ('RECORD', R.FIXED['RECORD']), ('AUTHOR', R.FIXED['AUTHOR']), ('WRITTEN_UTC', stamp),
          ('CLAIM', R.CLAIM), ('LAW', R.FIXED['LAW']), ('J_REF', R.FIXED['J_REF']), ('ASM_SHA256', own),
          ('LAMBDA_CH', R.FIXED['LAMBDA_CH']), ('A_E', R.FIXED['A_E']), ('KAPPA_B', R.FIXED['KAPPA_B']), ('RHO_G', R.FIXED['RHO_G'])]
    for grp in R.KEYS_PIN:
        if grp == 'PIN_CODE':
            kv.append((grp, '%s:%s ; %s:%s' % (asm_rel, own, READER, READER_SHA)))
        else:
            kv.append((grp, ' ; '.join('%s:%s' % (p, h) for p, h in sorted(PIN_GROUPS[grp].items()))))
    for n in (4, 3):
        vn = v[n]
        kv += [('N%d_RATIO_MAIN_%d' % (n, r), vn['RM'][r]) for r in range(3)] + [('N%d_ZR_%d' % (n, r), vn['ZR'][r]) for r in range(3)]
        for kind in KINDS:
            e, pre = vn[kind], 'N%d_%s_' % (n, R.KK[kind])
            lb = e['lb']
            kv += [(pre + 'M%d' % k, lb['M%d' % k]) for k in range(4)]
            if kind == 'am':
                kv.append((pre + 'NR', lb['nR']))
            else:
                nk = len([k for k in lb if k.startswith('nD_k')])
                kv += [(pre + 'ND', lb['nD'])] + [(pre + 'ND_K%d' % i, lb['nD_k%d' % i]) for i in range(nk)]
                kv += [(pre + 'NR0', lb['nR0']), (pre + 'TXM', lb['TXm']), (pre + 'TBM', lb['TBm']), (pre + 'ANN', lb['ann'])]
            kv.append((pre + 'MG', ' ; '.join('%s:%d:%s' % (g, j, e['mg'][(g, j)]) for g in R.BASES[kind] for j in range(4))))
            kv.append((pre + 'FAR', e['far']))
            if kind != 'am':
                kv.append((pre + 'SUPF', supf_string(e['supf'])))
            kv.append((pre + 'ZMIN', dec_down(e['z'])))
            if kind in ('e1', 'e3'):
                kv.append((pre + 'EPSR300', e['eps']))
            kv.append((pre + 'L300', l300[(n, kind)] if l300 else '0'))
            kv.append((pre + 'Q300', e['q'][1]))
    kv.append(('VERDICT', R.FIXED['VERDICT']))
    return kv


def text_of(kv):
    return ('# M4_KV_v1: the J-uniform law of kt_cert\'s A_t, A_am, R_e1 and R_e3 (SPEC_M4_LAW_v1 d51742f2), written by m4_asm_v1\n'
            + ''.join('%s = %s\n' % (k, x) for k, x in kv))


def law300_ok(rec, v, n, kind):
    """C-LAW300: Q_lo (1 - 1e-6) <= L_k(300) <= Q_hi (1 + 0.02), with L_k(300) the decimal the record carries."""
    L, q = Fraction(R.law(rec, kind, n, 300)), v[n][kind]['q']
    return Fraction(q[0]) * (1 - SLACK_LO) <= L <= Fraction(q[1]) * (1 + SLACK_HI)


def jnear(n, kind):
    """the trade scan's float near at J = 300, 400, 500, 600 as printed (decimal strings): one JTERMS2 line per J; VERDICT exactly VALID."""
    L = lines(SCAN % (kind, n))
    if [ln for ln in L if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise ValueError('C-SCAN: the scan output j%sn%d is not VERDICT VALID' % (kind, n))
    out = {}
    for J in JSCAN:
        ll = [mt.group(1) for mt in (re.match(r'JTERMS2 N=%d J=%d %s: .* near (%s)( |$)' % (n, J, kind, DECE), ln) for ln in L) if mt]
        if len(ll) != 1:
            raise ValueError('C-SCAN: not one JTERMS2 near at N=%d J=%d %s' % (n, J, kind))
        out[J] = ll[0]
    return out


def frac_lower(x):
    """the exact lower end of a finite ball as a Fraction (python-flint's man_exp is signed)."""
    if not x.is_finite():
        raise ValueError('a law ball is not finite')
    m, e = x.lower().man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def numerator(rec, kind, n, J):
    """the law's numerator sqrt(near^2 + far) + gB at J (L_k(J) D_k), as a ball."""
    b = R.law_balls(rec, kind, n, J)
    return (b['near'] * b['near'] + b['far']).sqrt() + b['gB']


def law_scan_ok(rec, kind, n, nf):
    """C-LAW-SCAN at (k, N): the numerator's lower end >= near_k^float(J) (1 - 1e-6) at J = 400, 500, 600."""
    return all(frac_lower(numerator(rec, kind, n, J)) >= Fraction(nf[J]) * (1 - SCAN_SLACK) for J in JGATE)


def c_copy(text, hd, far_again):
    """C-COPY: the written record parsed back; every copied key equals its source token, re-read from the pinned file (or
    the source reader again), by exact string equality. Returns the number of keys compared."""
    kv = R.parse(text)
    nk = 0
    for n in (4, 3):
        eps = hd['m2r'].law_v1(hd['m2rec'], n, 300)['eps_r']
        ctx.prec = 256
        far = far_again(n)
        vrec = hd['m3v'].load(os.path.join(CODEDIR, VAC[n][0]), os.path.join(CODEDIR, VAC[n][1]), 150, n)
        ctx.prec = 256
        for r, s in enumerate(zr_strings(hd['m3v'], vrec, n)):     # ZR recomputed from entry_ball
            if kv.get('N%d_ZR_%d' % (n, r)) != s:
                raise ValueError('C-COPY N%d_ZR_%d: the record value is not entry_ball recomputed' % (n, r))
            if kv.get('N%d_RATIO_MAIN_%d' % (n, r)) != R.dec_up(R.frac_upper(ratio_main(r, n - 1))):
                raise ValueError('C-COPY N%d_RATIO_MAIN_%d: the record value is not ratio_main recomputed' % (n, r))
            nk += 2
        z = s9_cert(hd['m3s'], n)
        for kind in KINDS:
            pre = 'N%d_%s_' % (n, R.KK[kind])
            g = lines(kt_rel('g', kind, n))
            lb = [ln for ln in g if ln.startswith('LAWBASE N=%d %s: ' % (n, kind))]
            if len(lb) != 1:
                raise ValueError('C-COPY %s: not one LAWBASE source line' % pre)
            body = ' ' + lb[0].split(': ', 1)[1]
            src = {'M0': 'M0', 'M1': 'M1', 'M2': 'M2', 'M3': 'M3'}
            if kind == 'am':
                src['NR'] = 'nR'
            else:
                src.update(ND='nD', NR0='nR0', TXM='TXm', TBM='TBm', ANN='ann')
                nks = len(re.findall(r' nD_k[0-9]+ ', body))
                if nks != len([k for k in kv if re.fullmatch(re.escape(pre) + r'ND_K[0-9]+', k)]):
                    raise ValueError('C-COPY %sND_K: the record has not the source count of nD_k tokens' % pre)
                src.update(('ND_K%d' % i, 'nD_k%d' % i) for i in range(nks))
            for rk, sk in src.items():
                toks = re.findall(r' %s (\S+)' % re.escape(sk), body)
                if len(toks) != 1 or kv.get(pre + rk) != toks[0]:
                    raise ValueError('C-COPY %s%s: the record value is not its LAWBASE token %s' % (pre, rk, sk))
                nk += 1
            rl = [ln for ln in g if ln.startswith('RESULT N=%d J=300 %s: ' % (n, kind))]
            mt = re.match(r'RESULT N=%d J=300 %s: %s \[(\S+), (\S+)\] ' % (n, kind, QNAME[kind]), rl[0]) if len(rl) == 1 else None
            if mt is None or kv.get(pre + 'Q300') != mt.group(2):
                raise ValueError('C-COPY %sQ300: the record value is not the RESULT upper end' % pre)
            prod = 'kt_cert_v1_7' if kind in ('t', 'am') else 'kt_cert_v1_6'
            head = 'EXPLICIT N=%d %-3s: m0 ' % (n, kind)
            dl = [ln for ln in lines('pk02/out_%s_x.%sn%d.out' % (prod, kind, n)) if ln.startswith(head)]
            grp = [x.split(' ') for x in dl[0][len(head) - len('m0 '):].split(';', 1)[0].split(' | ')] if len(dl) == 1 else []
            want = ' ; '.join('%s:%d:%s' % (b, j, grp[j][1 + i]) for i, b in enumerate(R.BASES[kind]) for j in range(4)) if len(grp) == 4 else None
            if want is None or kv.get(pre + 'MG') != want:
                raise ValueError('C-COPY %sMG: the record value is not the EXPLICIT data line' % pre)
            if kind in ('e1', 'e3') and kv.get(pre + 'EPSR300') != eps:
                raise ValueError('C-COPY %sEPSR300: the record value is not law_v1 eps_r again' % pre)
            if kv.get(pre + 'FAR') != far[kind]:
                raise ValueError('C-COPY %sFAR: the record value is not the far source again' % pre)
            if kv.get(pre + 'ZMIN') != dec_down(z[kind]):
                raise ValueError('C-COPY %sZMIN: the record value is not Z_min recomputed from the S9 entry' % pre)
            if kind != 'am' and kv.get(pre + 'SUPF') != supf_string(supf(kind, n)):
                raise ValueError('C-COPY %sSUPF: the record value is not supF recomputed' % pre)
            nk += 4 + (kind in ('e1', 'e3')) + (kind != 'am')
    return nk


def budget(rec, v):
    """C-BUDGET (INFO, FLOAT)."""
    for n in (4, 3):
        worst = {}
        for kind in KINDS:
            nf, D = jnear(n, kind), R.law_balls(rec, kind, n, 300)['D']
            parts = []
            for J in JSCAN:
                loss = float((R.law_balls(rec, kind, n, J)['L'] * D).mid()) / float(nf[J]) - 1
                worst[kind] = max(worst.get(kind, loss), loss)
                parts.append('J=%d %+.4f%%' % (J, 100 * loss))
            print('C-BUDGET N=%d %s (INFO, FLOAT): L_k(J) D_k / near_float(J) - 1: %s' % (n, kind, '; '.join(parts)))
        zc = {}
        for kind in ('t', 'am'):
            q = v[n][kind]['q']
            zc[kind] = (float(Fraction(q[3]) / Fraction(q[0])) ** 2 / float(v[n][kind]['z'])) ** 0.5 - 1
        tally = worst['t'] + worst['am'] + zc['t'] + zc['am']
        print('C-BUDGET N=%d (INFO, FLOAT): A_t + A_am tally %.3f%% = largest losses %.3f%% + %.3f%% and Z_min costs %.3f%% + %.3f%% '
              '(Z of the RESULT: (bound_hi/Q_lo)^2), against the corner budget %.1f%%' % (n, 100 * tally, 100 * worst['t'],
                                                                                      100 * worst['am'], 100 * zc['t'], 100 * zc['am'],
                                                                                      100 * float(BUDGET[n])))


def plant_refused(name, want, fn):
    """a plant that must be refused with the named message prefix."""
    try:
        fn()
        hit, why = False, 'not refused'
    except ValueError as e:
        hit, why = str(e).startswith(want), str(e)
    print('%s -> %s (%s)' % (name, 'FIRES' if hit else 'DOES NOT FIRE', why[:110]))
    if not hit:
        FAILS.append(name)


def plant_gate(name, ok_fn, what):
    """a plant whose gate must fail (ok_fn() False)."""
    ok = ok_fn()
    print('%s -> %s (%s %s)' % (name, 'FIRES' if not ok else 'DOES NOT FIRE', what, 'fails' if not ok else 'passes'))
    if ok:
        FAILS.append(name)


def _swap_line(L, old, new):
    return [new if ln == old else ln for ln in L]


def plants(text0, text, v, kvd, hd, far_again, rec):
    g = lines(kt_rel('g', 't', 4))
    fmt = 'FORMAT KT_CERT_RECORD_v1_8 CERTIFIED'
    sw = R._sub(R._sub(text0, 'N4_T_M1', kvd['N4_E1_M1']), 'N4_E1_M1', kvd['N4_T_M1'])
    rsw = R.parse_record(sw)
    plant_gate('PLANT-SWAP', lambda: law300_ok(rsw, v, 4, 't') or law300_ok(rsw, v, 4, 'e1'),
               'N4 t\'s and N4 e1\'s M1 exchanged: C-LAW300 on t or on e1')
    plant_gate('PLANT-MONO-KAPPA', lambda: chernoff_ok(R.A_E_F, arb(0)), 'kappa_B := 0: the Chernoff rates')
    plant_refused('PLANT-MONO-FAR', 'C-MONO-FAR4 N4 t oSS:', lambda: R.c_mono(R.parse_record(R._plant_far_c(text0, kvd))))
    plant_refused('PLANT-MOCK', 'C-REC g.tn4: FORMAT', lambda: kt_lines(_swap_line(g, fmt, 'FORMAT KT_CERT_RECORD_v1_8 MOCK'), 'g', 't', 4))
    plant_refused('PLANT-PRECERT', 'C-REC g.tn4: FORMAT',
                  lambda: kt_lines(_swap_line(g, fmt, 'FORMAT KT_CERT_RECORD_v1_8_PRECERT'), 'g', 't', 4))
    plant_refused('PLANT-VERDICT', 'C-REC g.tn4: VERDICT', lambda: kt_lines(_swap_line(g, 'VERDICT VALID', 'VERDICT VALID-PRECERT'), 'g', 't', 4))
    plant_refused('PLANT-PIN', 'C-HASH:', lambda: pinned(kt_rel('g', 't', 4), {kt_rel('g', 't', 4): all_pins()[kt_rel('g', 't', 4)][::-1]}))
    lbl = [ln for ln in g if ln.startswith('LAWBASE')][0]
    plant_refused('PLANT-LAWBASE-DUP', 'C-REC LAWBASE N=4 t: a key twice', lambda: lawbase(_swap_line(g, lbl, lbl + ' M1 1e-04'), 't', 4))
    plant_refused('PLANT-LAWBASE-MISS', 'C-REC LAWBASE N=4 t: the keys',
                  lambda: lawbase(_swap_line(g, lbl, re.sub(r' ann \S+', '', lbl)), 't', 4))
    x = lines('pk02/out_kt_cert_v1_7_x.tn4.out')
    xl = [ln for ln in x if ln.startswith('EXPLICIT N=4 t  : m0 ')][0]
    plant_refused('PLANT-EXPLICIT', 'C-REC EXPLICIT N=4 t: m1 carries 3 values',
                  lambda: explicit(_swap_line(x, xl, re.sub(r'\| m1 (\S+) ', '| m1 ', xl, count=1)), 't', 4, 'kt_cert_v1_7'))
    tx = lines(kt_rel('tX0', 't', 4))
    tl = [ln for ln in tx if ln.startswith('C-TAILM ')][0]
    plant_refused('PLANT-NEAR', 'C-LAW300-NEAR C-TAILM N=4 t:',
                  lambda: pass_lines(_swap_line(tx, tl, tl[:-len(' -> PASS')] + ' -> FAIL'), 'C-TAILM', 4, 't', True))
    plant_refused('PLANT-S9-TRIAL', 'C-S9-TRIAL N=4: trial_set ts',
                  lambda: s9_trial({'trial_set': {'ts': '%s:%s' % (os.path.basename(TSF[4]), all_pins()[TSF[3]]),
                                                  'vacres': '%s:%s' % (os.path.basename(VRF[4]), all_pins()[VRF[4]])}}, 4))
    plant_refused('PLANT-ORDER', 'C-COPY N4_T_M1:',
                  lambda: c_copy(R._sub(R._sub(text, 'N4_T_M1', kvd['N4_T_M3']), 'N4_T_M3', kvd['N4_T_M1']), hd, far_again))
    nf = jnear(4, 't')
    nf2 = dict(nf)
    nf2[500] = Fraction(nf[500]) * Fraction(102, 100)
    plant_gate('PLANT-SCAN', lambda: law_scan_ok(rec, 't', 4, nf2), 'N4 t scan near at J = 500 raised by 2%: C-LAW-SCAN')
    xh = [ln for ln in x if ln.startswith('HANDOFF N=4 t x: ')][0]
    plant_refused('PLANT-X-TIE', 'C-X-TIE x.tn4:', lambda: x_tie(g, _swap_line(x, xh, re.sub(r'sha256 [0-9a-f]{64}', 'sha256 ' + '0' * 64, xh)),
                                                                't', 4, 'kt_cert_v1_7', 'pk02/out_kt_cert_v1_7_x.tn4.out', producers()))
    nm_t = R.far_names('t')
    items = dict((nm, (Fraction(1, 10 ** 18), 2, Fraction(1, 20))) for nm in nm_t)
    w_ok = dict((nm, R.far_wpow('t', nm)) for nm in nm_t)
    far_tokens(items, {'t': dict((nm, nm) for nm in nm_t)}, w_ok, 't')      # the control: the right w passes
    plant_refused('PLANT-FAR-W', 'C-FAR-W t oSS:', lambda: far_tokens(items, {'t': dict((nm, nm) for nm in nm_t)}, dict(w_ok, oSS=1), 't'))
    r6 = Fraction(1e-6)
    ball6 = ([1 - r6, 0, 0, 0], [1 + r6, 0, 0, 0], 0)
    plant_refused('PLANT-Z-A0', 'C-Z-A0 N=4 G,1,1: a0_exact "1" but', lambda: z_const({'a0_exact': '1', 'ak': [1.0, 0.0, 0.0, 0.0],
                                                                                    'ak_rad': [1e-6, 0.0, 0.0, 0.0]}, ball6, 'G,1,1', 4))
    plant_gate('PLANT-Z-MID', lambda: z_const({'a0_exact': None, 'ak': [1.0, 0.0, 0.0, 0.0], 'ak_rad': [1e-6, 0.0, 0.0, 0.0]}, ball6, 'G,1,1', 4)
               == Fraction(1.0), 'an entry without a0_exact: Z_min\'s constant term equals the midpoint a_0')


def main(argv):
    global R
    mode = argv[0] if argv else ''
    if not ((mode == 'cert' and len(argv) == 1) or (mode == 'mock' and len(argv) == 2)):
        print('usage: m4_asm_v1.py cert | mock <mock far kv under code/>')
        return 2
    with open(os.path.abspath(__file__), 'rb') as fh:
        own = sha(fh.read())
    asm_rel = os.path.relpath(os.path.abspath(__file__), CODEDIR)
    print('m4_asm_v1 sha256 %s MODE=%s; file %s; python %s; ctx.prec %d' % (own, mode, asm_rel, sys.version.split()[0], ctx.prec))
    out = OWN + ('/M4_KV_v1.txt' if mode == 'cert' else '/mocks/out/M4_KV_v1_MOCK_%s.txt' % os.path.splitext(os.path.basename(asm_rel))[0])
    try:
        np_, nm, ns = c_hash()
        gate('C-HASH', True, '%d pinned files; the kt_cert run manifest\'s %d entries, %d of them pinned here too, equal' % (np_, nm, ns))
        R = module(READER, 'm4_reader_v1')
        if mode == 'mock':
            R.FIXED['FORMAT'], R.CLAIM = 'M4_KV_v1 MOCK', 'MOCK ' + R.CLAIM
        src_check()
        gate('C-SCAN-PIN', True, 'the %d scan outputs are pinned at kt_cert_v1_8\'s FIXREFS sha256s (l.273-280)' % scan_pins())
        v, count, hd = inputs(mode, argv[1] if mode == 'mock' else None)
        if mode == 'cert':
            far_again = lambda n: far_cert(hd['frd'], n)
        else:
            far_again = lambda n: mock_far(argv[1])[n]
        gate('C-REC', True, '%d kt_cert and x records: first lines, FORMAT, VERDICT, LAWBASE, RESULT and EXPLICIT exactly' % count['rec'])
        gate('C-X-TIE', True, '%d x records: producer and sha256 in kt_cert_v1_8\'s PRODUCERS (l.2169); each g record\'s HANDOFF-READ x line '
                              'names the x record and its HANDOFF sha256' % count['xtie'])
        gate('C-LAW300-NEAR', True, '%d C-NPK, C-NDK and C-TAILM lines, all reading PASS, at least one per record' % count['near'])
        gate('C-MHAT', True, 'M2(b) C-MHAT lines at N = 4 and 3: m1, m2, m3 >= 0 exactly, PASS')
        gate('C-S9-TRIAL', True, 'the S9 records\' trial_set is the pinned ts and vacres files at N = 4 and 3')
        gate('C-Z-A0', len(Z_A0) == 6, 'Z_min\'s constant term is LO_0 = ak_0 - ak_rad_0 of each S9 entry (a0_exact "1" only with a_0 = 1, radius 0): '
             + '; '.join('N%d %s a0_exact %s' % (n, k, Z_A0[(n, k)]) for (n, k) in sorted(Z_A0, key=lambda x: (-x[0], x[1]))))
        gate('C-FAR-W', True, 'FAR_CRUDE_v1: every item\'s weight J-power is at most the record\'s w (the largest over the kinds using its call)'
             if mode == 'cert' else 'MOCK far items (no w; mock run)')
        stamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        text0 = text_of(kvlist(v, own, asm_rel, None, stamp))
        rec0 = R.parse_record(text0)
        l300 = dict(((n, k), R.law(rec0, k, n, 300)) for n in (4, 3) for k in KINDS)
        kv = kvlist(v, own, asm_rel, l300, stamp)
        if mode == 'mock':
            bad = [k for k, x in kv if re.search('certified', x, re.I)]
            if bad:
                raise ValueError('mock: "certified" in the values of %s' % ', '.join(bad))
        text = text_of(kv)
        gate('C-MONO', chernoff_ok(R.A_E_F, R.kappa_b()), 'the Chernoff rates 0.45 a_e/2 and 0.45 kappa_B/2 certainly > 0')
        rec = R.check(text)
        gate('C-MONO-RECORD', True, 'the reader\'s check on the record: C-MONO (C-MONO-FAR4 per far item, C-MONO-GB, Z_min > 0, '
                                    'eps_r(300) < 1), exactly, and C-FMT')
        gate('C-COPY', True, 'the record parsed back: %d copied keys equal their source tokens by exact string equality' % c_copy(text, hd, far_again))
        for n in (4, 3):
            for k in KINDS:
                q = v[n][k]['q']
                gate('C-LAW300 N=%d %s' % (n, k), law300_ok(rec, v, n, k), 'L(300) %s, Q [%s, %s], L/Q_hi - 1 = %+.4f%% (expected %s; allowed '
                     '-1e-4 .. +3e-2)' % (l300[(n, k)], q[0], q[1], 100 * float(Fraction(l300[(n, k)]) / Fraction(q[1]) - 1),
                                          EXPECT.get((n, k), 'about +0.4% .. +0.75%')))
        for n in (4, 3):
            for k in KINDS:
                nf = jnear(n, k)
                worst = min(float(frac_lower(numerator(rec, k, n, J)) / Fraction(nf[J])) - 1 for J in JGATE)
                gate('C-LAW-SCAN N=%d %s' % (n, k), law_scan_ok(rec, k, n, nf), 'the law numerator at J = 400, 500, 600 against the scan near '
                     '(lower end over near - 1, smallest %+.4f%%; allowed -1e-6)' % (100 * worst))
        budget(rec, v)
        plants(text0, text, v, dict(kv), hd, far_again, rec)
    except ValueError as e:
        print('REFUSED: %s' % e)
        FAILS.append('REFUSED')
    if FAILS:
        print('VERDICT INVALID (%s)' % ', '.join(FAILS))
        return 1
    if not (os.path.dirname(out) in (OWN, OWN + '/mocks/out') and not os.path.lexists(out)):
        print('VERDICT INVALID (the record path %s is not new in its own folder)' % out)
        return 1
    with open(out, 'x') as fh:
        fh.write(text)
    os.chmod(out, 0o444)
    print('RECORD %s %s' % (os.path.basename(out), sha(text.encode())))
    print('VERDICT VALID')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
