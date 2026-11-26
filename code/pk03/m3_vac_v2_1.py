#!/usr/bin/env python3
"""m3_vac_v2_1.py -- pk03 (code/pk03/). REVISION of m3_vac_v2.py (bb6fc9fa), whose OFD.4 and OFD.3 stopped at the layer's int64
code guard ("11^19 >= 2^63: split the forms"): v2's formal rebuild kept the model's forms (vertices and pairs) and added the 6 d_uv
and tau, 19 variables with tau up to degree 10. FormsMajorants now uses a compact layout: the pair forms X_q (compact index qidx - V),
the 6 d_uv and tau, 13 variables on E4, E3 and ED alike (11^13 < 2^63). Fbar_0 has no X_v outside D2, so the layout has no X_v slot
and a stray X_v raises. C-P0SUB maps the compact pair index p back to the model's V + p before substituting. From the review's
CHECK_M3_VAC_v2 (6d55c0a7) notes: the stale C-P0T name is gone; PLANT-REP-OF-LAM runs the gate's own has_lam test on the stripped
dict; the chain's OF3 and OF4 estimates are 60 s and 120 s. File names carry v2_1. Everything else is v2's.
m3_vac_v2: REVISION of m3_vac_v1.py (a41c761d), whose OFD.4 and OFD.3 failed C-P0POS alone. P0 = Fbar_0
of the two p factors is built from xibar(u, v, 0) = X_q/2 + t D2(u, v)/(8 (1 - a)) with D2 = X_u^2 - 2 X_u X_v + X_v^2 = (X_u - X_v)^2
(m3_major_v2 7d94b18b l.36-37 and l.88-93, as riglap2): a nonnegative form whose X_u X_v coefficient is negative. So P0's monomial
coefficients are not all >= 0. What the chart law needs (ruled in RULING_N3_P0FORMS_rv01 a873a8c6; the ADD4 laws
item 2 with its erratum 759a99bd) is a polynomial with nonnegative coefficients in nonnegative forms and in t: then P0 >= 0 and
P0(t) <= P0(t_REF) pointwise for 0 <= t <= t_REF. The forms are nonnegative everywhere: X_v = |phi_v|^2, X_q = |phi_u - phi_v|^2 (the
squared n-component forms, m3_graph_v3 l.17-21), d_uv = (X_u - X_v)^2, tau >= 0. C-P0POS is replaced by (the rule's preferred form):
  C-P0FORMS  P0 rebuilt along Fbar(0)'s own code path in formal variables (FormsMajorants): one d_uv per unordered bond pair of the
             p factors for its D2(u, v), and tau for t (m3_major_v2's factor_bar 'p', j = 0, and xibar, l = 0, written out with
             tau^i for t^i and tau/(8 (1 - aa)) for t/(8 (1 - aa)); the expanded polynomial is never factored); every coefficient's
             lower end >= 0. The gate line counts monomials with an X_v factor outside D2 (none expected; X_v >= 0 would cover
             them). PLANT-P0FORMS: one |c_b| negated in the formal build must fail;
  C-P0SUB    d_uv -> D2(u, v) and tau -> t_REF substituted back give the run's P0: the key sets agree (a coefficient on one side only
             must be an exact zero) and every pair of balls overlaps. PLANT-P0SUB: one term dropped in the formal build must fail;
             PLANT-P0SUB-D2 (D2 without its -2 X_u X_v term) and PLANT-P0SUB-T (tau -> 2 t_REF) must fail too.
C-REP-OF also requires the float to have lam* (PLANT-REP-OF-LAM). File names carry v2: the outputs,
the hand-offs and the record m3_vac_N<N>_J150_v2.json. Everything else is v1's.
m3_vac_v1: the CERTIFIED vacuum records of M2(b) (PLAN_M3_CODE_v1_2_ADD4; ADD5_1 sect. 9; ADD6 sect. 3):
for N = 4 or 3 at J_REF = 150, the outer_far items VAC_OF_E4, VAC_OF_E3, VAC_OF_ED and the entries D_Z2 and G4R_0..2 (K = 3), written as
m3_vac_N<N>_J150_v2_1.json in the schema agreed with pk02 (SPEC_M2B_CERT_v1_ADD2 48d5fa54 sect. 1), on the closed layer arbeng_ma_v1_3
with m3_run_v1_7's safeguards: C-HASH, C-IMPORT, C-VALIDATED, C-SERIES, C-PREC, C-CX, C-CX2, PLANT-GUARD, C-FALLBACK-PATH, verdict-bound
hand-offs, the write after every gate and plant, RECORD lines, PLANT-NOWRITE, the bound reader and C-PREC-END.
Items, one at a time, each under its LIM: vD.N (D_Z2: the D graph's prep at J 150 and the entry), vGu<r>.N and vGc<r>.N (G4R_r's prep
stages u and c at dmaxH 12), vGk<r>.N (G4R_r's entry), OF4.N, OF3.N, OFD.N (one graph's outer_far each) and asm.N.
- outer_far (ADD4 sects. 3-4): GraphIV(S_gauge = S) (m3_graph_v3) with C-GAUGE and PLANT-GAUGE; C-GRAPH-REF against m3ref_v1_4's OFJSON;
  P0 = Fbar_0 of the two p factors at radii A_P = binary64 0.9**2 and t_REF = 1/150 (C-P0FORMS and C-P0SUB above; C-P0DEG: degree
  and pair degree as the float's); for lam in {0.5, 1, 1.5} and v in S: rates C_P t_REF + lam e_v rounded up, the tilted law (a lam with
  a tilt not certainly positive definite is skipped; C-OF-LAM: not all three), E_v[P0] = E2(P0, 1) from a TableFB on P0's support with
  caps {1: qP}, and acc_lam = sum_v e^(-lam J_REF a_m) N_v E_v[P0] with a_m = Fraction(0.55)**2; chart = the acc with the smallest upper
  end (lam*). far = sup_F(the two p factors, J_REF) x far_base(J_REF, theta*, A_P, the S-gauge G_vv, tree, N, V, log tau) at m3ref_v1_4's
  theta* (C-MF: m_F = 2); r = min_v theta* A_P/(2 G_vv) - n(V - 1)/(2 J_REF), a lower end. C-REP-OF: certified upper end / float in
  [1 - 1e-6, 1.15] for each lam's chart and for the far part, the float having lam*; C-LAW-OF: lam* >= 0.5 and r >= 0.5 a_m, exactly (PLANT-LAW).
- entries (ADD4 sects. 1-2 and 4): m3_bar_v10's Prep and bound5s at J_REF = 150 with the float references' radii, rho'^2 and theta0
  (C-PREP-REF, REFV): D_Z2 from m3ref_v1_4's vD (radii sqrt(min(80 G_vv/J, 0.6)), rho' 0.7; prep dmaxH 18), G4R_r from m3ref_v1_5's
  vG4ra<r> (vacrig11w l.407's conventions for these graphs, radii sqrt(min(60 G_vv/J, 0.5)), rho' 0.9; prep dmaxH 12, Hoelder above:
  ADD6 sect. 1); C-RULE: the references' radii and rho' follow RULES (PLANT-RULE), checked before the prep; each
  ENTRY line prints its dmaxH; C-TILT, C-MONO-FAR at J_REF 150, C-BUDGET; a0_exact = 1; at asm C-REP-B and C-REP-AK against the same
  references' KEYJSON. C-LIST: these entries are M3_ENTRY_LIST_v1_2's D:Z2 and G4-r:Z,0..2. The record keeps m3_record_v5's top-level
  s_rad 80 and rho_p 0.7 (the S7 rule, which D_Z2 follows) and adds 'rules' (each entry's rule), 'dmaxH' and 'dmaxH_note';
  'families' has each entry's radii^2, rho'^2 and theta0.
- the C-3 (INFO) ran as m3ref_v1_6's vDcal items (out/m3ref_v1_6_vDcal.<N>.all_z9sym.out): vD's prep at dmaxH 12 and 14 against
  18, norm by norm. The record's trial_set names each trial file with its full sha256 (the C-TRIAL).
- asm: C-SCOPE; the record text; C-FMT (m3_reader_v5._check_text); the reader plants (entry and kernel ones as m3_run_v1_7's; outer_far:
  PLANT-OF-CHART, -FAR, -VALUE, -AM-DEC, -AM-B64, -MF, -LAM, -LAMEQ, -R, -CLAIM, -KIND, -ENTKIND, and the (CHECK_M3_VAC_MODULES_v1
  20aeee78 note 1) -LAWJREF (law.J_REF alone at 300), -FIELD-EXTRA and -FIELD-MISSING (an outer_far item with one field more or less);
  PLANT-JREF, PLANT-N); C-BOUND-RT and the five PLANT-BOUND-*; C-PREC-ASM; PLANT-NOWRITE; the write; C-WRITE; the RECORD line.
Run: D=/mnt/g2/release/root/code/pk03; OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=$D/tmp
  timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B $D/m3_vac_v2_1.py ITEM LIM
  > $D/out/m3_vac_v2_1_ITEM.out 2> $D/out/m3_vac_v2_1_ITEM.err
"""
import resource, sys, time, math, hashlib, signal, os, json, re, traceback

