"""cplus_sidecheck_v1.py -- pk07 (code/pk07/). The one-off certified side check of Lemma 19.2 (c+)'s hypothesis for the certified
vertical export pk07/out/export_kt_s9h_v1_2_vsweep.kv (761084be), to the SPEC_CPLUS_SIDECHECK_rv01.md 1c2eef3c, Part A (the
row 5 decision (a)).

- C-HASH: the full sha256 of the bytes read must equal each of the three pins (the export, kt_s9h_v1_2.py, M2B_KV_v1).
- kt_s9h_v1_2.py is loaded unchanged, from the very bytes C-HASH checked (compiled from them, no edit, no monkeypatching), under the name
  kt_s9h_v1_2 (so its main() does not run), with the export run's mode globals: vsweep, LIM 60. Its TAG is set to cplus only because the
  module opens its own out/out_<label>_<mode>[_<TAG>].out with mode 'x' and the export run's own output exists; TAG changes nothing else
  the module computes before main().
- A0: the module's provide_m2b(fails, fires) in certified mode, with fails == [] and fires == [].
- check(K_N, sc) per N with sc = {}: A1 er, sv = the upper ends of vac_law_v1(dict(M2B=K_N), 300.0, sc), R = K_N['RTR'] * sc.get('Rtr',
  1.0); A2 den = 2 - R - er > 0 certainly; A3 sv < 1 certainly; A4 g = den - er/sqrt(1 - sv^2) > 0 certainly; A5 (INFO) er and sv beside the
  record's N*_EPS_R_300 and N*_S_300.
- PLANT-CPLUS-G per N: check(K_N, {'Rtr': f}) with f = (2 - 2.2 er)/K_N['RTR']: vac_law_v1 must not raise, A2 and A3 must pass, A4 must fail.
- The record out/cplus_sidecheck_v1.kv (FORMAT = CPLUS_SIDECHECK_v1, written with mode 'x'); the module's own log
  out/out_kt_s9h_v1_2_vsweep_cplus.out is pinned in it by sha256. J = 300 covers every J >= 300 through C-VACMONO (in A0), as the spec argues.

Run through the wrapper only, under the approval (cap 0.02 core-h)."""
import hashlib, os, sys, types

CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk07'
OUTD = OWN + '/out'
REC = os.path.join(OUTD, 'cplus_sidecheck_v1.kv')
PINS = dict(EXPORT=('pk07/out/export_kt_s9h_v1_2_vsweep.kv', '10f3c3d9a18b9c7a596121a8dbec7d2b82afb366704845a7c00e066c8bf6d4f6'),
            CODE=('pk07/kt_s9h_v1_2.py', '1b68e47141dfc5e873e2660711f6430a0badc9cc948ada32eb11641fabde4ff4'),
            M2B=('pk02/M2B_KV_v1.txt', '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d'))
MODULE_ARGV = ['vsweep', '60', 'cplus']        # the export run's mode globals (vsweep), LIM 60, TAG cplus (see the docstring)
CLAIM = ('For N in {3, 4} and every J >= 300 (t in (0, 1/300], t -> 0 included): 2 - R_tr - eps_r(J) - eps_r(J)/sqrt(1 - s(J)^2) > 0, '
         'with eps_r(J) and s(J) = eps_r(J)/(2 - R_tr - eps_r(J)) by LAW v1 on M2B_KV_v1 and R_tr its RTR. This is the hypothesis of Lemma '
         '19.2 (c+) (NOTE_LEMMA_19_2_CPLUS_rv01.md), so lambda_0 <= (1 + eps_r) mu-hat holds wherever export 761084be uses it.')

if not (os.path.isdir(OUTD) and os.path.realpath(os.path.dirname(REC)) == os.path.realpath(OUTD)
        and os.path.realpath(OUTD).startswith(os.path.realpath(OWN) + os.sep)):
    print('output directory check failed for %s' % REC)
    sys.exit(2)
if os.path.exists(REC):
    print('record exists: %s' % REC)
    sys.exit(2)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def write_record(lines):
    with open(REC, 'x') as fh:
        for ln in lines:
            fh.write(ln + '\n')


with open(os.path.abspath(__file__), 'rb') as fh:
    OWN_SHA = sha_bytes(fh.read())
head = ['FORMAT = CPLUS_SIDECHECK_v1', 'SCRIPT = pk07/cplus_sidecheck_v1.py:%s' % OWN_SHA]
raw, bad = {}, []
for k, (path, pin) in PINS.items():
    with open(os.path.join(CODEDIR, path), 'rb') as fh:
        raw[k] = fh.read()
    head.append('INPUT_%s = %s:%s' % (k, path, sha_bytes(raw[k])))
    if sha_bytes(raw[k]) != pin:
        bad.append('C-HASH %s' % k)
if bad:
    write_record(head + ['CLAIM = ' + CLAIM, 'VERDICT = INVALID (%s)' % ', '.join(bad)])
    print('INVALID: %s' % ', '.join(bad))
    sys.exit(1)

