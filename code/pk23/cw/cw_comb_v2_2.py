#!/usr/bin/env python3
"""cw_comb_v2_2.py (pk23, C_w variant B): cw_comb_v2_0.py (sha256 53c028369f75bc9079bce9c45b17319d00b9ca624fb616e14353b2c9906c8107) with IhR,10',b read through pk22's law certificate
m3_lawcert_c3k_v2 (sha256 c14e0e1a486302f29e732d85258d8f73b38f4b72d0547be8642e56ef1bdba607; the records m3_c3kp_E4D/E4N_N<N>_J300_c3kp.json, loaded with load bound to m3_run_v1_9_3_asm.<N>_c3k2.out,
and the certificate with load_lawcert bound to m3_lawcert_c3k_v2_<N>.out) through pk23's reader fork m3_reader_cw_v1_1 (sha256 361661a2204e88bdb3d89eb16361ea566e2bb29156be10b5f088aeec2e0eb6a0),
the P2 table pk25/p2/v3f2/MR_LEMMAP_V3F.kv (sha256 9ef6abafdf450eff317545dd95aff519051352db3c01c752f739466a616d48c4) pinned, and the record's STATUS decided by the run: CERTIFIED when every gate passes, every plant fires,
both N run on state 10' and the P2 table's header says STATUS = CERTIFIED and RUN_VERDICT = VALID; DRY otherwise, with the DRY inputs
named on the DRY_INPUTS line. The VERDICT line is exactly VERDICT VALID when every gate passes and every plant fires; a STATUS line follows
it. For P3 (pk25's confirmation of CW_X11_v1): jlo and jhi are MR_LEMMAP v3's tokens exactly; the header carries LEMMAP_SHA256,
TRIAL_SET (MR_LEMMAP v3's line), TRIAL_SET_10P (psi_xy''s trial file per N with its sha256) and DEFINITIONS. The notes on
v2_0 (9994a402), closed here: C-SQ2's sentence below words the normalisation factors as additive O(t^2) corrections; yes, the
T2 class carries the products of the first-order coefficients into R: __mul__'s R holds c1 d1 (the exact t^2 remainder of the product),
and inv's R holds (c1 + R t)^2 / (y0^3 (1 + eps)) from 1/(1 + e) = 1 - e + e^2/(1 + e), valid while 1 + eps does not hold 0 over the
piece's ball T, which C-FINITE checks on every piece (an arb ball that holds 0 makes the result infinite). C-FINITE's plant (the row
4655), PLANT-FINITE: on the first piece, TT00 with a_1 = -a_0/t_mid makes the 1 + eps of its inverse hold 0 over T, and the piece must be
refused. cw_comb_v2_0's per-piece lines for C-KAPPA's factor and for x1t_hi and c_h' move into the helpers fac_of and x1t_chp, which
the plant shares. Exact tokens (the row 4691; the class of P2's finite_rows fix): jlo, jhi and C-KAPPA's table
fields enter every bound as the exact Fractions of their tokens (tq, tmax; never float()); T is [1/jhi, 1/jlo] ([0, 1/jlo] on the last
piece) from those endpoints. The floats jlo, jhi serve the piece selection, the DRY |Q f|/t and the printout only. Made by
make_cw_comb_v2_x4.py. cw_comb_v2_0's docstring follows.
cw_comb_v2_0.py (pk23, C_w variant B; the P0_LOG rows 4589, 4610, 4620, 4633, 4638; pk25's D2_DESIGN_v1_3 sect. (d), its P2 note
and pk24's MIDROW_G6_SPEC_v1_7 sect. 4.3, Lemma mu_pe): the comb of C_w's (1,1) block for P3, per piece of MR_LEMMAP v3 and both N, with the
record writer, and the DRY |Q f|/t of the triangle form on every piece, the last one [1008859.4, inf) included. The T2 class, LawItem, c_t2
and rows_t2 are cw_comb_v1_4's (d620ef48), unchanged.
What the record claims once its inputs are certified (this version writes STATUS = DRY: the c3kp law certificate and N4 record, and P2's
certified table, are not out yet):
  x1t_hi t >= |Q_xy S M_c' x_1| >= |Q_ext S M_c' x_1| for every J of the piece (t = 1/J, the last piece to t = 0), x_1 = psi_1/|psi_1| (trial
  state 1, e1), Q_xy = I - |psi_xy'><psi_xy'| / |psi_xy'|^2 (state 10'), M_c' = M_h - c_h', c_h' = Mh00/TT00 = <S psi_0, M_h S psi_0> /
  <S psi_0, S psi_0>, and chp_lo <= c_h' <= chp_hi. ran Q_ext lies in ran Q_xy since P_ext contains psi_xy'.
The comb: X11 = kappa_L N11 - (kappa P1)^2/G_xy' (cw_comb_v1's form): N11 = Cxx - c_h'(Cx1 + C1x) + c_h'^2 C11 (pk23's certified LC laws),
kappa_L = g00/TT00, kappa = g00/T00, P1 = IhR,10',1 - c_h' T10',1, with G_xy' and T10',b built from S8's D and N laws times pk22's exact
c'(t) (psixy_exact_d_v2). Each input is a second-order form y = c0 + c1 t + t^2 R on the piece (class T2: the laws' true coefficients in c0
and c1; R holds a2 + a3 t, their radii and the law certificate's B(J) J^2: B(jlo) jhi^2 on a finite piece, B(jlo) jlo^2 on the last one
under C-MONO-LAST2).
- C-SQ2: X11's c0 and c1 balls hold 0 on every piece. Their true values are 0: Q_xy S M_c' psi_1 vanishes at t^0, since S M_c' psi_1(0) is a
  multiple of psi_xy'(0) = x_1 (x) y exactly (state 10'), and X11 main_D is its squared norm plus (a0/a2 - 1) A - ((a0/a1)^2 - 1)
  P^2/|psi_xy'|^2 (C-KAPPA's notation), additive corrections that are O(t^2) since a0 - a_k = |r|^2 - <r, S^k r> = O(t^2) for psi_0 =
  alpha u + r; so on the piece X11 <= t^2 max(R_hi, 0).
- C-KAPPA: in true units X11 = [(a0/a2) A - (a0/a1)^2 P^2/|psi_xy'|^2] / main_D, with a_k = <psi_0, S^k psi_0>, A = |S M_c' psi_1|^2 and
  P = <psi_xy', S M_c' psi_1>. Since 0 <= S <= 1, a0 >= a1 >= a2, so |Q_xy S M_c' psi_1|^2 / main_D <= X11 + ((a0/a1)^2 - 1) sub, with
  sub = (kappa P1)^2/G_xy' >= (P^2/|psi_xy'|^2)/main_D. And 1 - a1/a0 <= sin^2 angle(psi_0, u) <= |x_0 - u|^2 <= d_x0^2, d_x0 = |1 - c_0| +
  |c_1| + |c_3| + delta_0 (u~_0's coefficients on the unit vectors; delta_0^2 <= 2 (q_0^2 + eps_x0^2 + eps_y0^2), L3). d_x0 comes from
  MR_LEMMAP v3 on a finite piece (the correction over t^2 is at most sub (2 d^2/(1 - d^2)^2) jhi^2) and from P2's /t fields on the last
  piece (2 d_t^2/(1 - (d_t/jlo)^2)^2, with uhat_0(0) = (1, 0, 0) exactly from P2's UHAT0).
- So x1t_hi = ((max(R_hi, 0) + corr) / g11_lo)^1/2, rounded up; g11 = |psi_1|^2 / main_D from S8's D law.
Gates: C-PINS, C-PIN-10P, C-10P, C-MIRROR, C-ROWS (state 10's rows against e12_comb_v1's float series: the rows code), C-T0, C-SQ2,
C-MONO-LAST2, C-UHAT0; C-CH reports c_h' against MR_JOINT's c_h (no gate). Plants: PLANT-SQ2 (Cxx's a0 moved by 1e-6 must fail C-SQ2),
PLANT-10P (state 10's trial set in place of 10' must fail C-10P), PLANT-MONO (a far rate of 1e-7 must fail C-MONO-LAST2).
DRY |Q f|/t (the triangle form of D2 v1_3 with pk25's change (1) and the spec's use of mu_pe; P3 assembles it in CERT):
  |Q f|/t <= mu_x [ |u_x1| x1t + |u_xp| (C_h + mu_pe d_x0t) + mu_pe |u_x3|/t + |u_x1| |c_h - c_h'| r_t ] + mu_pe rhox/t,
  with mu_x <= sx_hi (Cauchy interlacing: u~_x is the second Ritz vector, 0 <= S), mu_pe = C_hi tau_hi^1/2 (Lemma mu_pe), u_x3(0) = 0 (P2's
  UHAT0), |u_x3|/t, rhox/t and d_x0t from P2's /t fields, |u_x1| and |u_xp| from MR_LEMMAP v3, r_t = (rho0t^2 + rhoxt^2 + rhoyt^2)^1/2 >=
  |Q_W S x_1|/t >= |Q_ext S x_1|/t, and |c_h - c_h'| from MR_JOINT's ch and the comb's c_h'. C_h (S9(b)'s |Q v_h| = C_h t) is a DRY
  constant here: the larger of kt_rb's certified |Q v_h| at J 300 times 300 (the spec's CERT300C lines) and S9(b)-h's float (S9H brief).
Usage: cw_comb_v2_0.py OUT JS4 JS3 STATE4 STATE3 (OUT a new file in pk23/cw/out; STATE 10p, or 10 as a DRY stand-in while that N's c3kp
record is missing). Prints the gates, plants, summary lines and the RECORD line."""
import copy, hashlib, importlib.util, json, math, os, re, sys
from fractions import Fraction as Fr
import flint
flint.ctx.prec = 256
arb, fmpq = flint.arb, flint.fmpq
W18 = '/mnt/g2/release/root/code'
HLD, CWD = W18 + '/pk23/pev', W18 + '/pk23/cw'
M3O, S3O = W18 + '/pk03/out', W18 + '/pk22/m3/out'
PSX = W18 + '/pk22/midrow/psixy'
MRL3, MRI, MRS = W18 + '/pk25/mr/v3/MR_LEMMAP.kv', W18 + '/pk25/mr/v4b/MR_INSERT.kv', W18 + '/pk25/mr/v4/MR_SPECTRAL.kv'
P2F = W18 + '/pk25/p2/v3f2/MR_LEMMAP_V3F.kv'
MRJ = W18 + '/pk22/midrow/g4/mrc/out/cert/MR_JOINT_CERT_v1.kv'
SPEC, S9HB = W18 + '/pk24/MIDROW_G6_SPEC_v1_7.md', W18 + '/notes/S9H_G5_BRIEF_v1.md'
RDRF = HLD + '/m3_reader_cw_v1_1.py'
C3K2F = W18 + '/pk22/m3/m3_lawcert_c3k_v2.py'
PINS = {MRL3: '275b179f', MRI: '46d3aeb5', MRS: '4a609ccf', P2F: '9ef6abaf', MRJ: 'b0331e56', RDRF: '361661a2', C3K2F: 'c14e0e1a'}
ROOM = {4: (2.1489 - 1.3407, 2.957), 3: (1.6612 - 0.4338, 2.889)}   # KC3's design room (D2 v1 sect. 0); the hard C-SIGN room (the rows 4610, 4620)
LCK = ('Cxx,1,1', 'Cx1,1,1', 'C1x,1,1', 'C11,1,1')
FAILS, NOFIRE = [], []
assert len(sys.argv) == 6, __doc__.split('Usage: ')[1]
OUT = os.path.abspath(sys.argv[1])
JSN = {4: float(sys.argv[2]), 3: float(sys.argv[3])}
STN = {4: sys.argv[4], 3: sys.argv[5]}
assert os.path.dirname(OUT) == CWD + '/out' and not os.path.exists(OUT), 'OUT must be a new file in pk23/cw/out'
assert all(s in ('10', '10p') for s in STN.values()), 'STATE must be 10 or 10p'