ITEM_RE = r'(vD|vGu[0-2]|vGc[0-2]|vGk[0-2]|OF4|OF3|OFD|asm)\.(4|3)'
if len(sys.argv) != 3 or not re.fullmatch(ITEM_RE, sys.argv[1]):
    print('usage: m3_vac_v2_1.py ITEM LIM   (ITEM = vD|vGu0..2|vGc0..2|vGk0..2|OF4|OF3|OFD|asm . 4|3; LIM = RLIMIT_CPU soft limit in s, 5..540)')
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
    'm3_graph_v3.py': '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    'm3_series_v2.py': '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    'm3_major_v2.py': '89dd5a2184a511d4dea39fb3c558501e9738af118be9d41f2ac4b2d4b8d7b016',
    'm3_bar_v10.py': '9a4de5dd54faff8aa3c1c047f870d198d27d12646fbff0c973ce0aff7903a0d5',
    'm3_entries_v3.py': '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    'm3_record_v5.py': 'd59b0a102a622ef49a0379e30248660b4cdb03167fc26747672d367698fbdeef',
    'm3_reader_v5.py': '44b95cfdd4dbffdeb8e970a9ef5dc6cd94320f89e36790a215f7dc710746956c',
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
    (OUTD, 'm3ref_v1_4_vD.4.all_z9sym.out'): 'e08acdb1017b62fec802c9d913e63638425fa99cafa6315a8fd66f5093dd08ac',
    (OUTD, 'm3ref_v1_5_vG4ra0.4.all_z9sym.out'): 'b5e6cef5e3d1e72bb57c7f96895260714c65fd8720c179c684d17d2bc001eba2',
    (OUTD, 'm3ref_v1_5_vG4ra1.4.all_z9sym.out'): 'f5e43f5f789889c3739a32139fd6f0039c191ec8fb4cff6f4f22b7c2708350d9',
    (OUTD, 'm3ref_v1_5_vG4ra2.4.all_z9sym.out'): 'daa625f2ecb0fa6825aa2fcc422e29c49caf142537b898a1a178005933c99fce',
    (OUTD, 'm3ref_v1_4_OF4.4.all_z9sym.out'): '71e16b40c548257e23dee869356ba155b5a5ef4584ed4a2546bb800446227bf7',
    (OUTD, 'm3ref_v1_4_OF3.4.all_z9sym.out'): '3a88c01caf2c14644d0b9ad06d2bd27b53b398137508903d785bcf3c7801b3d7',
    (OUTD, 'm3ref_v1_4_OFD.4.all_z9sym.out'): '540134b4810b474b058d5c6f7f8c5206a3e462aa6f7c0c0bd9706761d714a8b4',
    (OUTD, 'm3ref_v1_4_vD.3.all_z9sym.out'): 'abd71c3b94a71b7841b008f33cf6a1deaff13d81a615b3850bd3e3eecff47f91',
    (OUTD, 'm3ref_v1_5_vG4ra0.3.all_z9sym.out'): '2ca1bdc5087d0771f17e88520d658954c2942a385a74cbf937591af8031b0634',
    (OUTD, 'm3ref_v1_5_vG4ra1.3.all_z9sym.out'): '762492bd4940a22287239eb2be6da43ab4312abc3e4606795a45fcae9b816170',
    (OUTD, 'm3ref_v1_5_vG4ra2.3.all_z9sym.out'): 'c512628f7d249643f22d029623e33ffa272f493b14592add493c9396e419e1cb',
    (OUTD, 'm3ref_v1_4_OF4.3.all_z9sym.out'): 'afbebe643a52314d2c6e1d927bcada0b23292135273b7f15c7cb7665ad53e1c9',
    (OUTD, 'm3ref_v1_4_OF3.3.all_z9sym.out'): '497e0828553da2f12db4f6f3b0572ec7e5f7139a28387fef32996b6f68ec9918',
    (OUTD, 'm3ref_v1_4_OFD.3.all_z9sym.out'): '44315bafd06fd7f2f0d561c0cef856122ae82a395bfe4e169b55336cbd2e165d',
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