# the module, from the checked bytes, with the export run's mode globals
code_path = os.path.join(CODEDIR, PINS['CODE'][0])
sys.argv = [code_path] + MODULE_ARGV
mod = types.ModuleType('kt_s9h_v1_2')
mod.__file__ = code_path
try:
    exec(compile(raw['CODE'].decode('utf-8'), code_path, 'exec'), mod.__dict__)
except SystemExit as e:
    write_record(head + ['CLAIM = ' + CLAIM, 'VERDICT = INVALID (the module stopped at load: exit %r)' % (e.code,)])
    print('INVALID: the module stopped at load')
    sys.exit(1)
pt, iv, dec_iv, dec_dir = mod.pt, mod.iv, mod.dec_iv, mod.dec_dir


def check(K, sc):
    """A1-A4 on one N (SPEC Part A); returns the values and the three results."""
    V = mod.vac_law_v1(dict(M2B=K), 300.0, sc)
    er, sv = pt(V['eps_r'].b), pt(V['s'].b)
    R = K['RTR'] * sc.get('Rtr', 1.0)
    den = 2 - R - er
    a2, a3 = (den > 0) is True, (sv < 1) is True
    g = (den - er / iv.sqrt(1 - sv * sv)) if a3 else None
    a4 = a3 and (g > 0) is True
    return dict(er=er, sv=sv, R=R, den=den, g=g, a2=a2, a3=a3, a4=a4)


rec_kv = {}
for ln in raw['M2B'].decode('utf-8').split('\n'):
    if ' = ' in ln and not ln.startswith('#'):
        k_, v_ = ln.split(' = ', 1)
        rec_kv[k_] = v_
fails, fires = [], []
try:
    KS = mod.provide_m2b(fails, fires)
    a0 = fails == [] and fires == []
except (ArithmeticError, ValueError, RuntimeError, KeyError) as e:
    KS, a0 = None, False
    fails.append('provide_m2b raised: %r' % (e,))
body = ['PROVIDER = fails %r ; fires %r' % (fails, fires), 'A0 = %s' % ('PASS' if a0 else 'FAIL')]
why = [] if a0 else ['A0']
for N in (4, 3):
    if KS is None:
        why.append('N=%d not checked' % N)
        continue
    p = 'N%d_' % N
    r = check(KS[N], {})
    body += [p + 'RTR_LO = ' + dec_dir(r['R'], False), p + 'RTR_HI = ' + dec_dir(r['R'], True),
             p + 'ER = ' + dec_dir(r['er'], True), p + 'SV = ' + dec_dir(r['sv'], True),
             p + 'DEN_LO = ' + dec_dir(r['den'], False),
             p + 'G_LO = ' + (dec_dir(r['g'], False) if r['g'] is not None else 'none (A3 failed)'),
             p + 'ASSERT = A2 %s ; A3 %s ; A4 %s' % tuple('PASS' if x else 'FAIL' for x in (r['a2'], r['a3'], r['a4'])),
             p + 'A5 = INFO er %s beside the record\'s %sEPS_R_300 %s; sv %s beside %sS_300 %s (their agreement is C-LAW300\'s gate in A0)'
             % (dec_dir(r['er'], True), p, rec_kv.get(p + 'EPS_R_300'), dec_dir(r['sv'], True), p, rec_kv.get(p + 'S_300'))]
    why += ['N=%d %s' % (N, a) for a, ok in (('A2', r['a2']), ('A3', r['a3']), ('A4', r['a4'])) if not ok]
    f = (2 - r['er'] * dec_iv('2.2')) / KS[N]['RTR']
    try:
        q = check(KS[N], {'Rtr': f})
        fired = q['a2'] and q['a3'] and not q['a4']
        detail = 'planted den lower end %s, sv upper end %s, g upper end %s' % (
            dec_dir(q['den'], False), dec_dir(q['sv'], True), dec_dir(q['g'], True) if q['g'] is not None else 'none')
    except ArithmeticError as e:
        fired, detail = False, 'vac_law_v1 raised %r' % (e,)
    body.append(p + 'PLANT_CPLUS_G = %s (Rtr scaled by f = (2 - 2.2 er)/RTR; %s)' % ('FIRES' if fired else 'DOES NOT FIRE', detail))
    if not fired:
        why.append('N=%d PLANT-CPLUS-G does not fire' % N)
mod.FH.close()
log_path = mod.OUT_PATH
with open(log_path, 'rb') as fh:
    log_sha = sha_bytes(fh.read())
head.append('MODULE_RUN = kt_s9h_v1_2 loaded from the checked bytes, argv %s; its own log %s:%s' % (
    ' '.join(MODULE_ARGV), os.path.relpath(log_path, CODEDIR), log_sha))
write_record(head + body + ['CLAIM = ' + CLAIM, 'VERDICT = VALID' if not why else 'VERDICT = INVALID (%s)' % '; '.join(why)])
print('VERDICT %s' % ('VALID' if not why else 'INVALID (%s)' % '; '.join(why)))
sys.exit(0 if not why else 1)
