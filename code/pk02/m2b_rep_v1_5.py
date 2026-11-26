#!/usr/bin/env python3
"""m2b_rep_v1_5.py -- pk02 (code/pk02/). REVISION of m2b_rep_v1_4.py (8e6f18c9, never run): the five F-2-fixed pieces come from
m2b_cert_v1_4 (m2b_cert_v1_3 plus majfix_v1_1, C-RADV and C-TMONO) in place of m2b_cert_v1_3; the header line and usage name this file.
Nothing else changes (DIFF_m2b_rep_v1_4_to_v1_5.txt). The FLOAT twin stays m2b_floatref_v2 (majfix_v1: the same polynomials on these paths).
m2b_rep_v1_4 was: pk02 (code/pk02/). REVISION of m2b_rep_v1_3.py (87139b73) for the two trade fixes: C-REP of m2b_cert_v1_3's
re-run pieces. Changes, and nothing else (DIFF_m2b_rep_v1_3_to_v1_4.txt):
  - PRODUCER: d5, dwt, dwl, r0, tA from m2b_cert_v1_3 (majfix_v1's majorants); x, tX0, tX1, tX2, tB from m2b_cert_v1_1 (their paths use no
    trade). C-REP-BOUND covers the ten hand-off HEADs (five of each producer).
  - The FLOAT twin is m2b_floatref_v2 (the same majorants in binary64), its outputs out_m2b_floatref_v2_n<N>.out.
  - C-ANCHOR keeps NP, min TX_lam and the kbar check; D5, D5W_*, R0, R0W_* and ann are no longer anchored (the originals vacrig11f and
    vacrig11w use the radius trade), printed as INFO with that reason.
  - The header line and usage name this file. Run as v1_3 below with this file's name and NEW output paths.
m2b_rep_v1_3 was: pk02 (code/pk02/). REVISION of m2b_rep_v1_2.py (3a9a2953, never run) after dw.n4's CAP-STOP (the
rule, 2026-11-07): the weighted D5 comes from m2b_cert_v1_2's pieces dwt and dwl (one weight each) instead of m2b_cert_v1_1's dw, and
every other piece from m2b_cert_v1_1. PRODUCER names each piece's script and full sha256; the record name, the header line, the hand-off
name and the HEAD are checked against that producer. C-REP-BOUND covers the ten hand-off HEADs of each N (eight of v1_1, two of v1_2).
Nothing else changes. C-ANCHOR's resolution depends on the source print: about 5e-5 relative for vacmono, 1e-4
for vacrig11w and 3e-3 for the 3-digit vacrig11f precheck; cite it with C-ANCHOR.
m2b_rep_v1_2 was: REVISION of m2b_rep_v1_1.py (3d73eef6, never run): adds C-ANCHOR (after
accepting m2b_floatref_v1 as the FLOAT twin of vacrig11f, vacmono and vacrig11w): wherever the twin computes a quantity that the original
engines' existing frozen outputs also print (same J, same vacuum, same form), the two must agree to half a unit of the printed value's last
digit plus 1e-9 relative. Everything else is m2b_rep_v1_1's, unchanged.
C-ANCHOR. The originals' frozen outputs (sha256 pinned below) were run on pk10/scratch/vacres_K3_N<N>.json (the precheck names it; the
vacmono and vacrig11w prints carry the same m-hat), the twin on pk11/out/vacres_K3_N<N>_sym_v1.json. C-ANCHOR-VAC checks that the two
files have identical m1, m2, m3 and q1, q2, q3 equal to 1e-10 of max |q|: the sym file averages entries that are equal by symmetry, and
they differ by about 1e-12 of max |q| (3.65e-13 absolute at N = 4), far below the printed digits (half a unit is 2e-5 relative at the
finest), so the vacuum is the same at every printed digit. Anchored, per N:
  vacmono_N<N>.txt (J1 = 150): 'nP ... Minkowski' = the twin's NP; 'tailX ... Minkowski' = min over lambda of the twin's TX_<lam>
    (vacmono takes the same minimum over 0.3, 0.45, 0.6);
  vacrig11w_N<N>_J170.txt (J0 = 170): for w = wt and dl, 'D5w' = D5W_w and 'R0w' = R0W_w (the same (t^5/120) detf (||lin_w ED|| +
    ||B_w ED||) and ||lin_w R0|| + ||B_w R0||), with the printed kbar of wt equal to m2's kbar of this N to its 9 printed decimals;
  vacrig11f_N4_J150_precheck_v1.txt (N = 4 only, J1 = 150): 'D5' = D5, 'R0' = R0, 'ann' = min over lambda of ANN_<lam>.
Not anchored, with the reason printed: R1, R1_wt, R1_dl (rounding-level, printed by no original); NPM_wt, NPM_dl (the originals print the
joint form ||lin_w P|| + ||B_w P|| of P = sum_k t^k r_k, the twin the Minkowski form per order); TB (the originals' tailB is the chi3
product form, the twin's kt_cert's F1 per-bond form); TX and ANN per lambda (the originals print only the minimum); D5, R0 and ANN at
N = 3 (no vacrig11f output at N = 3 exists; vacrig11w's unweighted terms are at J = 170, which the twin computes only weighted).
PLANT-ANCHOR: the twin's NP times 1 + 1e-3 must fail its anchor (vacmono prints 5 digits).
--- m2b_rep_v1_1's description:
REVISION of m2b_rep_v1.py (63fbb44e, never run) for m2b_cert_v1_1 and the review 8c943f19 sect. 4: it reads m2b_cert_v1_1's records
and hand-offs (out_m2b_cert_v1_1_*, hand_m2b_cert_v1_1_*; HEAD with the exact boundaries and rho_pp_hex) and picks the record's one
HANDOFF line that names a sha256 (the PLANT-NOWRITE line says 'not written'); C-REP-BOUND: every hand-off HEAD at this N carries
a_m = Fraction(0.55)^2, a_e = Fraction(0.6)^2 and a_pp = Fraction(rho_pp)^2 with the same rho_pp_hex; the ball reader takes all three
forms of arb's str with radius ('[m +/- r]' with m of either sign, '[+/- r]', and a bare decimal for an exact value), with PLANT-PARSE.
C-REP for M2(b)'s port items (SPEC_M2B_CERT_v1 sect. 5): m2b_cert_v1_1's balls against m2b_floatref_v1's float64 values of the same
quantities in the same forms, at N = argv[1] in {3, 4}: NP, NPM_wt, NPM_dl, D5, D5W_wt, D5W_dl, R0, R0W_wt, R0W_dl, TX_<lam>, TB,
ANN_<lam> (the ball's midpoint against the float value, relative 1e-6); R1, R1_wt, R1_dl as INFO. PLANT-REP: the cert's D5 midpoint
times 1 + 1e-5 must fail its comparison.
Reads only; writes stdout. Run (own folder): D=/mnt/g2/release/root/code/pk02; o=$D/out/out_m2b_rep_v1_3_n<N>.out;
  [ ! -e "$o" ] && OMP_NUM_THREADS=1 timeout 300 nice -n 10 prlimit --as=4294967296 -- python3 -I -B $D/m2b_rep_v1_3.py
  <N> > "$o" 2> "${o%.out}.err"

"""
import sys, os, re, hashlib, json
from fractions import Fraction