SELF_SHA = sha(os.path.abspath(__file__))
out('m3_vac_v2_1 item %s LIM %d; script sha256 %s; python %s' % (ITEM, LIM, SELF_SHA, sys.version.split()[0]))
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
GENERIC = [('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_major', 'm3_major_v2.py'),
           ('m3_bar', 'm3_bar_v10.py'), ('m3_entries', 'm3_entries_v3.py'), ('m3_record', 'm3_record_v5.py'), ('m3_reader', 'm3_reader_v5.py'),
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
G, Model, Majorants = GR, SER.Model, MODS['m3_major'].Majorants
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
J_REF = 150
T_REF = Fraction(1, J_REF)
A_M = REC.A_M                                         # Fraction(0.55)**2: the region boundary agreed with pk02
A_P = 0.9 ** 2                                        # vacrig11f l.245-246 (binary64): the outer_far chart radius rho'^2
DMAXH = {'G4-r0': 12, 'G4-r1': 12, 'G4-r2': 12}       # ADD6 sect. 1: G4 - r has V = 12
RULES = {'D_Z2': {'s_rad': 80.0, 'cap': 0.6, 'rho_p': 0.7}}   # radii sqrt(min(s_rad G_vv/J_REF, cap)) and rho' of each entry's reference
RULES.update({'G4R_%d' % r: {'s_rad': 60.0, 'cap': 0.5, 'rho_p': 0.9} for r in range(3)})   # vacrig11w l.407 (m3ref_v1_5 vG4ra<r>)
DMAXH_NOTE = 'G4-r0, G4-r1, G4-r2: prep dmaxH 12, Hoelder above (riglap4 holder_mono; nE4 3^deg); D: prep dmaxH 18'   # 


def read_lines(path, tag):
    with open(path) as fh:
        return [json.loads(ln[len(tag) + 1:]) for ln in fh if ln.startswith(tag + ' ')]


with open(os.path.join(OWN, 'M3_ENTRY_LIST_v1_2.json')) as fh:
    LIST = json.load(fh)
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]
TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)
TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)])}
VACENT = {'D_Z2': ('D', [['pv', 'L'], ['pv', 'R']], 'D:Z2'), 'G4R_0': ('G4-r0', [], 'G4-r:Z,0'), 'G4R_1': ('G4-r1', [], 'G4-r:Z,1'),
          'G4R_2': ('G4-r2', [], 'G4-r:Z,2')}
REFV = {'D_Z2': 'm3ref_v1_4_vD.%d.all_z9sym.out', 'G4R_0': 'm3ref_v1_5_vG4ra0.%d.all_z9sym.out', 'G4R_1': 'm3ref_v1_5_vG4ra1.%d.all_z9sym.out',
        'G4R_2': 'm3ref_v1_5_vG4ra2.%d.all_z9sym.out'}
REFFAM = {'D_Z2': 'vD', 'G4R_0': 'vG4ra0', 'G4R_1': 'vG4ra1', 'G4R_2': 'vG4ra2'}
OFG = {'E4': (['vac', 'int', 'int', 'vac'], list(range(3, 9)), [(0, 1, 2), (9, 10, 11)], 'm3ref_v1_4_OF4.%d.all_z9sym.out'),
       'E3': (['vac', 'int', 'vac'], list(range(3, 9)), [(0, 1, 2), (6, 7, 8)], 'm3ref_v1_4_OF3.%d.all_z9sym.out'),
       'ED': (['vac', 'vac'], list(range(6)), [(0, 1, 2), (3, 4, 5)], 'm3ref_v1_4_OFD.%d.all_z9sym.out')}
OFITEM = {'OF4': 'E4', 'OF3': 'E3', 'OFD': 'ED'}


def check_list():
    """C-LIST: the vacuum entries are M3_ENTRY_LIST_v1_2's D:Z2 and G4-r:Z,r (graph, r and factors)."""
    ids = {e['id']: e for e in LIST['entries']}
    bad = []
    for key, (graph, encs, lid) in VACENT.items():
        e = ids.get(lid)
        g_ok = e is not None and ((e['graph'] == 'D' and graph == 'D') or (e['graph'] == 'G4-r' and graph == 'G4-r%d' % e.get('r', -1)))
        if not (g_ok and [list(f) for f in e['factors']] == encs):
            bad.append(key)
    gate('C-LIST', not bad, '(%s against M3_ENTRY_LIST_v1_2 ids D:Z2, G4-r:Z,0..2: graph, r and factors)%s' % (
        ', '.join(VACENT), (': ' + ', '.join(bad)) if bad else ''))


def ref_prep(key):
    return read_lines(os.path.join(OUTD, REFV[key] % NN), 'PREPJSON')[0]


def ref_key(key):
    return [d for d in read_lines(os.path.join(OUTD, REFV[key] % NN), 'KEYJSON') if d['key'] == key][0]


def vac_factors(key):
    graph, encs, _ = VACENT[key]
    return [ENT.factor(TS, graph, enc) for enc in encs]


def vac_graph(key):
    return ENT.build_graph(VACENT[key][0], NN, [vac_factors(key)])


def make_prep(key, g, stages, scalars=None):
    rp = ref_prep(key)
    graph = VACENT[key][0]
    ru = RULES[key]
    mid = [(S.up(gv) + S.down(gv)) / 2 for gv in g.Gvv]
    want = [min(ru['s_rad'] * m / J_REF, ru['cap']) for m in mid]
    drule = max([abs(a - w) / w for a, w in zip(rp['a_v'], want)] + [abs(rp['ap'] - ru['rho_p'] ** 2) / ru['rho_p'] ** 2])
    gate('C-RULE', len(want) == len(rp['a_v']) and drule <= 1e-12, '(%s: the reference radii^2 = min(%g G_vv/J_REF, %g) and rho\'^2 = %g^2 '
         '(RULES, the record\'s rules field), G_vv the certified mids: max relative difference %.1e (tol 1e-12))' % (
             key, ru['s_rad'], ru['cap'], ru['rho_p'], drule))
    bad = [min(1.01 * ru['s_rad'] * m / J_REF, 1.01 * ru['cap']) for m in mid]
    plant('PLANT-RULE', not (max(abs(a - w) / w for a, w in zip(rp['a_v'], bad)) <= 1e-12), '(%s: s_rad and cap times 1.01)' % key)
    pr = BAR.Prep(K, g, J_REF, rp['a_v'], rp['ap'], rp['theta0'], 6, log=out, dmaxH=DMAXH.get(graph, 18), stages=stages, scalars=scalars)
    encl = [-iv.log(1 - S.I(a)) / (2 * S.I(a)) * (1 / S.I(J_REF)) for a in rp['a_v']]
    gate('C-TILT', pr.ok and all(S.I(r) >= x.b for r, x in zip(pr.rates, encl)),
         '(%s: (a) %d tilt rates rounded up from their mp.iv enclosures at J_REF %d; (b) both tilts certainly positive definite)' % (
             key, len(pr.rates), J_REF))
    gate('C-PREP-REF', rp['J'] == J_REF and rp['family'] == REFFAM[key] and rp['N'] == NN,
         '(%s: %s PREPJSON of family %s, N %r, J %r; dmaxH %d)' % (key, REFV[key] % NN, rp['family'], rp['N'], rp['J'], DMAXH.get(graph, 18)))
    return pr, rp


