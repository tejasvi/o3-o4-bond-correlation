#!/usr/bin/env python3
"""m2b_asm_v1.py -- pk02 (code/pk02/). The assembly of the certified vacuum record M2B_KV_v1 (SPEC_M2B_CERT_v1 ffd842a2 with ADD1
2c97391f and ADD2 48d5fa54), for N = 3 and 4 in one run; it writes the record only if every check passes.
After the two trade fixes, the pieces whose paths call xibar or pi_vac come from
m2b_cert_v1_4 (the shared fix majfix_v1_1): d5, dwt, dwl, r0, tA; the others,
whose paths use no trade, from m2b_cert_v1_1: x, tX0, tX1, tX2, tB (PRODUCER, the review 849eeb24 point (1)). C-REP is m2b_rep_v1_5's against
m2b_floatref_v2; D5, R0 and ann have no independent anchor, their evidence being the derivations, C-MAJ-SAMPLE and C-P0SUB.
The M3 calls are m3_reader_v5's (load bound to the asm output; entry_ball; outer_far with value, chart, far, lam_star, r, a_m).
Inputs, every one pinned by full sha256 (filled at freeze from sha256sum, never typed):
  - the piece records and hand-offs of m2b_cert_v1_1 (x, tX0, tX1, tX2, tB) and m2b_cert_v1_4 (d5, dwt, dwl, r0, tA), at n4 and n3, read with
    (header, FORMAT, VERDICT exactly ['VERDICT VALID'], the one HANDOFF line with a sha256, the hand-off's sha256, END and 19-field HEAD);
  - C-REP: m2b_rep_v1_5's outputs at n4 and n3 (C-REP, C-REP-BOUND, C-ANCHOR, plants), VERDICT exactly ['VERDICT VALID'];
  - pk03's vacuum records, only through m3_reader_v5's certified load bound to their asm outputs, with pk03's asm manifest; the
    builder re-checks chart >= 0, far >= 0, value >= chart + far and law.a_m == Fraction(0.55)^2 exactly;
  - pk08's S4_RTR_CERTIFIED_v1.md (N*_RTR) with the CLOSE_S4_RTR_CERTIFIED_v1_rv01.md;
  - the trial vacuum (the m_j for MHAT_UP, the q_j for supp).
Assembly (arb at 512 bits; each key at its safe end, SPEC sect. 3a; decimals rounded up or down exactly by m2b_reader_v1's dec_up and
dec_down):
  NP, R1, D5, R0 (x, d5, r0); TX = min over lambda of tX's roots, TX_LAMSTAR; TB; ANN = min over lambda, ANN_LAMSTAR;
  WT = nPM_wt ; D5W_wt ; R0W_wt and WT_R1 = R1_wt, DL likewise (SPEC row 13);
  FAR = o4 + 2 MHAT_UP o3 + MHAT_UP^2 oD with o_X = VAC_OF_X.value and MHAT_UP the upper end of mhat(1/300) (C-MHAT);
  GB = supp(150) (sum_r e^{-0.95 150 (1 - cos 40 deg)} ratio_main_r zR_r)^{1/2}, zR_r = 1 + sum_{k=1..3} max(HI_k, 0) 150^-k + err_b of
  G4R_r, ratio_main_r = (det L_E4 / det L_{E4 - (r, 3 + r)})^{nn/2} on the sum-zero subspace, in arb;
  Z2 = 1 + sum_{k=1..3} min(LO_k, 0) 150^-k - err_b of D_Z2 (lower); RTR from pk08; AE = a_e rounded down; KAPPA_B (global) rounded
  down; the C-FMT values N*_EPS_*_300 = LAW v1 at J = 300 by m2b_reader_v1.law_balls on the keys as written, rounded up.
Checks: C-BOUND (the ten hand-off HEADs of each N carry one rho_pp_hex; a_m = every VAC_OF law.a_m = Fraction(0.55)^2; a_e, a_pp as
the record states; a_pp >= sin^2(asin rho_m + delta) in arb), C-MHAT, C-LAW (LAW v1 at J = 300, 600, 1200 nonincreasing), and the
read-back through m2b_reader_v1.check (every record check, C-MONO, C-FMT). Plants: PLANT-PRECERT, PLANT-VERDICT, PLANT-KIND, PLANT-MF,
PLANT-JREF, PLANT-LAYER (modified M3 copies through m3_reader_v5.loads), PLANT-BOUND, PLANT-MHAT.
Writes M2B_KV_v1.txt (exclusive create, then 444) and stdout, whose first line names this file's sha256 and whose 'RECORD <name>
<sha256>' line and VERDICT line bind the record (m2b_reader_v1.load).
The headroom quotes of SPEC sect. 4 (agreed with pk07): N*_Z2_FLOAT (vacmono's Z2low(J1)) and N*_RTR_FLOAT (S4's TARGET_FLOAT) exact,
N*_Z2_FACTOR and N*_RTR_FACTOR rounded up; m2b_reader_v1 allows these keys and checks the quotients.
"""
import sys, os, re, hashlib, json, time, importlib.util
from fractions import Fraction