OWN = '/mnt/g2/release/root/code/pk02'
SROOT = '/mnt/g2/release/root/code'
CERT_SHA = 'b73bb41b5bdf3eb53d24229bae5a92462ad9cc48e4661f36189b9b0459159181'
CERT2_SHA = '771885066cad263730c912a1215208d8cf5690744dd6e6d3e188ce5a17f35cba'
CERT3_SHA = '6f45086bb85d3beaaf56fc1adc27f9a2492e2d8e4de02788516b592645cbfaae'            # m2b_rep_v1_5: the F-2-fixed pieces (m2b_cert_v1_4)
PRODUCER = {p: ('m2b_cert_v1_1', CERT_SHA) for p in ('x', 'tX0', 'tX1', 'tX2', 'tB')}      # no trade on these paths
PRODUCER.update({p: ('m2b_cert_v1_4', CERT3_SHA) for p in ('d5', 'dwt', 'dwl', 'r0', 'tA')})   # v1_5: the trade fix (v1_4 of the cert)
FREF_SHA = '066da2ec5be42c020057e253d50e5569105732d7e29c49b00bd98bce5dce8b86'             # m2b_rep_v1_4: the twin with majfix_v1's majorants
ANCHOR = {
    'pk10/scratch/vacmono_N3.txt': '4e31722f9420bee1435fddc14f0e08809afada46583c71234dc8522b0b773fea',
    'pk10/scratch/vacmono_N4.txt': 'dba25ee6a444578612a8fa867e2c399730432d9ab817fe792a32bd021bbeea4a',
    'pk10/scratch/vacrig11w_N3_J170.txt': '9baf04a406932cc5930b4f703874eb9c73eb53c7b11733df75f10c6981f00dae',
    'pk10/scratch/vacrig11w_N4_J170.txt': 'd603847511de1018f72c6996a063935022b1b686cdb91214c2afb68121c01bf7',
    'pk02/out/vacrig11f_N4_J150_precheck_v1.txt': '9337e33730be09e0ea2831e7472003b91f0b1ea7890f41119a3790f763bce14a',
    'pk10/scratch/vacres_K3_N3.json': 'ebcbd08ca532642188071c964039808a318038020bb1a788a7fa3a49cb357426',
    'pk10/scratch/vacres_K3_N4.json': '516b2501c37a65b21b617fba3cb1d7b02adf9966f409bc5105418822dfa0e765',
    'pk11/out/vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    'pk11/out/vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    'pk10/scratch/m2_N3_J170.json.b': '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    'pk10/scratch/m2_N4_J170.json.b': '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
}
NN = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] in ('3', '4') else 0
if NN == 0:
    print('usage: m2b_rep_v1_5.py 3|4')
    sys.exit(2)