def laws_of(pr, mF):
    """U3's laws and Lemma U's far rate (lower end) for an entry with J-degree m_F, at J_REF = 150."""
    g = pr.g
    cF = mF + Fraction(g.n * (g.V - 1), 2)
    rate = pr.alpha_lo - S.I(cF) / J_REF
    return {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': J_REF, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, g.Gvv)]},
            'ann': {'n': g.n, 'J_REF': J_REF, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, pr.tilt_p['Gvv'])]},
            'far_rate': S.down(rate), 'far_cF': str(cF)}, rate


def plant_mono(pr):
    """PLANT-MONO: with theta0 = 1e-3 the far rate must not be certainly positive."""
    g = pr.g
    alpha = min((S.I(1e-3) * S.I(pr.ap) / (2 * gv)).a for gv in g.Gvv)
    rate = alpha - S.I(Fraction(g.n * (g.V - 1), 2)) / J_REF
    plant('PLANT-MONO', not (rate.a > 0), '(theta0 = 1e-3: far rate %.3e)' % S.down(rate))


def compute_vac_entry(pr, key):
    """one vacuum entry at J_REF = 150 (m3_bar_v10 bound5s, K = 3, no budget: these entries have no heavy group norm)."""
    facs = vac_factors(key)
    pr.qcap = 6
    pr.maxrel = 0.0
    t0 = cpu()
    STAGE[0] = 'entry %s' % key
    ak, bars, info = pr.bound(facs, 'std', entry=key)
    laws, rate = laws_of(pr, info['mF'])
    gate('C-MONO-FAR', rate.a > 0, '%s: far rate alpha_min - (m_F + n(V-1)/2)/J_REF = %.4e > 0 (m_F %d, J_REF %d)' % (key, S.down(rate), info['mF'], J_REF))
    rec = REC.entry_record(ak, bars, T_REF, 'free', a0_exact=1, laws=laws)
    barsum = rec['Bp']['rem'] + rec['Bp']['tail'] + rec['Bp']['ann'] + rec['Bp']['far']
    okb = pr.maxrel <= 1e-3 and rec['B']['rnd'] <= 0.1 * barsum
    gate('C-BUDGET', okb, '%s: largest relative radius of a norm %.1e (<= 1e-3), rnd %.2e <= 0.1 x bar %.3e' % (key, pr.maxrel, rec['B']['rnd'], barsum))
    out('AKRAD-INFO %s: largest relative radius of an a_k %.2e' % (key, info.get('ak_relrad', 0.0)))
    out('ENTRY %s dmaxH %d ak %s err %.9e parts rem %.9e tail %.9e ann %.9e far %.9e rnd %.3e groups %d Dn %d forms %d' % (
        key, pr.dmaxH, ['%.12g' % x for x in rec['ak']], rec['err'], rec['B']['rem'], rec['B']['tail'], rec['B']['ann'], rec['B']['far'], rec['B']['rnd'],
        info['groups'], info['Dn'], len(info['forms'])))
    out('STAGE-CPU entry %s %.2f s' % (key, cpu() - t0))
    return {'name': key, 'parity': 'free', 'ak': ak, 'bars': bars, 'a0_exact': 1, 'laws': laws, 'qcap': 6, 'maxrel': pr.maxrel, 'cpu': cpu() - t0}


def run_vd():
    stage('vD: D_Z2 at J_REF %d' % J_REF)
    check_list()
    g = vac_graph('D_Z2')
    pr, rp = make_prep('D_Z2', g, ('u', 'c'))
    out('PREP D_Z2 N=%d: V %d, F %d, J_REF %d, theta0 %r; rE %.6e nC8 %.6e nC6 %.6e farbase %.6e' % (
        NN, g.V, g.F, J_REF, rp['theta0'], float(pr.rE.mid), float(pr.nC8.mid), float(pr.nC6.mid), float(pr.farbase.b)))
    plant_mono(pr)
    res = [compute_vac_entry(pr, 'D_Z2')]
    write_handoff('vD', {'family': 'vD', 'entries': res, 'scal_u': pr.scalars_out('u'), 'scal_c': pr.scalars_out('c'), 'fallbacks': fb_info()})


def run_vg_stage(r, stg):
    key = 'G4R_%d' % r
    stage('%s prep stage %s (dmaxH %d)' % (key, stg, DMAXH['G4-r%d' % r]))
    g = vac_graph(key)
    pr, rp = make_prep(key, g, (stg,))
    if stg == 'c':
        plant_mono(pr)
    write_handoff('vG%d' % r, {'family': 'vG%d' % r, 'stage': stg, 'scal': pr.scalars_out(stg), 'fallbacks': fb_info()})


def run_vg_entry(r):
    key = 'G4R_%d' % r
    stage('%s entry' % key)
    su = read_handoff('vGu%d.%d' % (r, NN), 'vG%d' % r)['scal']
    sc = read_handoff('vGc%d.%d' % (r, NN), 'vG%d' % r)['scal']
    g = vac_graph(key)
    pr, rp = make_prep(key, g, (), scalars=dict(su, **sc))
    res = [compute_vac_entry(pr, key)]
    write_handoff('vG%d' % r, {'family': 'vG%d' % r, 'entries': res, 'fallbacks': fb_info()})


C_P_IV = -iv.log(1 - S.I(A_P)) / (2 * S.I(A_P))       # vacrig11f l.247 in mp.iv