OWN = '/mnt/g2/release/root/code/pk02'
CODEDIR = '/mnt/g2/release/root/code'
CODE = {'pk02/m2b_cert_v1_1.py': '@@SHA:m2b_cert_v1_1.py@@', 'pk02/m2b_cert_v1_4.py': '@@SHA:m2b_cert_v1_4.py@@',
        'pk02/majfix_v1_1.py': '@@SHA:majfix_v1_1.py@@', 'pk02/majfix_v1.py': '@@SHA:majfix_v1.py@@',
        'pk02/m2b_rep_v1_5.py': '@@SHA:m2b_rep_v1_5.py@@', 'pk02/run_m2b_f2_v1.sh': '@@SHA:run_m2b_f2_v1.sh@@',
        'pk02/m2b_reader_v1.py': '@@SHA:m2b_reader_v1.py@@', 'pk02/arbeng_c2b_v2.py': '@@SHA:arbeng_c2b_v2.py@@',
        'pk02/arbeng_ma_v1_3.py': '@@SHA:arbeng_ma_v1_3.py@@', 'pk02/m2b_floatref_v2.py': '@@SHA:m2b_floatref_v2.py@@'}
LAYER = {'pk02/out/out_kt_ma_val_v1_5_v1.out': '@@SHA:out/out_kt_ma_val_v1_5_v1.out@@',
         'pk02/out/out_kt_ma_val_v1_5_v2.out': '@@SHA:out/out_kt_ma_val_v1_5_v2.out@@',
         'pk02/out/out_kt_ma_val_v1_5_v3.out': '@@SHA:out/out_kt_ma_val_v1_5_v3.out@@',
         'pk02/out/out_kt_ma_val_v1_5_v4.out': '@@SHA:out/out_kt_ma_val_v1_5_v4.out@@',
         'rv01/CLOSE_ARBENG_MA_V1_3_rv01.md': '@@SHA:../rv01/CLOSE_ARBENG_MA_V1_3_rv01.md@@'}
TRIAL = {'pk11/out/vacres_K3_N3_sym_v1.json': '@@SHA:../pk11/out/vacres_K3_N3_sym_v1.json@@',
         'pk11/out/vacres_K3_N4_sym_v1.json': '@@SHA:../pk11/out/vacres_K3_N4_sym_v1.json@@',
         'pk10/scratch/m2_N3_J170.json.b': '@@SHA:../pk10/scratch/m2_N3_J170.json.b@@',
         'pk10/scratch/m2_N4_J170.json.b': '@@SHA:../pk10/scratch/m2_N4_J170.json.b@@'}
FLOATREC = {'pk02/out/out_m2b_floatref_v2_n4.out': '@@SHA:out/out_m2b_floatref_v2_n4.out@@',
            'pk02/out/out_m2b_floatref_v2_n3.out': '@@SHA:out/out_m2b_floatref_v2_n3.out@@'}
FLOATQ = {'pk10/scratch/vacmono_N3.txt': '@@SHA:../pk10/scratch/vacmono_N3.txt@@',
          'pk10/scratch/vacmono_N4.txt': '@@SHA:../pk10/scratch/vacmono_N4.txt@@'}   # vac_float's Z2 (Z2_FLOAT)
M3CODE = {'pk03/m3_reader_v5.py': '@@SHA:../pk03/m3_reader_v5.py@@'}
M3FILES = {                                  # N -> [(record json, sha256), (asm output, sha256), (asm manifest, sha256)], paths under CODEDIR
    4: [('pk03/out/m3_vac_N4_J150_v2_1.json', '@@SHA:../pk03/out/m3_vac_N4_J150_v2_1.json@@'),
        ('pk03/out/m3_vac_v2_1_asm.4.out', '@@SHA:../pk03/out/m3_vac_v2_1_asm.4.out@@'),
        ('pk03/MANIFEST_m3_vac_v2_1_asm.4.sha256', '@@SHA:../pk03/MANIFEST_m3_vac_v2_1_asm.4.sha256@@')],
    3: [('pk03/out/m3_vac_N3_J150_v2_1.json', '@@SHA:../pk03/out/m3_vac_N3_J150_v2_1.json@@'),
        ('pk03/out/m3_vac_v2_1_asm.3.out', '@@SHA:../pk03/out/m3_vac_v2_1_asm.3.out@@'),
        ('pk03/MANIFEST_m3_vac_v2_1_asm.3.sha256', '@@SHA:../pk03/MANIFEST_m3_vac_v2_1_asm.3.sha256@@')]}