def out(line):
    print(line, flush=True)


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def ab(q):
    q = Fr(q)
    return arb(fmpq(q.numerator, q.denominator))


def hi(x):
    """a float >= the arb x (its upper end, one step up)."""
    return math.nextafter(float(x.upper()), math.inf)


def lo(x):
    return math.nextafter(float(x.lower()), -math.inf)


def chi2_tail(n, x):
    """Prob(chi^2_n > x) for n = 2, 3 (pk22's e4_comb_v1_1, the forms its law certificates use)."""
    if n == 2:
        return (-x / 2).exp()
    assert n == 3
    return (x / 2).sqrt().erfc() + (2 * x / arb.pi()).sqrt() * (-x / 2).exp()


def p_law(g, J):
    return sum((chi2_tail(int(g['n']), ab(J) * ab(a) / ab(G)) for a, G in g['a_G']), arb(0))


class T2:
    """y(t) = c0 + c1 t + t^2 R for every t of the piece; T is the piece's t-ball."""
    def __init__(self, c0, c1, R, T):
        self.c0, self.c1, self.R, self.T = c0, c1, R, T

    def __add__(self, o):
        return T2(self.c0 + o.c0, self.c1 + o.c1, self.R + o.R, self.T)

    def __sub__(self, o):
        return T2(self.c0 - o.c0, self.c1 - o.c1, self.R - o.R, self.T)

    def scale(self, s):
        return T2(self.c0 * s, self.c1 * s, self.R * s, self.T)

    def __mul__(self, o):
        T = self.T
        R = self.c0 * o.R + o.c0 * self.R + self.c1 * o.c1 + T * (self.c1 * o.R + o.c1 * self.R) + T * T * self.R * o.R
        return T2(self.c0 * o.c0, self.c0 * o.c1 + self.c1 * o.c0, R, T)

    def inv(self):
        T, y0 = self.T, self.c0
        eps = (self.c1 * T + self.R * T * T) / y0
        R = -self.R / (y0 * y0) + ((self.c1 + self.R * T) / y0) ** 2 / (y0 * (1 + eps))
        return T2(1 / y0, -self.c1 / (y0 * y0), R, T)

    def value(self):
        return self.c0 + self.c1 * self.T + self.R * self.T * self.T