class FormsMajorants(Majorants):
    """m3_major_v2.Majorants (7d94b18b) for P0 = Fbar_0 of 'p' factors in formal variables (C-P0FORMS), in a compact layout: the graph's
    pair forms X_q at indices 0..NP-1 (qidx - V), d_uv at NP + b for each listed bond's D2(u, v) = X_u^2 - 2 X_u X_v + X_v^2, and tau at
    NP + len(bonds) for t; no X_v slot. factor_bar ('p', j = 0: l = 0 only, so cf = t^i |c_b|) and xibar (l = 0) are m3_major_v2's
    l.112-124 and l.92 with tau^i for S.ipow(t, i) and tau/(8 (1 - aa)) for t/(8 (1 - aa)); any other factor kind, j or l raises.
    plant: None, 'flip' (the first nonzero |c_b| negated: PLANT-P0FORMS) or 'drop' (that term left out: PLANT-P0SUB)."""
    def __init__(self, kern, model, avec, t, bonds, plant=None):
        super().__init__(kern, model, avec, t)
        self.bonds = list(bonds)
        self.plant, self.planted = plant, False
        self.NP = len(self.g.pairs)
        self.ITAU = self.NP + len(self.bonds)
        self.NV = self.ITAU + 1
        self.ONE = self.mono([0] * self.NV, 1)
        self.ZERO = kern.SPoly(self.NV)

    def D2(self, i, j):
        b = self.bonds.index((i, j)) if (i, j) in self.bonds else self.bonds.index((j, i))
        return self.xv(self.NP + b, 1)

    def tau(self, k):
        return self.ONE if k == 0 else self.xv(self.ITAU, k)

    def xibar(self, u, v, l, aa):
        if l != 0:
            raise ValueError('FormsMajorants: only xibar(., 0) enters P0')
        return self.xv(self.g.qidx(u, v) - self.g.V, 1, Fraction(1, 2)).add(self.D2(u, v).mul(self.tau(1)).scale(S.ka(1 / (8 * (1 - aa)))))

    def factor_bar(self, f, j):
        if f[0] != 'p' or j != 0:
            raise ValueError('FormsMajorants: only factor_bar of a p factor at j = 0 enters P0')
        _, col, q1, q2, q3 = f
        T, M, Bv = col
        prs = [(T, M), (M, Bv), (T, Bv)]
        out = self.ONE
        for i, coef in ((1, q1), (2, q2), (3, q3)):
            for cb, mono in zip(coef, SER.BASIS9):
                if cb == 0.0:
                    continue
                sgn = 1
                if self.plant is not None and not self.planted:
                    self.planted = True
                    if self.plant == 'drop':
                        continue
                    sgn = -1
                out = out.add(self._fbd(prs, mono, 0).mul(self.tau(i)).scale(S.ka(sgn * S.I(abs(cb)))))
        return out


def p0_bonds(pf):
    """the unordered bond pairs (u, v) whose D2 enters the p factors' xibar (m3_major_v2.factor_bar: (T, M), (M, B), (T, B) of each
    column), each listed once."""
    out = []
    for f in pf:
        T, M, Bv = f[1]
        for u, v in ((T, M), (M, Bv), (T, Bv)):
            if (u, v) not in out and (v, u) not in out:
                out.append((u, v))
    return out


def p0_forms(g, pf, plant=None):
    """P0 = Fbar_0 of the p factors at radii A_P in the compact formal layout: (the polynomial, the bonds, NP, the index of tau)."""
    bonds = p0_bonds(pf)
    mjf = FormsMajorants(K, Model(K, g, 3, pf), [A_P] * g.V, T_REF, bonds, plant=plant)
    return mjf.Fbar(0), bonds, mjf.NP, mjf.ITAU


def p0_substitute(P0f, bonds, npair, itau, mj, t, drop_cross=False):
    """P0f with each compact X_q moved back to the model's index V + p, each d_uv replaced by mj.D2(u, v) (for a plant: by
    X_u^2 + X_v^2) and tau by t, as a polynomial in mj's variables."""
    d2 = [mj.xv(u, 2).add(mj.xv(v, 2)) if drop_cross else mj.D2(u, v) for u, v in bonds]
    pw = {}
    out = mj.ZERO
    for e, c in P0f.to_arb_dict().items():
        em = [0] * mj.NV
        for p_ in range(npair):
            em[mj.g.V + p_] = e[p_]
        term = mj.mono(em, c)
        for b, k in enumerate(e[npair:itau]):
            if k:
                if (b, k) not in pw:
                    pw[(b, k)] = d2[b].power(k)
                term = term.mul(pw[(b, k)])
        if e[itau]:
            term = term.scale(S.ka(S.ipow(S.I(t), e[itau])))
        out = out.add(term)
    return out


def poly_match(A, B):
    """the C-P0SUB test: (the key sets agree, a coefficient on one side only being an exact zero, and every pair of balls
    overlaps; the number of one-sided keys that are not exact zeros; the largest gap between non-overlapping balls)."""
    a, b = S.spoly_iv(A), S.spoly_iv(B)
    ok, onesided, gap = True, 0, 0.0
    for e in set(a) | set(b):
        if e not in a or e not in b:
            x = a[e] if e in a else b[e]
            if not (x.a == 0 and x.b == 0):
                ok, onesided = False, onesided + 1
            continue
        x, y = a[e], b[e]
        if x.a > y.b:
            ok, gap = False, max(gap, S.up(x.a - y.b))
        elif y.a > x.b:
            ok, gap = False, max(gap, S.up(y.a - x.b))
    return ok, onesided, gap


def of_graph(gname):
    cols, Sg, pcols, _ = OFG[gname]
    V, E = G.strip(cols)
    prs = []
    for c_ in pcols:
        prs += [(c_[0], c_[1]), (c_[1], c_[2]), (c_[0], c_[2])]
    g = G.GraphIV(V, E, prs, NN, S_gauge=Sg)
    return g, E, [TS.pv(tuple(c_)) for c_ in pcols], Sg, pcols