S4 = {'pk08/S4_RTR_CERTIFIED_v1.md': '@@SHA:../pk08/S4_RTR_CERTIFIED_v1.md@@',
      'rv01/CLOSE_S4_RTR_CERTIFIED_v1_rv01.md': '@@SHA:../rv01/CLOSE_S4_RTR_CERTIFIED_v1_rv01.md@@'}
MA_DENY = ('@@SHA:arbeng_ma_v1_1.py@@', '@@SHA:arbeng_ma_v1_2.py@@')      # arbeng_ma_v1_1 (D-1) and arbeng_ma_v1_2, for PLANT-LAYER
PIECES = ('x', 'd5', 'dwt', 'dwl', 'r0', 'tX0', 'tX1', 'tX2', 'tB', 'tA')
PRODUCER = {p: 'm2b_cert_v1_4' if p in ('d5', 'dwt', 'dwl', 'r0', 'tA') else 'm2b_cert_v1_1' for p in PIECES}   # The review 849eeb24 (1)
PIECEPINS = {                                # the 20 VALID piece records and their hand-offs, full sha256 (filled at freeze, never typed)
#@PIECEPINS@
}
REPOUT = {'pk02/out/out_m2b_rep_v1_5_n4.out': '@@SHA:out/out_m2b_rep_v1_5_n4.out@@',
          'pk02/out/out_m2b_rep_v1_5_n3.out': '@@SHA:out/out_m2b_rep_v1_5_n3.out@@'}   # C-REP's VALID outputs (m2b_rep_v1_5)
RHO_PP_HEX_PIN = '@@RHOPPHEX@@'              # every hand-off HEAD's rho_pp_hex must equal it (the review T69 N3)
OUTREC = os.path.join(OWN, 'M2B_KV_v1.txt')
FAILS = []


def sha_file(p):
    try:
        with open(p, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


def gate(name, ok, line):
    print('%s: %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'), flush=True)
    if not ok:
        FAILS.append(name)


SELF_SHA = sha_file(os.path.abspath(__file__))
print('m2b_asm_v1 sha256 %s (cert v1_1 %s, cert v1_4 %s, rep v1_5 %s, reader %s)' % (
    SELF_SHA, CODE['pk02/m2b_cert_v1_1.py'][:8], CODE['pk02/m2b_cert_v1_4.py'][:8], CODE['pk02/m2b_rep_v1_5.py'][:8],
    CODE['pk02/m2b_reader_v1.py'][:8]), flush=True)
_tabs = [CODE, LAYER, TRIAL, FLOATREC, FLOATQ, M3CODE, S4, PIECEPINS, REPOUT] + [dict(M3FILES[n]) for n in sorted(M3FILES)]
_bad = [p for tab in _tabs for p, h in sorted(tab.items()) if sha_file(os.path.join(CODEDIR, p)) != h]
gate('C-HASH', not _bad and sorted(M3FILES) == [3, 4], '%d pinned files%s' % (sum(len(t) for t in _tabs),
                                                                              (': ' + ', '.join(_bad)) if _bad else ''))
if _bad or sorted(M3FILES) != [3, 4]:
    print('VERDICT INVALID (C-HASH)')
    sys.exit(2)
from flint import arb, arb_mat, ctx
ctx.prec = 512
_sp = importlib.util.spec_from_file_location('m3r_v5', os.path.join(CODEDIR, next(iter(M3CODE))))
m3r = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(m3r)
_sp2 = importlib.util.spec_from_file_location('m2b_reader_v1', os.path.join(OWN, 'm2b_reader_v1.py'))
rdr = importlib.util.module_from_spec(_sp2)
_sp2.loader.exec_module(rdr)
ctx.prec = 512
A_M, A_E = Fraction(0.55) ** 2, Fraction(0.6) ** 2
DELTA = arb.pi() * 40 / 180
farb, frac_upper, dec_up = rdr.farb, rdr.frac_upper, rdr.dec_up