class LawItem:
    """one certified entry through the reader's entry_law (ak, ak_rad as exact rationals; parts and laws of the certificate)."""
    def __init__(self, name, law):
        self.name, self.law = name, law
        self.ak = [Fr(x) for x in law['ak']]
        self.rad = [Fr(x) for x in law['ak_rad']]

    def B(self, J):
        lw, bp, J = self.law['laws'], self.law['parts'], Fr(J)
        e = ab(bp['rem']) * (ab(Fr(300) / J) ** 4)
        for part in ('tail', 'ann'):
            e = e + ab(bp[part]) * (p_law(lw[part], J) / p_law(lw[part], Fr(300))).sqrt()
        e = e + ab(bp['far']) * (-ab(lw['far_rate']) * ab(J - 300)).exp()
        return e.upper()

    def mono_last2(self, jlo):
        """J^2 B(J) non-increasing from jlo: rate jlo >= 2 and 4/kappa <= jlo for tail and ann (log-concave chi-square tails)."""
        lw = self.law['laws']
        rate = Fr(lw['far_rate'])
        ok = rate > 0 and rate * jlo >= 2
        for part in ('tail', 'ann'):
            g, kap = lw[part], None
            for a, G in g['a_G']:
                r = Fr(a) / Fr(G)
                k = r / 2 if int(g['n']) == 2 else r * (jlo * r) / (2 * (1 + jlo * r))
                kap = k if kap is None or k < kap else kap
            ok = ok and kap is not None and kap > 0 and 4 / kap <= jlo
        return ok

    def t2(self, jlo, jhi, T):
        Bj = self.B(jlo)
        Bt2 = (ab(jlo) * ab(jlo) * Bj).upper() if jhi is None else (ab(jhi) * ab(jhi) * Bj).upper()
        R = ab(self.ak[2]) + ab(self.ak[3]) * T + arb(0, (ab(self.rad[2]) + ab(self.rad[3]) * T.upper() + Bt2).upper())
        return T2(ab(self.ak[0]) + arb(0, ab(self.rad[0]).upper()), ab(self.ak[1]) + arb(0, ab(self.rad[1]).upper()), R, T)