def run_of(gname):
    """one graph's outer_far at J_REF = 150 (ADD4 sects. 3-4; ADD6 sect. 3): the chart part for lam in {0.5, 1, 1.5} (a lam whose tilt is
    not certainly positive definite is skipped; all three skipped fails C-OF-LAM) and the truly far part at m3ref_v1_4's theta*."""
    stage('outer_far %s' % gname)
    g, E, pf, Sg, pcols = of_graph(gname)
    okg, why = g.check_gauge()
    gate('C-GAUGE', okg, '(%s N=%d, S = %s: %s)' % (gname, NN, Sg, why))
    Bbad = [row[:] for row in g.Bm]
    Bbad[g.s0] = [0] * (g.V - 1)
    plant('PLANT-GAUGE', not g.check_gauge(Bbad)[0], '(%s: the basis with its pivot row zeroed must fail C-GAUGE)' % gname)
    ref = read_lines(os.path.join(OUTD, OFG[gname][3] % NN), 'OFJSON')[0]
    ec = sorted((tuple(e), G.coupling_float(c)) for e, c in E)
    ef = sorted((tuple(e), c) for e, c in ref['edges'])
    gate('C-GRAPH-REF', ec == ef and ref['V'] == g.V and ref['S'] == Sg and ref['pcols'] == [list(c_) for c_ in pcols] and ref['N'] == NN,
         '(%s: %d edges with binary64 couplings, V, S and pcols equal m3ref_v1_4\'s OFJSON)' % (gname, len(E)))
    mj = Majorants(K, Model(K, g, 3, pf), [A_P] * g.V, T_REF)
    P0 = mj.Fbar(0)
    coefs = S.spoly_iv(P0)
    P0f, bonds, npair, itau = p0_forms(g, pf)
    cf = S.spoly_iv(P0f)
    gate('C-P0FORMS', all(c.a >= 0 for c in cf.values()), '(%s: all %d coefficients of P0 in the compact forms X_q (%d pairs), d_uv (%d '
         'bonds) and tau have lower ends >= 0; the layout has no X_v slot, so a stray X_v would have raised)' % (gname, len(cf), npair,
                                                                                                                len(bonds)))
    cfl = S.spoly_iv(p0_forms(g, pf, plant='flip')[0])
    plant('PLANT-P0FORMS', not all(c.a >= 0 for c in cfl.values()), '(%s: one |c_b| negated in the formal build)' % gname)
    okS, oneS, gapS = poly_match(p0_substitute(P0f, bonds, npair, itau, mj, T_REF), P0)
    gate('C-P0SUB', okS, '(%s: X_q back to V + p, d_uv -> D2(u, v) and tau -> t_REF give the run\'s P0 (%d coefficients): key sets agree '
         '(one-sided keys that are not exact zeros: %d) and every pair of balls overlaps (largest gap %.3e))' % (gname, len(coefs), oneS, gapS))
    Pdr, bdr, npdr, itdr = p0_forms(g, pf, plant='drop')
    okD = poly_match(p0_substitute(Pdr, bdr, npdr, itdr, mj, T_REF), P0)[0]
    plant('PLANT-P0SUB', not okD, '(%s: one term dropped in the formal build)' % gname)
    okB = poly_match(p0_substitute(P0f, bonds, npair, itau, mj, T_REF, drop_cross=True), P0)[0]
    plant('PLANT-P0SUB-D2', not okB, '(%s: D2 without its -2 X_u X_v term)' % gname)
    okT = poly_match(p0_substitute(P0f, bonds, npair, itau, mj, 2 * T_REF), P0)[0]
    plant('PLANT-P0SUB-T', not okT, '(%s: tau -> 2 t_REF)' % gname)
    degP, qP = BAR.deg(P0), BAR.qdeg(P0, g.V)
    gate('C-P0DEG', degP == ref['degP'] and qP == ref['qP'], '(%s: deg P0 %d and its pair degree %d; the float\'s %d, %d)' % (
        gname, degP, qP, ref['degP'], ref['qP']))
    idx = BAR.support(P0)
    P0r = BAR.restrict(K, P0, idx)
    one = S.spoly(K, {tuple([0] * len(idx)): 1}, len(idx))
    rate0 = C_P_IV * S.I(T_REF)
    acc, okl = {}, {}
    for lam in (0.5, 1.0, 1.5):
        terms, ok = [], True
        for v in Sg:
            t1 = cpu()
            rates = [S.up(rate0)] * g.V
            rates[v] = S.up(rate0 + S.I(lam))
            tl = g.tilted(rates)
            if tl is None:
                ok = False
                out('OF-LAM %s lam %r: the tilt at v = %d is not certainly positive definite; lam skipped' % (gname, lam, v))
                break
            Gam, Wi, gr = g.restrict(tl['Gam'], idx)
            tab = BAR.TableFB(K, S.arb_mat_of(Gam), g.n, max(degP, 1), gr, {1: max(qP, 1)}, Wi, '%s lam %r v %d' % (gname, lam, v))
            Ev = S.nonneg(S.arb_to_iv(tab.E2(P0r, one)))
            terms.append(iv.exp(-S.I(lam) * S.I(J_REF) * S.I(A_M)) * tl['N'] * Ev)
            out('OF-UNIT %s lam %r v %d: N %.6e E[P0] %.6e (%.2f s)' % (gname, lam, v, float(tl['N'].mid), float(Ev.mid), cpu() - t1))
        okl[str(lam)] = ok
        acc[str(lam)] = S.isum(terms) if ok else None
    oks = [lam for lam in (0.5, 1.0, 1.5) if okl[str(lam)]]
    gate('C-OF-LAM', bool(oks), '(%s: certainly positive definite tilts for lam %s; all three skipped is a hard failure)' % (gname, oks))
    lam_star = min(oks, key=lambda lam: S.up(acc[str(lam)]))
    chart = acc[str(lam_star)]
    supF, mF = BAR.sup_F(pf, J_REF)
    gate('C-MF', mF == 2, '(%s: the J-degree of the two p factors m_F = %d, the law\'s exponent 2)' % (gname, mF))
    th = ref['theta_star']
    tree = g.tree()
    fb = S.far_base(S.I(J_REF), S.I(th), S.I(A_P), g.Gvv, tree, g.N, g.V, g.log_tau)
    far = supF * fb
    rlo = min(S.down(S.I(th) * S.I(A_P) / (2 * gv)) for gv in g.Gvv)
    r_iv = S.I(rlo) - S.I(Fraction(g.n * (g.V - 1), 2 * J_REF))
    reps = []
    for lam in oks:
        fl = ref['chart_per_lam'].get(str(lam))
        if fl:
            reps.append(('chart lam %r' % lam, S.up(acc[str(lam)]) / fl))
    reps.append(('far', S.up(far) / ref['far']))
    lo_, hi_ = min(x[1] for x in reps), max(x[1] for x in reps)
    has_lam = lambda d_, lam: bool(d_.get(str(lam)))
    has_star = has_lam(ref['chart_per_lam'], lam_star)
    gate('C-REP-OF', has_star and 1 - 1e-6 <= lo_ and hi_ <= 1.15, '(%s: certified upper end / float, %s; the float has lam* %r: %s)' % (
        gname, ', '.join('%s %.9f' % (k, float(v)) for k, v in reps), lam_star, has_star))
    nostar = {k: v for k, v in ref['chart_per_lam'].items() if k != str(lam_star)}
    plant('PLANT-REP-OF-LAM', not has_lam(nostar, lam_star), '(%s: the gate\'s lam* test on the float\'s chart_per_lam without lam*)' % gname)
    law_ok = lambda lam, rl: Fraction(lam) >= Fraction(1, 2) and Fraction(rl) >= Fraction(1, 2) * A_M
    okr = law_ok(lam_star, S.down(r_iv))
    gate('C-LAW-OF', okr, '(%s: lam* %r >= 0.5; r %.9e >= 0.5 a_m %.9e, compared exactly; theta* %r)' % (
        gname, lam_star, S.down(r_iv), float(Fraction(1, 2) * A_M), th))
    rbad = float(Fraction(1, 2) * A_M)
    while Fraction(rbad) >= Fraction(1, 2) * A_M:
        rbad = math.nextafter(rbad, 0.0)
    plant('PLANT-LAW', not law_ok(0.4, S.down(r_iv)) and not law_ok(lam_star, rbad), '(lam* 0.4, and r the binary64 just below 0.5 a_m, must each fail C-LAW-OF)')
    out('OF-VALUE %s: chart %.9e (lam* %r), far %.9e (supF %.6f x farbase %.6e), value %.9e' % (
        gname, S.up(chart), lam_star, S.up(far), float(supF.mid), S.up(fb), S.up(S.isum([chart, far]))))
    write_handoff(OFITEM_INV[gname], {'family': OFITEM_INV[gname], 'acc': acc, 'ok': okl, 'lam_star': lam_star, 'chart': chart, 'far': far,
                                      'farbase': fb, 'supF': supF, 'theta_star': th, 'r': r_iv, 'mF': mF, 'degP': degP, 'qP': qP,
                                      'GS': g.Gvv, 'fallbacks': fb_info()})