def frac_lower(x):
    m, e = x.lower().man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def dec_down(f, digits=12):
    """a decimal string at or below the Fraction f > 0 (rounded down exactly to the given significant digits)."""
    if not f > 0:
        raise ValueError('dec_down: %r is not positive' % f)
    e = len(str(f.numerator)) - len(str(f.denominator))
    while Fraction(10) ** e > f:
        e -= 1
    while Fraction(10) ** (e + 1) <= f:
        e += 1
    k = digits - 1 - e
    sc = f * Fraction(10) ** k
    s = str(sc.numerator // sc.denominator)
    return '%s.%se%+03d' % (s[0], s[1:], e)


def piece_rows(piece, n):
    """m2b_rep_v1_5's record and hand-off checks (the producer's sha256 from CODE); returns (HEAD fields, hand-off rows)."""
    item = '%s.n%d' % (piece, n)
    pname = PRODUCER[piece]
    rec = os.path.join(OWN, 'out_%s_%s.out' % (pname, item))
    lines = open(rec).read().splitlines()
    hl = [ln for ln in lines if ln.startswith('HANDOFF N=%d vac %s: ' % (n, piece)) and ' sha256 ' in ln]
    cert = CODE['pk02/%s.py' % pname]
    if not (lines and lines[0].startswith('%s sha256 %s ITEM=%s ' % (pname, cert, item)) and
            [ln for ln in lines if ln.startswith('FORMAT ')] == ['FORMAT M2B_PIECE_v1 CERTIFIED'] and
            [ln for ln in lines if ln.startswith('VERDICT')] == ['VERDICT VALID'] and len(hl) == 1):
        raise ValueError('record %s: header, FORMAT, VERDICT or HANDOFF line' % os.path.basename(rec))
    want = hl[0].split(' sha256 ')[1].split()[0]
    path = os.path.join(OWN, 'hand_%s_%s.txt' % (pname, item))
    if hl[0].split()[4] != os.path.basename(path):
        raise ValueError('record %s names another hand-off' % os.path.basename(rec))
    data = open(path, 'rb').read()
    body, sep, endline = data.decode().rpartition('END ')
    head = body.splitlines()[0].split() if body else []
    if not (sep == 'END ' and hashlib.sha256(data).hexdigest() == want and endline == hashlib.sha256(body.encode()).hexdigest() + '\n' and
            len(head) == 19 and head[:3] == ['HEAD', pname, cert] and head[3:9] == ['piece', piece, 'kind', 'vac', 'N', str(n)] and
            [head[i] for i in (9, 11, 13, 15, 17)] == ['prec', 'a_m', 'a_e', 'a_pp', 'rho_pp_hex']):
        raise ValueError('hand-off of %s: sha256, END or HEAD' % item)
    return head, body.splitlines()[1:]


EXPECTED_V = {'x': {'NP', 'R1', 'NPM_wt', 'R1_wt', 'NPM_dl', 'R1_dl'}, 'd5': {'D5'}, 'dwt': {'D5W_wt'}, 'dwl': {'D5W_dl'},
              'r0': {'R0', 'R0W_wt', 'R0W_dl'}, 'tX0': set(), 'tX1': set(), 'tX2': set(), 'tB': set(), 'tA': set()}
EXPECTED_A = {'tX0': {('X', '0.3')}, 'tX1': {('X', '0.45')}, 'tX2': {('X', '0.6')}, 'tB': {('B', '0.45')},
              'tA': {('A', '0.3'), ('A', '0.45'), ('A', '0.6')}}


def pieces_of(n):
    """the port items of N n as balls, the lambda*s, and the ten HEADs. Each piece's V keys and A rows must be exactly its own set
    (the review T69 N3: D5W_wt only from dwt, D5W_dl only from dwl, no key from two pieces)."""
    vals, heads, acc = {}, {}, {'X': {}, 'A': {}, 'B': {}}
    for piece in PIECES:
        head, rows = piece_rows(piece, n)
        heads[piece] = head
        vk, ak = set(), set()
        for ln in rows:
            f = ln.split(' ', 3)
            if f[0] == 'V':
                if f[1] in vals or f[1] in vk:
                    raise ValueError('%s.n%d: key %s twice' % (piece, n, f[1]))
                vk.add(f[1])
                vals[f[1]] = arb(ln.split(' ', 2)[2])
            elif f[0] == 'A':
                if (f[1], f[2]) in ak:
                    raise ValueError('%s.n%d: A row %s %s twice' % (piece, n, f[1], f[2]))
                ak.add((f[1], f[2]))
                acc[f[1]][f[2]] = arb(f[3])
        if vk != EXPECTED_V[piece] or ak != EXPECTED_A.get(piece, set()):
            raise ValueError('%s.n%d: value keys %s / A rows %s, expected %s / %s' % (piece, n, sorted(vk), sorted(ak), sorted(EXPECTED_V[piece]),
                                                                                  sorted(EXPECTED_A.get(piece, set()))))
    roots = {fam: {lam: a.sqrt() for lam, a in d.items()} for fam, d in acc.items()}
    if sorted(roots['X']) != ['0.3', '0.45', '0.6'] or sorted(roots['A']) != ['0.3', '0.45', '0.6'] or list(roots['B']) != ['0.45']:
        raise ValueError('N%d: the tail pieces\' lambdas' % n)
    lx = min(roots['X'], key=lambda l: frac_upper(roots['X'][l]))
    la = min(roots['A'], key=lambda l: frac_upper(roots['A'][l]))
    vals.update(TX=roots['X'][lx], ANN=roots['A'][la], TB=roots['B']['0.45'])
    return vals, dict(TX=lx, ANN=la), heads


def mhat_up(n):
    """MHAT_UP = mhat(1/300) = 1 + m1/300 + m2/300^2 + m3/300^3 rounded up; C-MHAT: m1, m2, m3 >= 0 exactly, and MHAT_UP >= mhat(t) at
    t = 1/600, 1/1200 and 0."""
    with open(os.path.join(CODEDIR, 'pk11/out/vacres_K3_N%d_sym_v1.json' % n)) as fh:
        R = json.load(fh)
    m = [R['m1'], R['m2'], R['m3']]

    def mh(t):
        return 1 + sum((arb(m[k]) * t ** (k + 1) for k in range(3)), arb(0))
    s = dec_up(frac_upper(mh(arb(1) / 300)), 15)
    ok = all(x >= 0 for x in m) and all(bool(arb(s) >= mh(t)) for t in (arb(1) / 600, arb(1) / 1200, arb(0)))
    return s, ok, m


SQ5, SQ21 = arb(5).sqrt(), arb(21).sqrt()
TRI = [(3 + SQ21) / 6, (3 + SQ21) / 6, (3 * SQ5 - SQ21) / 12]
PAIRS = [(0, 1), (1, 2), (0, 2)]
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]
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