def load_as(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def c_t2(T, xd, support):
    """the exact c(t) of psixy_exact_d (c_pv for state 0) as second-order forms on the piece: c_pv = d_0 S00 / (1 + tau),
    tau = S00 (t e1_0 + t^2 e2_0 + t^3 e3_0), c_a = d_a - c_pv (t e1_a + t^2 e2_a + t^3 e3_a)."""
    XS00, Xd, Xe = xd[0], xd[1], xd[2]
    poly = lambda a: T2(arb(0), ab(Xe[0][a]), ab(Xe[1][a]) + ab(Xe[2][a]) * T, T)
    one_tau = T2(arb(1), arb(0), arb(0), T) + poly(0).scale(ab(XS00))
    cpv = one_tau.inv().scale(ab(Xd[0] * XS00))
    out_ = {0: cpv}
    for a in support:
        if a:
            out_[a] = T2(ab(Xd[a]), arb(0), arb(0), T) - cpv * poly(a)
    return out_


def rows_t2(g_, T, xd, support):
    """T10,b (b = 0, 1, 3) and G10,10 from S8's certified laws and the exact c(t), each a second-order form on the piece."""
    c = c_t2(T, xd, support)
    key = lambda pre, a, b: '%s,%d,%d' % (pre, min(a, b), max(a, b))
    zero = T2(arb(0), arb(0), arb(0), T)
    res = {}
    for b in (0, 1, 3):
        acc = zero
        for a in support:
            acc = acc + c[a] * g_[key('T', a, b)]
        res['T10,%d' % b] = acc
    acc = zero
    for a in support:
        for a2 in support:
            acc = acc + c[a] * c[a2] * g_[key('g', a, a2)]
    res['G10,10'] = acc
    return res


def kv_table(path, N, suffix=''):
    """an MR_INPUT_KV-style table: (header {name: text}, ordered keys, {key: {field: float, or None for inf}}) for the rows N<N>_P<i><suffix>."""
    head, keys, rows, fields = {}, [], {}, None
    for ln in open(path).read().split('\n'):
        m = re.match(r'^(N%d_P\d+)%s = (.*)$' % (N, re.escape(suffix)), ln)
        if m:
            v = m.group(2).split()
            assert fields is not None and len(v) >= len(fields), (path, m.group(1))
            keys.append(m.group(1))
            rows[m.group(1)] = dict((f, (None if x == 'inf' else (x if x in ('True', 'False') else float(x)))) for f, x in zip(fields, v))
            rows[m.group(1)]['_tok'] = dict(zip(fields, v))   # the table's own tokens (the record copies jlo and jhi exactly)
            continue
        m = re.match(r'^([A-Za-z0-9_]+) = (.*)$', ln)
        if m and not re.match(r'^N\d_P\d+', m.group(1)):
            head[m.group(1)] = m.group(2)
            if m.group(1) == 'FIELDS':
                fields = m.group(2).split()
    return head, keys, rows


def amax(r, f):
    return max(abs(r[f + '_lo']), abs(r[f + '_hi']))


def tq(row, f):
    """v2_2 (the row 4691): a table field as the exact Fraction of its token, never through float()."""
    return Fr(row['_tok'][f])


def tmax(row, f):
    return max(abs(tq(row, f + '_lo')), abs(tq(row, f + '_hi')))


# inputs and pins
for p, h8 in PINS.items():
    gate('C-PINS', sha(p).startswith(h8), '(%s sha256 %s, expected %s)' % (os.path.relpath(p, W18), sha(p)[:16], h8))
RDR = load_as('m3_reader_cw_v1', RDRF)
spec_txt, brief_txt = open(SPEC).read(), open(S9HB).read()
qv = dict((int(n), Fr(x)) for n, x in re.findall(r'CERT300C QV N=([43]) J=300: \|\|Q v_h\|\| <= \[([0-9.]+), ', spec_txt))
fl = re.search(r'float ([0-9.]+) t at N = 4,\s+([0-9.]+) t at N = 3', brief_txt)
CH_DRY = {4: max(float(qv[4] * 300), float(fl.group(1))), 3: max(float(qv[3] * 300), float(fl.group(2)))}
out('C_H DRY: kt_rb CERT300C |Q v_h| x 300 = %.6f (N4), %.6f (N3); S9(b)-h float %s (N4), %s (N3); used %.6f, %.6f' % (
    float(qv[4] * 300), float(qv[3] * 300), fl.group(1), fl.group(2), CH_DRY[4], CH_DRY[3]))
REC_ROWS, SUMMARY, TS_LINE = {}, [], {}


def run_n(N, JS, STATE):
    CERTS = {}
    for tag, fams, recpat, asm, cert, cout in (
            ('hl', ('L', 'LH', 'LT'), HLD + '/out/m3_hl_%s_N%d_J300_hl.json', HLD + '/out/m3_run_v1_9_3_asm.%d.out',
             HLD + '/out/m3_lawcert_hl_v1_1_N%d.json', HLD + '/out/m3_lawcert_hl_v1_1_%d.out'),
            ('s8', ('D', 'E2', 'E3', 'FF'), M3O + '/m3_s8v3_%s_N%d_J300_v1_8_1.json', M3O + '/m3_run_v1_8_1_asmP.%d.out',
             M3O + '/m3_lawcert_v1_1_N%d.json', M3O + '/m3_lawcert_v1_1_%d.out'),
            ('s8n', ('N',), M3O + '/m3_s8v3_%s_N%d_J300_v1_8_2.json', M3O + '/m3_run_v1_8_2_asmN.%d.out',
             M3O + '/m3_lawcert_v1_2_N%d.json', M3O + '/m3_lawcert_v1_2_%d.out'),
            ('c3k', ('E4D', 'E4N'), S3O + '/m3_c3k_%s_N%d_J300_c3k.json', S3O + '/m3_run_v1_9_3_asm.%d_c3k.out',
             S3O + '/m3_lawcert_c3k_v1_N%d.json', S3O + '/m3_lawcert_c3k_v1_%d.out'),
            ('cw', ('LC',), HLD + '/out/m3_cw_%s_N%d_J300_cw.json', HLD + '/out/m3_run_v1_9_3_asmc.%d.out',
             HLD + '/out/m3_lawcert_cw_v1_N%d.json', HLD + '/out/m3_lawcert_cw_v1_%d.out')):
        recs = dict((f, RDR.load(recpat % (f, N), asm % N, 300, N)) for f in fams)
        CERTS[tag] = RDR.load_lawcert(cert % N, cout % N, 300, N, recs)
        out('LAWCERT %s N=%d: %s (%s), %d entries' % (tag, N, os.path.basename(cert % N), CERTS[tag]['producer'], len(CERTS[tag]['entries'])))
    LI = lambda tag, fam, key: LawItem('%s:%s' % (fam, key), RDR.entry_law(CERTS[tag], fam, key))
    IT = {'TT00': LI('hl', 'L', 'TT,0,0'), 'Mh00': LI('hl', 'LH', 'Mh,0,0'), 'g00': LI('s8', 'D', 'g,0,0'), 'g11': LI('s8', 'D', 'g,1,1'),
          'g33': LI('s8', 'D', 'g,3,3'), 'T00': LI('s8n', 'N', 'T,0,0')}
    for k in LCK:
        IT[k] = LI('cw', 'LC', k)
    C3KP = {}
    if STATE == '10p':   # pk22's c3k rerun on 10', through its law certificate m3_lawcert_c3k_v2
        for f in ('E4D', 'E4N'):
            C3KP[f] = RDR.load(S3O + '/m3_c3kp_%s_N%d_J300_c3kp.json' % (f, N), S3O + '/m3_run_v1_9_3_asm.%d_c3k2.out' % N, 300, N)
        CERTS['c3kp'] = RDR.load_lawcert(S3O + '/m3_lawcert_c3k_v2_N%d.json' % N, S3O + '/m3_lawcert_c3k_v2_%d.out' % N, 300, N, C3KP)
        out('LAWCERT c3kp N=%d: m3_lawcert_c3k_v2_N%d.json (%s), %d entries; records %s' % (N, N, CERTS['c3kp']['producer'], len(CERTS['c3kp']['entries']),
                                                                                    ', '.join('%s %s' % (r_['name'], r_['sha256'][:16]) for r_ in C3KP.values())))
    for b in (0, 1, 3):
        IT['IhR%d' % b] = LI('c3kp', 'E4N', 'IhR,10,%d' % b) if STATE == '10p' else LI('c3k', 'E4N', 'IhR,10,%d' % b)
    XDF = {'10': PSX + '/out/psixy_exact_d_v1_n%d.json' % N, '10p': PSX + '/out/psixy_exact_d_v2_n%d.json' % N}
    XDATA = {}
    for st_, pth_ in XDF.items():
        xd_ = json.load(open(pth_))
        XDATA[st_] = (Fr(xd_['S00']), [Fr(x) for x in xd_['d']], [[Fr(x) for x in xd_['e%d' % k]] for k in (1, 2, 3)], list(xd_['support']),
                      xd_['trial_set'])
    SUP = XDATA['10'][3]
    assert XDATA['10p'][3] == SUP, 'the supports of 10 and 10p differ'
    for fam, pre, tag in (('D', 'g', 's8'), ('N', 'T', 's8n')):
        for a in SUP:
            for b in SUP:
                k_ = '%s,%d,%d' % (pre, min(a, b), max(a, b))
                if k_ not in IT:
                    IT[k_] = LI(tag, fam, k_)
    man10p = dict((ln.split()[1], ln.split()[0]) for ln in open(PSX + '/MANIFEST_PSIXY_10P_v1.sha256') if ln.strip())
    h10p = sha(XDF['10p'])
    gate('C-PIN-10P', man10p.get(XDF['10p']) == h10p, '(N=%d: psixy_exact_d_v2_n%d.json sha256 %s is its row in pk22\'s MANIFEST_PSIXY_10P_v1)' % (
        N, N, h10p[:16]))
    TS_LINE[N] = XDATA[STATE][4]
    if STATE == '10p':
        ts_rec = (C3KP['E4N']['top']['trial_set']['ts'], C3KP['E4D']['top']['trial_set']['ts'])
        gate('C-10P', XDATA['10p'][4] == ts_rec[0] == ts_rec[1],
             '(N=%d: the c3kp records\' trial set %s is the one psixy_exact_d_v2 names, so their 10\' is c\'(t)\'s 10\')' % (N, XDATA['10p'][4][:48]))
        plant('PLANT-10P', not (XDATA['10'][4] == ts_rec[0] == ts_rec[1]),
              '(N=%d: state 10\'s trial set %s in place of 10\'s must fail C-10P)' % (N, XDATA['10'][4][:48]))
    E12 = json.load(open(W18 + '/pk22/midrow/e12/out/e12_comb_v1_N%d.json' % N))['items']   # C-ROWS' float control only
    h3, k3, L3 = kv_table(MRL3, N)
    hp, kp, P2 = kv_table(P2F, N)
    _, _, INS = kv_table(MRI, N, '_h')
    _, _, SPE = kv_table(MRS, N)
    _, _, JNT = kv_table(MRJ, N)
    uh = hp.get('N%d_UHAT0' % N, '')
    toks = dict((t.split(' ', 1)[0], t.split(' ', 1)[1]) for t in (x.strip() for x in uh.split(';')) if ' ' in t)
    gate('C-UHAT0', toks.get('u0p') == '1' and toks.get('u01') == '0' and toks.get('u03') == '0' and toks.get('ux3') == '0' and k3 == kp,
         '(N=%d: P2\'s UHAT0 gives uhat_0(0) = (1, 0, 0) and uhat_x3(0) = 0 exactly; P2 and MR_LEMMAP v3 have the same %d pieces)' % (N, len(k3)))
    dm = max(abs(float(a - b)) for a, b in zip(IT['Cx1,1,1'].ak, IT['C1x,1,1'].ak))
    gate('C-MIRROR', dm <= 1e-9, '(N=%d: Cx1,1,1 against C1x,1,1, largest |a_k difference| %.2e; certified laws)' % (N, dm))
    lam1, lam2 = (3 - math.sqrt(5)) / 2, (5 - math.sqrt(21)) / 2
    sx0, sy0 = lam1 ** 2, lam2 ** 2
    ch0 = (N - 1) * (1 - 2 * math.sqrt(3.0 / 7) / 3) / 2
    chh = -(2.0 / 3) * (1 - lam2) ** 2 / math.sqrt(21)
    n11_0 = sx0 * sx0 * ((N - 1) * chh * chh / 2) * sy0   # s_x0^2 m_y^2 s_y0^2

    def x11_of(items, jlo, jhi, T, xd):
        g = dict((k, v.t2(Fr(jlo), None if jhi is None else Fr(jhi), T)) for k, v in items.items())
        g.update(rows_t2(g, T, xd, SUP))
        ch = g['Mh00'] * g['TT00'].inv()
        kap, kapL = g['g00'] * g['T00'].inv(), g['g00'] * g['TT00'].inv()
        N11 = g['Cxx,1,1'] - ch * (g['Cx1,1,1'] + g['C1x,1,1']) + ch * ch * g['C11,1,1']
        kP1 = kap * (g['IhR1'] - ch * g['T10,1'])
        sub = kP1 * kP1 * g['G10,10'].inv()
        return kapL * N11 - sub, sub, ch, N11, g

    def fac_of(key, r, last, jlo, jhi):
        """C-KAPPA's factor over t^2 on a piece (cw_comb_v2_0's lines moved here so that PLANT-FINITE shares them; v2_2: jlo and jhi
        exact Fractions and every table field its exact token)."""
        if last:
            p = P2[key]
            dt = ab(tmax(p, 'u0pt') + tmax(p, 'u01t') + tmax(p, 'u03t')) + (2 * (ab(tq(p, 'q0t_hi')) ** 2 + ab(tq(p, 'eps_x0t_hi')) ** 2
                                                                                + ab(tq(p, 'eps_y0t_hi')) ** 2)).sqrt()
            dmax = dt / ab(jlo)
            return 2 * dt * dt / (1 - dmax * dmax) ** 2
        d = ab(max(abs(1 - tq(r, 'u0p_lo')), abs(1 - tq(r, 'u0p_hi'))) + tmax(r, 'u01') + tmax(r, 'u03')) + (
            2 * (ab(tq(r, 'q0_hi')) ** 2 + ab(tq(r, 'eps_x0_hi')) ** 2 + ab(tq(r, 'eps_y0_hi')) ** 2)).sqrt()
        return 2 * d * d / (1 - d * d) ** 2 * ab(jhi) ** 2

    def x1t_chp(X11, sub, ch, g, fac, key):
        """x1t_hi, chp_lo, chp_hi, R_hi and the C-KAPPA term on a piece (cw_comb_v2_0's lines, unchanged, moved here so that PLANT-FINITE
        shares them)."""
        g11lo = g['g11'].value().lower()
        assert lo(g11lo) > 0, 'g11 not positive on %s' % key
        RX = X11.R.upper()
        RX = arb(0) if hi(RX) <= 0 else RX
        corr = sub.value().upper() * fac
        y2 = ((RX + corr) / g11lo).upper()
        chv = ch.value()
        return hi(y2.sqrt()), lo(chv), hi(chv), RX, corr

    rows_rec, first, worst, worst11, last_info, sq2_all, ccor, fin_all = [], None, None, None, None, True, 0.0, True
    for key in k3:
        r = L3[key]
        jlo, jhi = r['jlo'], r['jhi']                                   # floats: the selection, the DRY |Q f|/t and the printout only
        last = jhi is None
        jq = tq(r, 'jlo')                                               # v2_2: the exact tokens enter every bound (no float())
        hq = None if last else tq(r, 'jhi')
        tlo_q = Fr(0) if last else 1 / hq
        T = ab((1 / jq + tlo_q) / 2) + arb(0, ab((1 / jq - tlo_q) / 2).upper())   # v2_2: [1/jhi, 1/jlo] ([0, 1/jlo]) from exact endpoints
        if last:
            bad = sorted(k for k, v in IT.items() if not v.mono_last2(jq))
            gate('C-MONO-LAST2', not bad, '(N=%d: on the last piece from jlo %.1f, J^2 B(J) is non-increasing for every one of the %d laws (rate jlo >= 2; '
                 '4/kappa <= jlo for tail and ann); failing: %s)' % (N, jlo, len(IT), ', '.join(bad) or 'none'))
            pm = copy.copy(IT['Cxx,1,1'])
            pm.law = dict(pm.law)
            pm.law['laws'] = dict(pm.law['laws'])
            pm.law['laws']['far_rate'] = Fr(1, 10 ** 7)
            plant('PLANT-MONO', not pm.mono_last2(jq), '(N=%d: Cxx,1,1 with a far rate of 1e-7 must fail C-MONO-LAST2 at jlo %.1f)' % (N, jlo))
        if first is None:   # C-ROWS: the rows code on state 10 (v1's exact c(t)) against e12_comb_v1's float series (state 10)
            g0 = dict((k, v.t2(jq, hq, T)) for k, v in IT.items())
            g10 = rows_t2(g0, T, XDATA['10'], SUP)
            dr = max(max(abs(float(g10[k].c0.mid()) - float(E12[k]['A_float'][0])), abs(float(g10[k].c1.mid()) - float(E12[k]['A_float'][1])))
                     for k in ('T10,0', 'T10,1', 'T10,3', 'G10,10'))
            gate('C-ROWS', dr <= 1e-9, '(N=%d: T10,b and G10,10 from S8 laws times the exact c(t) of state 10: t^0 and t^1 against e12_comb_v1, '
                 'largest difference %.2e; the same code builds the rows of state %s)' % (N, dr, STATE))
        X11, sub, ch, N11, g = x11_of(IT, jq, hq, T, XDATA[STATE])
        if first is None:
            dn, dc = abs(float(N11.c0.mid()) - n11_0), abs(float(ch.c0.mid()) - ch0)
            gate('C-T0', dn <= 1e-12 + float(N11.c0.rad()) and dc <= 1e-12 + float(ch.c0.rad()),
                 '(N=%d: N11(0) %.12e against s_x0^2 m_y^2 s_y0^2 %.12e (difference %.1e); c_h\'(0) %s against c_h0 %.15f (difference %.1e))' % (
                     N, float(N11.c0.mid()), n11_0, dn, ch.c0.str(15), ch0, dc))
            pit = dict(IT)
            pc = copy.copy(IT['Cxx,1,1'])
            pc.ak = [pc.ak[0] + Fr(1, 10 ** 6)] + pc.ak[1:]
            pit['Cxx,1,1'] = pc
            Xp = x11_of(pit, jq, hq, T, XDATA[STATE])[0]
            plant('PLANT-SQ2', not (Xp.c0.contains(arb(0)) and Xp.c1.contains(arb(0))),
                  '(N=%d: Cxx,1,1 with a_0 moved by 1e-6 must fail C-SQ2 on the first piece: t^0 ball %s)' % (N, Xp.c0.str(3)))
            pif = dict(IT)   # PLANT-FINITE (the row 4655): TT00 with a_1 = -a_0/t_mid, so the 1 + eps of its inverse holds 0 over T
            pt = copy.copy(IT['TT00'])
            pt.ak = [pt.ak[0], -pt.ak[0] / ((1 / jq + 1 / hq) / 2)] + pt.ak[2:]
            pif['TT00'] = pt
            gtt = pt.t2(jq, hq, T)
            onef = 1 + (gtt.c1 * T + gtt.R * T * T) / gtt.c0
            try:
                Xf, subf, chf, _, gf = x11_of(pif, jq, hq, T, XDATA[STATE])
                xf = x1t_chp(Xf, subf, chf, gf, fac_of(key, r, False, jq, hq), key)
                refused, shown = not all(math.isfinite(v_) for v_ in xf[:3]), 'x1t_hi %s, c_h\' [%s, %s]' % xf[:3]
            except (ZeroDivisionError, ValueError, ArithmeticError) as exc_:
                refused, shown = True, 'the piece raised %s' % type(exc_).__name__
            plant('PLANT-FINITE', onef.contains(arb(0)) and refused,
                  '(N=%d: TT00 with a_1 = -a_0/t_mid makes 1 + eps of its inverse hold 0 over the first piece (1 + eps %s), and C-FINITE must '
                  'refuse the piece: %s)' % (N, onef.str(3), shown))
            first = key
        sq2 = X11.c0.contains(arb(0)) and X11.c1.contains(arb(0))
        sq2_all = sq2_all and sq2
        x1t, chp_lo, chp_hi, RX, corr = x1t_chp(X11, sub, ch, g, fac_of(key, r, last, jq, hq), key)
        fin_all = fin_all and all(math.isfinite(v_) for v_ in (x1t, chp_lo, chp_hi))
        ccor = max(ccor, float((corr / (RX + corr)).upper()) if hi(RX + corr) > 0 else 0.0)
        rows_rec.append((key, jlo, jhi, x1t, chp_lo, chp_hi, r['_tok']['jlo'], r['_tok']['jhi']))
        # the DRY |Q f|/t (P3's assembly, for the report)
        p, ins, spe, jn = P2[key], INS[key], SPE[key], JNT.get(key)
        mupe = ins['C_hi'] * math.sqrt(spe['tau_hi'])
        dxt = amax(p, 'u0pt') + amax(p, 'u01t') + amax(p, 'u03t') + math.sqrt(2 * (p['q0t_hi'] ** 2 + p['eps_x0t_hi'] ** 2 + p['eps_y0t_hi'] ** 2))
        rt = math.sqrt(p['rho0t_hi'] ** 2 + p['rhoxt_hi'] ** 2 + p['rhoyt_hi'] ** 2)
        dch = max(abs(jn['ch_hi'] - chp_lo), abs(chp_hi - jn['ch_lo'])) if jn else float('nan')
        p11, p0 = amax(r, 'ux1') * x1t, amax(r, 'uxp') * (CH_DRY[N] + mupe * dxt)
        p3, pch, prx = mupe * amax(p, 'ux3t'), amax(r, 'ux1') * dch * rt, mupe * p['rhoxt_hi']
        qft = spe['sx_hi'] * (p11 + p0 + p3 + pch) + prx
        if last:
            last_info = (jlo, x1t, qft, p11, p0, p3, pch, prx, mupe, spe['sx_hi'])
        if jlo >= JS:
            if worst is None or qft > worst[0]:
                worst = (qft, jlo, p11, p0, p3, pch, prx, mupe, spe['sx_hi'])
            if worst11 is None or x1t > worst11[0]:
                worst11 = (x1t, jlo)
    gate('C-SQ2', sq2_all and last_info is not None, '(N=%d STATE %s: X11\'s t^0 and t^1 balls hold 0 on all %d pieces, the last [%.1f, inf) included)' % (
        N, STATE, len(rows_rec), last_info[0] if last_info else float('nan')))
    gate('C-FINITE', fin_all, '(N=%d: x1t_hi and [chp_lo, chp_hi] are finite on all %d pieces, so every inverse 1/(y0 (1 + eps)) of the T2 class '
         'stayed away from 0 over the piece\'s ball T (the condition on N-2; its plant is PLANT-FINITE))' % (N, len(rows_rec)))
    js_row = next(x for x in rows_rec if x[1] >= JS)
    chm = [(x[0], x[4], x[5], JNT[x[0]]['ch_lo'], JNT[x[0]]['ch_hi']) for x in rows_rec if x[0] in JNT]
    ov = sum(1 for x in chm if x[1] <= x[4] and x[3] <= x[2])
    out('C-CH N=%d: c_h\' (comb) and MR_JOINT\'s c_h intervals overlap on %d of %d pieces; at the J_s piece %s c_h\' [%.12f, %.12f], ch [%.12f, %.12f] '
        '(no gate)' % (N, ov, len(chm), js_row[0], js_row[4], js_row[5], JNT[js_row[0]]['ch_lo'], JNT[js_row[0]]['ch_hi']))
    out('X1T N=%d STATE %s: x1t_hi %.6f at the J_s piece [%.1f, %.1f]; at most %.6f from J_s (at jlo %.1f); %.6f on the last piece [%.1f, inf); '
        'C-KAPPA share of (R + corr) at most %.2e; %d pieces from jlo %.2f' % (N, STATE, js_row[3], js_row[1], js_row[2], worst11[0], worst11[1],
                                                                            last_info[1], last_info[0], ccor, len(rows_rec), rows_rec[0][1]))
    rm, rh = ROOM[N]
    out('DRY QF N=%d JS %.0f: worst |Q f|/t %.4f at jlo %.1f (mu_x <= sx_hi %.5f times: (1,1) %.4f, psi-hat %.2e, e3 %.4f, c_h %.2e; plus r_x %.4f, '
        'mu_pe %.4f); against KC3\'s room %.4f -> %s; against the hard C-SIGN room %.3f -> %s' % (
            N, JS, worst[0], worst[1], worst[8], worst[2], worst[3], worst[4], worst[5], worst[6], worst[7], rm, 'inside' if worst[0] < rm else 'OUTSIDE',
            rh, 'inside' if worst[0] < rh else 'OUTSIDE'))
    out('DRY QF N=%d last piece [%.1f, inf): |Q f|/t %.4f (mu_x <= %.5f times: (1,1) %.4f, psi-hat %.2e, e3 %.4f, c_h %.2e; plus r_x %.4f)' % (
        N, last_info[0], last_info[2], last_info[9], last_info[3], last_info[4], last_info[5], last_info[6], last_info[7]))
    REC_ROWS[N] = rows_rec
    SUMMARY.append((N, STATE, js_row[3], worst11[0], last_info[1], worst[0], worst[1], last_info[2]))


for N in (4, 3):
    run_n(N, JSN[N], STN[N])
code_sha = sha(os.path.abspath(__file__))
verdict = 'VALID' if not FAILS and not NOFIRE else 'INVALID'
P2HEAD = kv_table(P2F, 4)[0]
dry_parts = (['N%d STATE 10 (state 10 for 10\')' % n for n in (4, 3) if STN[n] != '10p'] +
             ([] if (P2HEAD.get('STATUS') == 'CERTIFIED' and P2HEAD.get('RUN_VERDICT') == 'VALID') else
              ['P2 %s (STATUS %s) for the last piece\'s C-KAPPA term' % (os.path.relpath(P2F, W18), P2HEAD.get('STATUS'))]))
status = 'CERTIFIED' if verdict == 'VALID' and not dry_parts else 'DRY'
L = ['# CW_X11 (pk23, cw_comb_v2_2 %s): written by cw_comb_v2_2' % status, 'FORMAT = CW_X11_KV_v1', 'RECORD = CW_X11', 'PRODUCER = pk23 cw_comb_v2_2',
     'CODE = pk23/cw/cw_comb_v2_2.py:%s' % code_sha, 'STATUS = %s' % status, 'RUN_VERDICT = %s' % verdict,
     'CLAIM = on every piece (for every J in [jlo, jhi], t = 1/J, the last piece to t = 0): x1t_hi t >= |Q_xy S M_c\' x_1| >= |Q_ext S M_c\' x_1|, '
     'x_1 = psi_1/|psi_1|, Q_xy = I - |psi_xy\'><psi_xy\'|/|psi_xy\'|^2 (state 10\'), M_c\' = M_h - c_h\', c_h\' = Mh00/TT00 in [chp_lo, chp_hi]',
     'DRY_INPUTS = %s' % ('; '.join(dry_parts) or 'none'),
     'SOURCE = pk23 m3_lawcert_cw_v1 9087afc2, m3_lawcert_hl_v1_1 8d5fe3c7, reader m3_reader_cw_v1_1 %s; pk03 m3_lawcert_v1_1, v1_2; '
     'pk22 m3_lawcert_c3k_v1, m3_lawcert_c3k_v2 %s (c3kp records), psixy_exact_d_v1, v2 (MANIFEST_PSIXY_10P_v1); pk25 MR_LEMMAP v3 3164b778, '
     'P2 %s %s; MR_INSERT v4b 54691bc1, MR_SPECTRAL v4 0e4d8177 and pk22 MR_JOINT 80bc8d81 for the DRY |Q f|/t only' % (
         sha(RDRF)[:8], sha(C3K2F)[:8], os.path.relpath(P2F, W18), sha(P2F)[:8]),
     'J_UNIFORMITY = PER-PIECE: every row holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf (t = 0)',
     'LEMMAP_SHA256 = %s' % sha(MRL3), 'TRIAL_SET = %s' % kv_table(MRL3, 4)[0]['TRIAL_SET'],
     'TRIAL_SET_10P = N4 %s, N3 %s (the trial file of psi_xy\' per N, as psixy_exact_d names it: state 10\' when the run\'s STATE is 10p; '
     'C-10P)' % (TS_LINE[4], TS_LINE[3]),
     'DEFINITIONS = x1t_hi >= |Q_xy S M_c\' x_1| / t at every J of the piece (t = 1/J, the last piece to t = 0); x_1 = psi_1/|psi_1| (state 1 of '
     'TRIAL_SET); Q_xy = I - |psi_xy\'><psi_xy\'| / |psi_xy\'|^2 with psi_xy\' the state 10\' of TRIAL_SET_10P (pk22\'s exact c\'(t), '
     'psixy_exact_d_v2); M_c\' = M_h - c_h\' with c_h\' = Mh00/TT00 = <S psi_0, M_h S psi_0> / <S psi_0, S psi_0> (pk23\'s Pev laws); '
     'chp_lo <= c_h\' <= chp_hi on the piece; ran Q_ext lies in ran Q_xy, so x1t_hi t >= |Q_ext S M_c\' x_1| too',
     'FIELDS = jlo jhi x1t_hi chp_lo chp_hi']
for N in (4, 3):
    for key, jlo, jhi, x1t, a, b, tlo, thi in REC_ROWS[N]:
        L.append('%s = %s %s %r %r %r' % (key, tlo, thi, x1t, a, b))
text = '\n'.join(L) + '\n'
with open(OUT, 'x') as fh:
    fh.write(text)
for s in SUMMARY:
    out('SUMMARY N=%d STATE %s: x1t_hi %.4f at J_s, at most %.4f from J_s, %.4f on the last piece; DRY |Q f|/t worst %.4f at jlo %.1f, %.4f on the '
        'last piece' % s)
out('RECORD %s %s' % (os.path.basename(OUT), hashlib.sha256(text.encode()).hexdigest()))
out('VERDICT %s' % ('VALID' if verdict == 'VALID' else 'INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % x for x in NOFIRE])))
out('STATUS %s (DRY inputs: %s)' % (status, '; '.join(dry_parts) or 'none'))