PIECES = ('x', 'd5', 'dwt', 'dwl', 'r0', 'tX0', 'tX1', 'tX2', 'tB', 'tA')
TOL = 1e-6
FAILS = []
HEADS = {}
NUM = r'[-+]?[0-9]+(?:\.[0-9]+)?(?:e[-+]?[0-9]+)?'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def gate(name, ok, line):
    print('%s: %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def head_ok(head, piece):
    """the HEAD of the piece's producer: HEAD <script> <sha256> piece <p> kind vac N <N> prec <prec> a_m <p/q> a_e <p/q> a_pp <p/q>
    rho_pp_hex <hex>."""
    name, psha = PRODUCER[piece]
    return (len(head) == 19 and head[:2] == ['HEAD', name] and head[2] == psha and head[3:5] == ['piece', piece] and
            head[5:9] == ['kind', 'vac', 'N', str(NN)] and head[9] == 'prec' and
            [head[i] for i in (11, 13, 15, 17)] == ['a_m', 'a_e', 'a_pp', 'rho_pp_hex'])


def piece_rows(piece):
    """the hand-off rows of a piece after the record and hand-off checks against its producer; None if a check fails."""
    item = '%s.n%d' % (piece, NN)
    name, psha = PRODUCER[piece]
    rec = os.path.join(OWN, 'out_%s_%s.out' % (name, item))
    lines = open(rec).read().splitlines()
    hl = [ln for ln in lines if ln.startswith('HANDOFF N=%d vac %s: ' % (NN, piece)) and ' sha256 ' in ln]
    ok = (bool(lines) and lines[0].startswith('%s sha256 %s ITEM=%s ' % (name, psha, item)) and
          [ln for ln in lines if ln.startswith('FORMAT ')] == ['FORMAT M2B_PIECE_v1 CERTIFIED'] and
          [ln for ln in lines if ln.startswith('VERDICT')] == ['VERDICT VALID'] and len(hl) == 1)
    rows = None
    if ok:
        want = hl[0].split(' sha256 ')[1].split()[0]
        path = os.path.join(OWN, 'hand_%s_%s.txt' % (name, item))
        ok = hl[0].split()[4] == os.path.basename(path)
        data = open(path, 'rb').read() if ok else b''
        body, sep, endline = data.decode().rpartition('END ')
        head = body.splitlines()[0].split() if body else []
        ok = (ok and sep == 'END ' and hashlib.sha256(data).hexdigest() == want and
              endline == hashlib.sha256(body.encode()).hexdigest() + '\n' and head_ok(head, piece))
        if ok:
            rows = body.splitlines()[1:]
            HEADS[piece] = head
    gate('C-REP-READ %s' % item, ok, 'record %s (sha256 %s): header, FORMAT, VERDICT, hand-off sha256, checksum and HEAD' % (
        os.path.basename(rec), sha(rec)[:8]))
    return rows


def parts(s):
    """the decimal midpoint and radius strings of arb's str with radius: '[m +/- r]', '[+/- r]' (midpoint 0) or a bare decimal (radius 0)."""
    s = s.strip()
    mt = re.fullmatch(r'\[(%s) \+/- (%s)\]' % (NUM, NUM), s)
    if mt:
        return mt.group(1), mt.group(2)
    mt = re.fullmatch(r'\[\+/- (%s)\]' % NUM, s)
    if mt:
        return '0', mt.group(1)
    mt = re.fullmatch(NUM, s)
    if mt:
        return s, '0'
    raise ValueError('not a ball: %r' % s[:60])


def mid(s):
    """the midpoint of a ball string as a float (C-REP compares midpoints; the balls are the cert's)."""
    return float(parts(s)[0])


def plant_parse():
    """PLANT-PARSE: balls of every form round-trip to containing balls; a sign-dropping reading is caught."""
    from flint import arb, ctx
    ctx.prec = 512
    third = arb(1) / 3
    cases = [('0 +- r', arb(0, arb(2) ** -40)), ('negative', -third), ('negative, wide', arb(-third.mid(), arb(2) ** -20)),
             ('exact negative', arb(-5) / 4), ('exact zero', arb(0)), ('tiny', third * arb(10) ** -300),
             ('large negative', -third * arb(10) ** 300), ('positive', third * 7)]
    bad = []
    for name, x in cases:
        s = x.str(80, radius=True)
        m, r = parts(s)
        y = arb(s)
        okm = abs(float(m) - float(x.mid())) <= float(r) + 1e-15 * abs(float(x.mid()))
        if not (y.contains(x) and okm and (r == '0') == (x.rad() == 0 and s == m)):
            bad.append(name)
        print('PLANT-PARSE %s: %s -> mid %s, rad %s, parsed ball contains the original: %s' % (name, s[:48], m[:24], r[:12], y.contains(x)))
    x = -third
    s = x.str(80, radius=True)
    caught = not arb(s.replace('-', '', 1)).contains(x)
    print('PLANT-PARSE sign drop: the negative ball read without its sign contains the original: %s -> %s' % (
        not caught, 'FIRES' if caught else 'DOES NOT FIRE'))
    if bad or not caught:
        FAILS.append('PLANT-PARSE (%s)' % ', '.join(bad + ([] if caught else ['sign drop not caught'])))


def anchor_text(rel):
    """an original engine's frozen output (or input), checked against its pin."""
    data = open(os.path.join(SROOT, rel), 'rb').read()
    if hashlib.sha256(data).hexdigest() != ANCHOR[rel]:
        raise ValueError('anchor file %s differs from its pin' % rel)
    return data


def half_unit(s):
    """half a unit of the last printed digit of a printed float ('2.6744e-06' -> 5e-11; '0.827139427' -> 5e-10)."""
    mt = re.fullmatch(r'[-+]?[0-9]+(?:\.([0-9]+))?(?:e([-+]?[0-9]+))?', s)
    if mt is None:
        raise ValueError('not a printed float: %r' % s)
    return 0.5 * 10.0 ** (int(mt.group(2) or 0) - len(mt.group(1) or ''))


def anchored(twin, printed):
    return twin is not None and abs(twin - float(printed)) <= half_unit(printed) + 1e-9 * abs(twin)


def find(text, pat, what):
    mt = re.search(pat, text, re.M)
    if mt is None:
        raise ValueError('C-ANCHOR: %s not found' % what)
    return mt


def c_anchor(fref):
    """C-ANCHOR: the twin's values against the originals' frozen prints (see the docstring); returns the (name, twin, printed, source) rows."""
    old = json.loads(anchor_text('pk10/scratch/vacres_K3_N%d.json' % NN))
    new = json.loads(anchor_text('pk11/out/vacres_K3_N%d_sym_v1.json' % NN))
    okm = all(old[k] == new[k] for k in ('m1', 'm2', 'm3'))
    qs = [(a, b) for k in ('q1', 'q2', 'q3') for a, b in zip(old[k], new[k])]
    okl = all(len(old[k]) == len(new[k]) for k in ('q1', 'q2', 'q3'))
    qmax = max(abs(b) for _, b in qs)
    dq = max(abs(a - b) for a, b in qs)
    gate('C-ANCHOR-VAC n%d' % NN, okm and okl and dq <= 1e-10 * qmax, 'old vacres_K3_N%d.json vs sym: m1..m3 identical %s; q1..q3 '
         'max |difference| %.2e (max |q| %.3e, bound 1e-10 of it)' % (NN, okm, dq, qmax))
    vm = anchor_text('pk10/scratch/vacmono_N%d.txt' % NN).decode()
    if not vm.startswith('# vacmono: N = %d, J1 = 150 (rho_m 0.55, rho_e 0.6, delta 40 deg)\n' % NN):
        raise ValueError('C-ANCHOR: vacmono header')
    tx = [fref.get('TX_%s' % lam) for lam in ('0.3', '0.45', '0.6')]
    an = [fref.get('ANN_%s' % lam) for lam in ('0.3', '0.45', '0.6')]
    rows = [('NP', fref.get('NP'), find(vm, r'^nP: joint \S+, Minkowski (\S+)$', 'vacmono nP').group(1), 'vacmono nP Minkowski, J1 150'),
            ('min TX_lam', min(tx) if None not in tx else None, find(vm, r'^tailX: joint \S+, Minkowski (\S+)$', 'vacmono tailX').group(1),
             'vacmono tailX Minkowski (minimum over 0.3, 0.45, 0.6), J1 150')]
    vw = anchor_text('pk10/scratch/vacrig11w_N%d_J170.txt' % NN).decode()
    kb = find(vw, r'^# vacrig11w: N = %d; rho_m 0.55 rho_e 0.6 delta 40.0 deg; weighted residuals for wt:([0-9.]+),dl ' % NN,
              'vacrig11w header').group(1)
    find(vw, r'^J =  170\.0: ', 'vacrig11w J = 170 line')
    kbar = json.loads(anchor_text('pk10/scratch/m2_N%d_J170.json.b' % NN))['kbar']
    gate('C-ANCHOR-KBAR n%d' % NN, abs(kbar - float(kb)) <= half_unit(kb), "vacrig11w's printed wt kbar %s vs m2's kbar %r" % (kb, kbar))
    # m2b_rep_v1_4: D5W_w, R0W_w (vacrig11w) and D5, R0, ann (the vacrig11f precheck) are no longer anchored: the originals run the trade
    # of the trade fix, the twin runs majfix_v1's majorants (C-REP compares the twin with m2b_cert_v1_3, the same majorants in balls).
    for name, twin, printed, src in rows:
        gate('C-ANCHOR %s n%d' % (name, NN), anchored(twin, printed), 'twin %s vs %s %s (tolerance %.1e + 1e-9 rel)' % (
            'missing' if twin is None else '%.12e' % twin, src, printed, half_unit(printed)))
    for name, why in (('R1, R1_wt, R1_dl', 'rounding-level; printed by no original'),
                      ('NPM_wt, NPM_dl', 'the originals print the joint form of P = sum_k t^k r_k; the twin is Minkowski per order'),
                      ('TB', "the originals' tailB is the chi3 product form; the twin's is kt_cert's F1 per-bond form"),
                      ('D5, D5W_wt, D5W_dl, R0, R0W_wt, R0W_dl, ann', 'the originals (vacrig11f, vacrig11w) use the trade; the twin uses '
                       'majfix_v1'),
                      ('TX_<lam> per lambda', 'the originals print only the minimum over lambda')):
        print('INFO C-ANCHOR n%d not anchored: %s (%s)' % (NN, name, why))
    return rows


print('m2b_rep_v1_5 sha256 %s N=%d; m2b_cert_v1_1 %s (x, tX0-2, tB); m2b_cert_v1_4 %s (d5, dwt, dwl, r0, tA); m2b_floatref_v2 %s' % (
    sha(os.path.abspath(__file__)), NN, CERT_SHA[:8], CERT3_SHA[:8], FREF_SHA[:8]))
if sha(os.path.join(OWN, 'm2b_cert_v1_1.py')) != CERT_SHA or sha(os.path.join(OWN, 'm2b_cert_v1_4.py')) != CERT3_SHA or \
        sha(os.path.join(OWN, 'm2b_floatref_v2.py')) != FREF_SHA:
    print('SHA MISMATCH (engines)')
    print('VERDICT INVALID (C-HASH)')
    sys.exit(2)
plant_parse()
fpath = os.path.join(OWN, 'out', 'out_m2b_floatref_v2_n%d.out' % NN)
flines = open(fpath).read().splitlines()
okf = bool(flines) and flines[0].startswith('m2b_floatref_v2 sha256 %s N=%d' % (FREF_SHA, NN)) and \
    [ln for ln in flines if ln.startswith('VERDICT')] == ['VERDICT VALID']
gate('C-REP-READ floatref n%d' % NN, okf, '%s (sha256 %s): header and VERDICT' % (os.path.basename(fpath), sha(fpath)[:8]))
fref = {}
for ln in flines:
    mt = re.match(r'FREF N=%d (\S+) ([-+0-9.e]+)$' % NN, ln)
    if mt:
        fref[mt.group(1)] = float(mt.group(2))
try:
    arows = c_anchor(fref)
except (ValueError, OSError, KeyError) as e:
    gate('C-ANCHOR n%d' % NN, False, 'refused: %s' % e)
    arows = []
pl = [r for r in arows if r[0] == 'NP' and r[1] is not None]
fired = bool(pl) and not anchored(pl[0][1] * (1 + 1e-3), pl[0][2])
print('PLANT-ANCHOR n%d: the twin NP x (1 + 1e-3) against vacmono %s -> %s' % (NN, pl[0][2] if pl else 'missing',
                                                                             'FIRES' if fired else 'DOES NOT FIRE'))
if not fired:
    FAILS.append('PLANT-ANCHOR did not fire')
cert = {}
for piece in PIECES:
    rows = piece_rows(piece)
    if rows is None:
        continue
    for ln in rows:
        f = ln.split(' ', 2)
        if f[0] == 'V':
            cert[f[1]] = mid(f[2])
        elif f[0] == 'A':
            g = ln.split(' ', 3)
            fam, lam, acc = g[1], g[2], mid(g[3])
            key = {'X': 'TX_%g' % float(lam), 'B': 'TB', 'A': 'ANN_%g' % float(lam)}[fam]
            cert[key] = acc ** 0.5
hx = sorted(set(h[18] for h in HEADS.values()))
okb = len(HEADS) == len(PIECES) and len(hx) == 1
if okb:
    rho = float.fromhex(hx[0])
    okb = all(Fraction(h[12]) == Fraction(0.55) ** 2 and Fraction(h[14]) == Fraction(0.6) ** 2 and Fraction(h[16]) == Fraction(rho) ** 2
              for h in HEADS.values())
gate('C-REP-BOUND n%d' % NN, okb, '%d hand-off HEADs: rho_pp_hex %s, a_m, a_e, a_pp exact' % (len(HEADS), ' '.join(hx)))
KEYS = ['NP', 'NPM_wt', 'NPM_dl', 'D5', 'D5W_wt', 'D5W_dl', 'R0', 'R0W_wt', 'R0W_dl', 'TX_0.3', 'TX_0.45', 'TX_0.6', 'TB', 'ANN_0.3',
        'ANN_0.45', 'ANN_0.6']
for k in KEYS:
    if k not in cert or k not in fref:
        gate('C-REP %s' % k, False, 'missing (cert %s, float %s)' % (k in cert, k in fref))
        continue
    rel = abs(cert[k] / fref[k] - 1)
    gate('C-REP %s' % k, rel <= TOL, 'cert midpoint %.12e vs float %.12e: rel %.1e (tolerance %.0e)' % (cert[k], fref[k], rel, TOL))
for k in ('R1', 'R1_wt', 'R1_dl'):
    print('INFO C-REP %s: cert midpoint %s vs float %s (rounding-level on both sides; not compared)' % (
        k, '%.6e' % cert[k] if k in cert else 'missing', '%.6e' % fref[k] if k in fref else 'missing'))
if 'D5' in cert and 'D5' in fref:
    fired = abs(cert['D5'] * (1 + 1e-5) / fref['D5'] - 1) > TOL
    print('PLANT-REP: the cert D5 midpoint x (1 + 1e-5) against the float -> %s' % ('FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        FAILS.append('PLANT-REP did not fire')
print('VERDICT %s' % ('VALID' if not FAILS else 'INVALID (%s)' % ', '.join(FAILS)))