def supp(q, J):
    """vacrig11f l.358-359 in arb: 1 + sum_i t^i |q_i(b)| (2J)^len(mono) at J."""
    t = arb(1) / J
    return 1 + sum((t ** i * abs(arb(cb)) * arb(2 * J) ** len(mono_) for i, coef in ((1, q[1]), (2, q[2]), (3, q[3]))
                    for cb, mono_ in zip(coef, BASIS)), arb(0))


def j_uniform(ball, upper):
    """ADD4's J-uniform forms on m3_reader's exact entry ball (LO, HI, err_b): 1 + sum_{k=1..3} max(HI_k, 0) 150^-k + err_b (upper) or
    1 + sum_{k=1..3} min(LO_k, 0) 150^-k - err_b (lower); a_0 = 1 exactly is checked."""
    LO, HI, eb = ball
    if not (Fraction(LO[0]) == 1 and Fraction(HI[0]) == 1):
        raise ValueError('a_0 is not exactly 1')
    t = Fraction(1, 150)
    if upper:
        return 1 + sum(max(Fraction(HI[k]), 0) * t ** k for k in (1, 2, 3)) + Fraction(eb)
    return 1 + sum(min(Fraction(LO[k]), 0) * t ** k for k in (1, 2, 3)) - Fraction(eb)


def m3_items(n):
    """pk03's vacuum record of N n through m3_reader_v5 (bound to its asm output), the manifest check, and the builder's re-checks."""
    (pj, hj), (po, ho), (pm, _) = M3FILES[n]
    rec = m3r.load(os.path.join(CODEDIR, pj), os.path.join(CODEDIR, po), 150, n)
    man = open(os.path.join(CODEDIR, pm)).read().splitlines()
    names = {os.path.basename(ln.split()[1]): ln.split()[0] for ln in man if len(ln.split()) == 2}
    okm = names.get(os.path.basename(pj)) == hj and names.get(os.path.basename(po)) == ho
    of = {}
    for g in ('E4', 'E3', 'ED'):
        it = m3r.outer_far(rec, 'VAC_OF_' + g)
        v, c, f = Fraction(it['value']), Fraction(it['chart']), Fraction(it['far'])
        if not (c >= 0 and f >= 0 and v >= c + f and Fraction(it['a_m']) == A_M):
            raise ValueError('VAC_OF_%s: the builder\'s re-check (chart, far >= 0, value >= chart + far, a_m) fails' % g)
        of[g] = (v, it)
    z2 = j_uniform(m3r.entry_ball(rec, 'D_Z2'), False)
    zr = [j_uniform(m3r.entry_ball(rec, 'G4R_%d' % r), True) for r in range(3)]
    return rec, okm, of, z2, zr