OFITEM_INV = {v: k for k, v in OFITEM.items()}


def header(fam):
    return {'script': SELF_SHA, 'item': ITEM, 'family': fam, 'N': NN, 'kernel': '%s:%s' % (KERNEL, KFILES[KERNEL + '.py'][:8]),
            'arb_kernel': '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), 'trial': TRIAL, 'format': 'm3_vac_v2_1 hand-off'}




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
    name = 'm3_vac_v2_1_%s.json' % ITEM
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
    name = 'm3_vac_v2_1_%s.json' % item
    hdr, body = HO.read(name, os.path.join(OUTD, 'm3_vac_v2_1_%s.out' % item), {'script': SELF_SHA, 'item': item, 'N': NN, 'family': fam},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (name, valid_verdict()))
    return body


FILES = ('vac',)


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


def reader_refuses(text, jref=J_REF, nexp=None, name='<plant>'):
    try:
        RDR._check_text(text, jref, NN if nexp is None else nexp, name)
        return False
    except ValueError:
        return True


def run_asm():
    stage('asm')
    res = {}
    for item, fam in [('vD.%d' % NN, 'vD')] + [('vGk%d.%d' % (r_, NN), 'vG%d' % r_) for r_ in range(3)]:
        for r in read_handoff(item, fam)['entries']:
            res[r['name']] = r
    ofs = {gname: read_handoff('%s.%d' % (OFITEM_INV[gname], NN), OFITEM_INV[gname]) for gname in OFG}
    gate('C-SCOPE', set(res) == set(VACENT) and set(ofs) == set(OFG), '(entries %s; outer_far %s)' % (', '.join(sorted(res)), ', '.join(sorted(ofs))))
    items = {}
    for key in VACENT:
        r = res[key]
        items[key] = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=1, laws=r['laws'])
    rep, rak = [], []
    for key in VACENT:
        d = ref_key(key)
        for p in ('rem', 'tail', 'ann', 'far'):
            if d['B'][p] > 0:
                rep.append((items[key]['B'][p] / d['B'][p], key, p))
        for k, (a, fa) in enumerate(zip(res[key]['ak'], d['ak'])):
            rak.append((abs(float(a.mid) - fa) / max(1.0, abs(fa)), key, k))
    lo_, hi_ = min(rep), max(rep)
    gate('C-REP-B', 1 - 1e-6 <= lo_[0] and hi_[0] <= 1.15, '(%d bar parts against the float references (REFV) z9sym at J 150: certified/float in [%.9f (%s %s), %.6f (%s %s)])' % (
        len(rep), lo_[0], lo_[1], lo_[2], hi_[0], hi_[1], hi_[2]))
    plant('PLANT-REPB', not (1 - 1e-6 <= lo_[0] * 0.5), '(the smallest ratio times 0.5)')
    wr = max(rak)
    gate('C-REP-AK', wr[0] <= 1e-9, '(%d a_k against the float references (REFV) z9sym: largest |certified mid - float| / max(1, |float|) %.2e at %s a_%d)' % (
        len(rak), wr[0], wr[1], wr[2]))
    plant('PLANT-REPAK', not (wr[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')
    for gname, b in ofs.items():
        items['VAC_OF_' + gname] = REC.outer_far_record(b['chart'], b['far'], b['lam_star'], b['theta_star'], b['r'], J_REF, r_parts={
            'farbase_hi': S.up(b['farbase']), 'supF_hi': S.up(b['supF']),
            'chart_per_lam_hi': {k: (S.up(v) if v is not None else None) for k, v in b['acc'].items()}})
    # the text, C-FMT on the text, the plants, and only then the write
    tag = TAG
    eng = {'m3_vac_v2_1': SELF_SHA, 'modules': dict(OWNMOD)}
    kern = {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}
    fams = {key: {k: ref_prep(key)[k] for k in ('a_v', 'ap', 'theta0')} for key in VACENT}
    top = REC.top_level(NN, J_REF, fams, TRIAL, eng, tag, kern, extra={'A_M': str(A_M), 'A_P': A_P, 'dmaxH': DMAXH, 'rules': RULES,
        'dmaxH_note': DMAXH_NOTE})
    texts = {'vac': json.dumps(dict(top, items=items))}
    paths = {'vac': os.path.join(OUTD, 'm3_vac_N%d_J150%s_v2_1.json' % (NN, tag))}
    vn = os.path.basename(paths['vac'])
    rd = RDR._check_text(texts['vac'], J_REF, NN, name=vn)
    okf = all(rd['entries'][k] == (items[k]['ak'], items[k]['err']) for k in VACENT) and all(
        RDR.outer_far(rd, 'VAC_OF_' + gname)['chart'] == items['VAC_OF_' + gname]['chart'] and
        RDR.outer_far(rd, 'VAC_OF_' + gname)['far'] == items['VAC_OF_' + gname]['far'] for gname in OFG)
    gate('C-FMT', okf, '(%s: %d entries and %d outer_far items read back exactly from the text by m3_reader_v5; %d bytes; sha256 %s)' % (
        vn, len(VACENT), len(OFG), len(texts['vac']), tsha(texts['vac'])))

    def mut(fn):
        d = json.loads(texts['vac'])
        fn(d)
        return json.dumps(d)
    deny = dict(DENY)
    half = Fraction(1, 2) * A_M
    rb = float(half)
    while Fraction(rb) >= half:
        rb = math.nextafter(rb, 0.0)
    E4i = lambda d: d['items']['VAC_OF_E4']
    kr = max((k for k in items if items[k].get('kind') == 'entry'), key=lambda k: sum(items[k]['ak_rad']))
    plants = [
        ('PLANT-FMT', lambda d: d['items']['D_Z2']['B'].pop('rnd')),
        ('PLANT-RND', lambda d: d['items'][kr]['B'].__setitem__('rnd', 0.0)),
        ('PLANT-READER-PRECERT', lambda d: (d.__setitem__('format', 'M3_RECORD_v1_PRECERT'), d.__setitem__('claim', 'NOT CERTIFIED (PRECERT): ' + d['claim']))),
        ('PLANT-READER-KERNEL', lambda d: d.__setitem__('kernel_sha256', flip(d['kernel_sha256']))),
        ('PLANT-READER-PREC', lambda d: d.__setitem__('kernel_prec', 256)),
        ('PLANT-LAYER-V1_1', lambda d: (d.__setitem__('kernel_file', 'arbeng_ma_v1_1.py'), d.__setitem__('kernel_sha256', deny['arbeng_ma_v1_1.py']))),
        ('PLANT-LAYER-V1_2', lambda d: (d.__setitem__('kernel_file', 'arbeng_ma_v1_2.py'), d.__setitem__('kernel_sha256', deny['arbeng_ma_v1_2.py']))),
        ('PLANT-CLAIM', lambda d: d.__setitem__('claim', d['claim'] + ' ')),
        ('PLANT-ARBK', lambda d: d.__setitem__('arb_kernel_sha256', flip(d['arb_kernel_sha256']))),
        ('PLANT-ARBB', lambda d: d.__setitem__('arb_base_sha256', flip(d['arb_base_sha256']))),
        ('PLANT-KIND', lambda d: d['items']['G4R_0'].pop('kind')),
        ('PLANT-OF-CHART', lambda d: E4i(d).__setitem__('chart', -1e-12)),
        ('PLANT-OF-FAR', lambda d: E4i(d).__setitem__('far', -1e-12)),
        ('PLANT-OF-VALUE', lambda d: E4i(d).__setitem__('value', 0.5 * E4i(d)['far'])),
        ('PLANT-OF-AM-DEC', lambda d: E4i(d)['law'].__setitem__('a_m', '121/400')),
        ('PLANT-OF-AM-B64', lambda d: E4i(d)['law'].__setitem__('a_m', str(Fraction(0.55 ** 2)))),
        ('PLANT-OF-MF', lambda d: E4i(d)['law'].__setitem__('mF', 3)),
        ('PLANT-OF-LAM', lambda d: (E4i(d).__setitem__('lam_star', 0.4), E4i(d)['law'].__setitem__('lam_star', 0.4))),
        ('PLANT-OF-LAMEQ', lambda d: E4i(d)['law'].__setitem__('lam_star', 1.5 if E4i(d)['lam_star'] != 1.5 else 1.0)),
        ('PLANT-OF-R', lambda d: E4i(d)['law'].__setitem__('r', rb)),
        ('PLANT-OF-CLAIM', lambda d: E4i(d).__setitem__('law_claim', E4i(d)['law_claim'] + ' ')),
        ('PLANT-OF-KIND', lambda d: E4i(d).__setitem__('kind', 'entry')),
        ('PLANT-OF-ENTKIND', lambda d: d['items']['D_Z2'].__setitem__('kind', 'outer_far')),
        ('PLANT-OF-LAWJREF', lambda d: E4i(d)['law'].__setitem__('J_REF', 300)),
        ('PLANT-OF-FIELD-EXTRA', lambda d: E4i(d).__setitem__('note', 'x')),
        ('PLANT-OF-FIELD-MISSING', lambda d: E4i(d).pop('r_parts')),
    ]
    for lab, fn in plants:
        plant(lab, reader_refuses(mut(fn)), '(m3_reader_v5 must refuse this copy of the vacuum record)')
    plant('PLANT-JREF', reader_refuses(texts['vac'], jref=300), '(the J_REF-150 record read at expected J_REF 300)')
    plant('PLANT-N', reader_refuses(texts['vac'], nexp=3 if NN == 4 else 4), '(read with the other N)')
    vh = tsha(texts['vac'])
    try:
        RDR.loads(texts['vac'], 'RECORD %s %s\nVERDICT VALID\n' % (vn, vh), J_REF, NN, vn)
        gate('C-BOUND-RT', True, '(m3_reader_v5.loads accepts the record under an output that names it and ends VALID)')
    except ValueError as ex:
        gate('C-BOUND-RT', False, '(refused: %s)' % ex)
    for lab, otext in (('PLANT-BOUND-VERDICT', 'RECORD %s %s\nVERDICT VALID-PRECERT\n' % (vn, vh)),
                       ('PLANT-BOUND-INVALID', 'RECORD %s %s\nVERDICT INVALID (C-REP-B)\n' % (vn, vh)),
                       ('PLANT-BOUND-TWO', 'RECORD %s %s\nVERDICT VALID\nVERDICT VALID\n' % (vn, vh)),
                       ('PLANT-BOUND-SHA', 'RECORD %s %s\nVERDICT VALID\n' % (vn, flip(vh))),
                       ('PLANT-BOUND-NONE', 'VERDICT VALID\n')):
        try:
            RDR.loads(texts['vac'], otext, J_REF, NN, vn)
            plant(lab, False, '(m3_reader_v5.loads must refuse this asm output)')
        except ValueError:
            plant(lab, True, '(m3_reader_v5.loads refuses this asm output)')
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
    if FAM == 'vD':
        run_vd()
    elif FAM[:3] in ('vGu', 'vGc'):
        run_vg_stage(int(FAM[3]), FAM[2])
    elif FAM[:3] == 'vGk':
        run_vg_entry(int(FAM[3]))
    elif FAM in OFITEM:
        run_of(OFITEM[FAM])
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