def plant_m3(n, mutate_rec=None, mutate_out=None, j_ref=150):
    """loads on a modified copy of N n's record or asm output, the RECORD line re-bound to the modified bytes; True if refused."""
    (pj, _), (po, _), _ = M3FILES[n]
    rec_text = open(os.path.join(CODEDIR, pj)).read()
    out_text = open(os.path.join(CODEDIR, po)).read()
    if mutate_rec is not None:
        obj = json.loads(rec_text)
        mutate_rec(obj)
        rec_text = json.dumps(obj)
    name = os.path.basename(pj)
    new_sha = hashlib.sha256(rec_text.encode()).hexdigest()
    out_text = '\n'.join(('RECORD %s %s' % (name, new_sha)) if ln.startswith('RECORD %s ' % name) else ln for ln in out_text.splitlines()) + '\n'
    if mutate_out is not None:
        out_text = mutate_out(out_text)
    try:
        m3r.loads(rec_text, out_text, j_ref, n, name)
        return False
    except ValueError:
        return True


def plants(n, fires):
    def precert(o):
        o['format'] = o['format'] + '_PRECERT'

    def kind(o):
        o['items']['VAC_OF_E4']['kind'] = 'entry'

    def mf(o):
        o['items']['VAC_OF_E4']['law']['mF'] = 3

    def layer(o):
        o['kernel_sha256'] = MA_DENY[0]                    # the record's kernel fields are top-level (m3_vac_*_v2_1.json)
    res = [('PLANT-PRECERT', plant_m3(n, precert)), ('PLANT-KIND', plant_m3(n, kind)), ('PLANT-MF', plant_m3(n, mf)),
           ('PLANT-LAYER', plant_m3(n, layer)), ('PLANT-JREF', plant_m3(n, j_ref=300)),
           ('PLANT-VERDICT', plant_m3(n, mutate_out=lambda s: s.replace('VERDICT VALID', 'VERDICT VALID-PRECERT')))]
    for name, fired in res:
        print('%s N=%d: %s' % (name, n, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('%s n%d' % (name, n))


def s4_rtr(n, key='RTR'):
    """N<n>_RTR (or N<n>_TARGET_FLOAT) of pk08's record, as printed."""
    hit = [ln for ln in open(os.path.join(CODEDIR, 'pk08/S4_RTR_CERTIFIED_v1.md')).read().splitlines() if ln.startswith('N%d_%s = ' % (n, key))]
    if len(hit) != 1:
        raise ValueError('S4 record: %d N%d_%s lines' % (len(hit), n, key))
    v = hit[0].split(' = ', 1)[1].strip()
    if not rdr.DEC.fullmatch(v):
        raise ValueError('S4 record: N%d_%s %r is not a decimal' % (n, key, v))
    return v


def z2_float(n):
    """vac_float's Z2 for the headroom quote: vacmono_N<n>.txt's 'Z2low(J1) = ...' as printed (FLOATQ, pinned)."""
    mt = re.search(r'Z2low\(J1\) = ([0-9.]+);', open(os.path.join(CODEDIR, 'pk10/scratch/vacmono_N%d.txt' % n)).read())
    if mt is None or not rdr.DEC.fullmatch(mt.group(1)):
        raise ValueError('vacmono_N%d.txt: no Z2low(J1) value' % n)
    return mt.group(1)


def assemble(n, fires):
    """every key of N n as a string at its safe end, the lambda*s, the HEADs' rho_pp_hex, and the checks."""
    rp = os.path.join(OWN, 'out', 'out_m2b_rep_v1_5_n%d.out' % n)
    rl = open(rp).read().splitlines()
    gate('C-REP N=%d' % n, bool(rl) and rl[0].startswith('m2b_rep_v1_5 sha256 %s N=%d' % (CODE['pk02/m2b_rep_v1_5.py'], n)) and
         [ln for ln in rl if ln.startswith('VERDICT')] == ['VERDICT VALID'], 'm2b_rep_v1_5 output %s (sha256 %s): C-REP, C-REP-BOUND, '
         'C-ANCHOR and plants' % (os.path.basename(rp), sha_file(rp)[:8]))
    vals, lams, heads = pieces_of(n)
    hx = sorted(set(h[18] for h in heads.values()))
    rec, okm, of, z2, zr = m3_items(n)
    okb = hx == [RHO_PP_HEX_PIN] and all(Fraction(h[12]) == A_M and Fraction(h[14]) == A_E and Fraction(h[16]) == Fraction(float.fromhex(hx[0])) ** 2
                               for h in heads.values()) and all(Fraction(of[g][1]['a_m']) == A_M for g in of)
    okb = okb and bool(farb(Fraction(float.fromhex(hx[0])) ** 2) >= (arb('0.55').asin() + DELTA).sin() ** 2)
    gate('C-BOUND N=%d' % n, okb, 'the ten hand-off HEADs carry one rho_pp_hex (%s), equal to RHO_PP_HEX_PIN; a_m = every VAC_OF law.a_m = Fraction(0.55)^2; '
         'a_e = Fraction(0.6)^2; a_pp = Fraction(rho_pp)^2 >= sin^2(asin rho_m + delta)' % ' '.join(hx))
    pb = Fraction('0.3025') != Fraction(of['E4'][1]['a_m'])
    print('PLANT-BOUND N=%d: a near boundary of 0.3025 against law.a_m -> %s' % (n, 'FIRES' if pb else 'DOES NOT FIRE'))
    if not pb:
        fires.append('PLANT-BOUND n%d' % n)
    gate('C-M3-MANIFEST N=%d' % n, okm, 'pk03\'s asm manifest names the record and the asm output with their pinned sha256')
    mh, okmh, m = mhat_up(n)
    gate('C-MHAT N=%d' % n, okmh, 'm1..m3 = %r >= 0 exactly; MHAT_UP %s >= mhat(t) at t = 1/300, 1/600, 1/1200, 0' % (m, mh))
    pm = not all(x >= 0 for x in (m[0], -m[1], m[2]))
    print('PLANT-MHAT N=%d: m2 := -m2 fails the sign test -> %s' % (n, 'FIRES' if pm else 'DOES NOT FIRE'))
    if not pm:
        fires.append('PLANT-MHAT n%d' % n)
    with open(os.path.join(CODEDIR, 'pk11/out/vacres_K3_N%d_sym_v1.json' % n)) as fh:
        R = json.load(fh)
    q = [None, R['q1'], R['q2'], R['q3']]
    mha = arb(mh)
    far = farb(of['E4'][0]) + 2 * mha * farb(of['E3'][0]) + mha * mha * farb(of['ED'][0])
    gsum = sum(((-arb('0.95') * 150 * (1 - DELTA.cos())).exp() * ratio_main(r, n - 1) * farb(zr[r]) for r in range(3)), arb(0))
    gb = supp(q, 150) * gsum.sqrt()
    keys = {k: dec_up(frac_upper(vals[k])) for k in ('NP', 'R1', 'D5', 'R0', 'TX', 'TB', 'ANN')}
    keys.update(TX_LAMSTAR=lams['TX'], ANN_LAMSTAR=lams['ANN'], FAR=dec_up(frac_upper(far)), MHAT_UP=mh, GB=dec_up(frac_upper(gb)),
                Z2=dec_down(z2), RTR=s4_rtr(n), AE=dec_down(A_E, 17), Z2_FLOAT=z2_float(n), RTR_FLOAT=s4_rtr(n, 'TARGET_FLOAT'))
    keys.update(Z2_FACTOR=dec_up(Fraction(keys['Z2_FLOAT']) / Fraction(keys['Z2'])), RTR_FACTOR=dec_up(Fraction(keys['RTR']) /
                                                                                                     Fraction(keys['RTR_FLOAT'])))
    for w in ('wt', 'dl'):
        keys[w.upper()] = ' ; '.join(dec_up(frac_upper(vals[k + '_' + w])) for k in ('NPM', 'D5W', 'R0W'))
        keys[w.upper() + '_R1'] = dec_up(frac_upper(vals['R1_' + w]))
    plants(n, fires)
    return keys, hx[0], rec


def kappa_b_key():
    amax = farb(A_E)
    kap = 2 * (1 - DELTA.cos()) - amax ** 2 / (4 * (1 - amax))
    return dec_down(frac_lower(kap))


def pin_value(tab):
    return ' ; '.join('%s:%s' % (p, h) for p, h in tab)


def main():
    fires = []
    try:
        per = {n: assemble(n, fires) for n in (4, 3)}
    except (ValueError, OSError, KeyError) as e:
        print('REFUSED: %s' % e)
        print('VERDICT INVALID (REFUSED)')
        return 1
    hx = sorted(set(per[n][1] for n in (4, 3)))
    gate('C-BOUND both N', len(hx) == 1, 'rho_pp_hex %s at N = 4 and 3' % ' '.join(hx))
    const = {'FORMAT': 'M2B_KV_v1', 'RECORD': 'M2B_KV_v1', 'AUTHOR': 'pk02',
             'WRITTEN_UTC': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'CLAIM': rdr.CLAIM, 'LAW': 'v1', 'J1': '150', 'J0': '170',
             'J_MIN': '300', 'CXI': '0.6594', 'VQ': '0.66767 ; 0.56373', 'KAPPA': '0.41729', 'KAPPA_B': kappa_b_key(), 'A_M': str(A_M),
             'A_E': str(A_E), 'A_PP': str(Fraction(float.fromhex(hx[0])) ** 2), 'RHO_PP_HEX': hx[0], 'ASM_SHA256': SELF_SHA}
    recd = {'const': {k: (v, rdr.KEYS_CONST[k]) for k, v in const.items()}}
    for n in (4, 3):
        keys = per[n][0]
        recd['N%d' % n] = {k: (v, rdr.KEYS_N[k]) for k, v in keys.items()}
        P = rdr.balls_of(recd, n)
        law = rdr.law_balls(P, arb(300))
        for k, nm in rdr.FMT:
            keys[k] = dec_up(frac_upper(law[nm]), 12)
        e3 = [rdr.law_balls(P, arb(J))['eps_r'] for J in (300, 600, 1200)]
        gate('C-LAW N=%d' % n, bool(e3[0] >= e3[1]) and bool(e3[1] >= e3[2]), 'LAW v1 eps_r at J = 300, 600, 1200: %s, %s, %s' % tuple(
            x.str(6) for x in e3))
    why = FAILS + ['%s did not fire' % x for x in fires]
    if why:
        print('NO RECORD: %s' % ', '.join(why))
        print('VERDICT INVALID (%s)' % ', '.join(why))
        return 1
    pins = {'PIN_CODE': pin_value(sorted(CODE.items()) + [('pk02/m2b_asm_v1.py', SELF_SHA)]), 'PIN_LAYER': pin_value(sorted(LAYER.items())),
            'PIN_TRIAL': pin_value(sorted(TRIAL.items())), 'PIN_M3_CODE': pin_value(sorted(M3CODE.items())), 'PIN_S4': pin_value(sorted(S4.items()))}
    for n in (4, 3):
        pp = []
        for piece in PIECES:
            for nm in ('out_%s_%s.n%d.out' % (PRODUCER[piece], piece, n), 'hand_%s_%s.n%d.txt' % (PRODUCER[piece], piece, n)):
                pp.append(('pk02/' + nm, sha_file(os.path.join(OWN, nm))))
        pins['PIN_PIECES_N%d' % n] = pin_value(pp)
        pins['PIN_M3_N%d' % n] = pin_value(M3FILES[n])
    pins['PIN_REP'] = pin_value([('pk02/out/out_m2b_rep_v1_5_n%d.out' % n, sha_file(os.path.join(OWN, 'out', 'out_m2b_rep_v1_5_n%d.out' % n)))
                                 for n in (4, 3)] + sorted(FLOATREC.items()))
    L = ['# M2B_KV_v1: the certified vacuum record of M2(b) (SPEC_M2B_CERT_v1 with ADD1 and ADD2), written by m2b_asm_v1.',
         '# Format S4U_KV_v1 style: one "KEY = value" per line; # lines are comments. Read it only through m2b_reader_v1 (load, bound to the',
         '# asm output that names this file with its sha256). Lists are separated by " ; "; PIN_* tokens are path:sha256 under code/.',
         '# Safe ends (SPEC sect. 3a): lower for N*_Z2, N*_AE and KAPPA_B; exact for the constants, the lambda*s and the pins; upper otherwise.']
    L += ['%s = %s' % (k, const[k]) for k in rdr.KEYS_CONST if k != 'VERDICT']
    for n in (4, 3):
        L += ['N%d_%s = %s' % (n, k, per[n][0][k]) for k in rdr.KEYS_N]
    L += ['%s = %s' % (k, pins[k]) for k in rdr.KEYS_PIN] + ['VERDICT = VALID']
    text = '\n'.join(L) + '\n'
    try:
        rdr.check(text)
        okr = True
    except ValueError as e:
        okr = False
        print('READBACK refused: %s' % e)
    gate('C-FMT (read back through m2b_reader_v1.check)', okr, 'the record passes every reader check, C-MONO and LAW v1 at J = 300')
    if FAILS:
        print('NO RECORD: %s' % ', '.join(FAILS))
        print('VERDICT INVALID (%s)' % ', '.join(FAILS))
        return 1
    with open(OUTREC, 'x') as fh:
        fh.write(text)
    os.chmod(OUTREC, 0o444)
    print('RECORD %s %s' % (os.path.basename(OUTREC), sha_file(OUTREC)))
    print('VERDICT VALID')
    return 0


if __name__ == '__main__':
    sys.exit(main())
