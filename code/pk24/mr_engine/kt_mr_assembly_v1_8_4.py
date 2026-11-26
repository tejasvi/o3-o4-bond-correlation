#!/usr/bin/env python3
"""kt_mr_assembly_v1_8_4.py (pk24): the M1 assembly engine of the MIDROW programme, made by tools/make_mrengine_v1_8_4.py from
mr_engine/src/kt_mr_assembly_v1_8_4.py.in (the maker fills the sha256 pins). Specification: pk24/MIDROW_G6_SPEC_v1_6_1.md (sect. 5b: the tail section), the M2 plan pk24/MIDROW_M2_PLAN_v1_1.md (sect. 3) and the
engine notes.
Changes from v1_8_3 (the tail-check request): per N, a line C-TAILMONO OK naming the conditions the stop checked on every piece, and
a line TAIL SUP with the least and largest sup over d >= D0 of e-hat(d) over the pieces (rows D0..D_MAX, then the envelope at
max(D0, D_MAX + 1)) and where it enters h's envelope; rows, tail rows and verdicts are v1_8_3's.
v1_8_3's changes from v1_8_2 (job192's floor test): on a piece whose bulk h row has a Way B floor, the tail's h envelope takes the coefficient
[-1, 1], as alpha_h does for the crude ends there, so C-TAILMONO passes and the sign condition (c) fails on that piece; nothing else.
v1_8_2's changes from v1_8_1:
- MR_INPUT_KV_v4's final fields: MR_INSERT = v3 + xc_lo xc_hi xf_hi, MR_EXACT = v3 + Axc_lo Axc_hi Axf_hi; the floors xf_hi, Axf_hi (Way B,
  row 4325) are >= 0 and nonzero only on the last piece and only for h (MR_INSERT h; MR_EXACT h-1, h0), else G-FLOOR stops. MR_EXACT (v3 or
  v4) may end with Pe_hi, the exact end's unwindowed flip-even |P_e a| (route (v), row 4376);
- G-PIN requires X_DEFINITION on v4 MR_INSERT and MR_EXACT, exactly XDEF below: the coefficient interval and the floor enclose the x
  amplitude at every J of the piece (with a zero floor, xc_lo <= v_x / t^p <= xc_hi), and an ORIENT_CHECK line on MR_SPECTRAL, MR_INSERT and
  MR_EXACT matching ORIENT_RX, whose piece counts must equal the record grid's (the producer's numeric orientation check, rows 4335, 4340);
- C-ORIENT adds c_y(-1) > 0 on every MR_SPECTRAL row (the y anchor) and ties MR_INSERT to the convention: t and a v_x > 0, h, t and a v_y > 0
  on every row (the v1_7_1 N-1);
- G-FACTX with floors: t xc -+ floor inside the amplitude at both ends of each piece (power 1), floor 0 and xc = vx (power 0);
- factored mode: a row with a nonzero floor has no certified coefficient sign (alpha_h gives [-1, 1]), so X falls back to v1_6's form there,
  and the tail's sign condition (c) fails on that piece; the run prints how many class-piece evaluations fell back review;
- route (v): an exact end with Pe_hi has |P_e a| = Pe_hi, so the m = 1 rest takes the least of |P_e a_L| N'_R and N'_L |P_e a_R| over the
  ends that give |P_e a|; the output's ROUTE_V line says whether MR_EXACT carries Pe_hi;
- plants YORIENT (c_y(-1) flipped on one row), IORIENT (t's v_x flipped on one row), OCHK (MR_INSERT's ORIENT_CHECK dropped), XDEF (MR_INSERT's
  X_DEFINITION replaced by an upper-bound text) and FLOOR (a floor off the last piece), each a stop.
v1_8_1's changes from v1_8: the list of the COUNT line is named cnt (v1_8 reused the name tail, so a run without TAIL wrote an empty
OUT.tail); nothing else.
v1_8's changes from v1_7_1 (G6 v1_6_1 sect. 5b, Theorem M2; the row 4274 item 2, the float design of D0, M0 and n0):
- the TAIL option D0:M0 (factored mode only; NMAX >= n0 = 2 D0 + M0 + 1, else G-TAIL stops) runs the tail section on every piece: the crude
  end envelopes at D0 (end(X, D0, env=True): the leading terms two-sided by their moduli; h's coefficient xc + [-s, s] and x amplitude
  v_x + t_hi [-s, s] with s = sup over d >= D0 of e-hat(d), the rows from D0 to D_MAX and the envelope at max(D0, D_MAX + 1)); the envelope
  classes, (h end, partner end) in {-1, ..., D0 - 1, D0+}^2 with at least one D0+, for m = 1..M0 - 1 (2..M0 - 1 for an h partner), by the
  finite check's margin code; Lemma T(b)'s m-tail at M0 for each type pair (h, T); the sign condition (c); Proposition J's envelope orbits
  L_J(D0, d_R), d_R = 0..D0. One row per piece in the tail record OUT.tail (MR_TAIL_KV_v1). TAIL_VERDICT is PASS iff every envelope class
  and envelope orbit passes, every m-tail lower end is > 0 and (c) holds, on every piece; with TAIL, RUN_VERDICT also needs it. D0:M0:D is a
  design run: no NMAX condition, and the tail does not enter RUN_VERDICT (TAIL_VERDICT DESIGN-PASS or DESIGN-FAIL);
- C-TAILMONO (a stop): s_x, s_y, tau, rho_1 and env_r below 1 on the piece, and the envelope at D0 encloses the end at d = D0..D0 + 12,
  D_MAX and D_MAX + 1 (A_y, A_x, N', |P_e a|, |S a|, e; for h also its coefficient and e);
- the class margin is the helper margin(ty, EL, ER, m) on end tuples (end_tuple), and Proposition J per piece is sb_piece(); the finite
  check's rows are v1_7_1's;
- plants TAILQ (N'* times 1e6 in the m-tail; fires on TAIL-MTAIL), TAILSIGN (the t envelope's coefficient flipped on the first piece; fires
  on TAIL-SIGN) and TAILENV (the envelope taken at D0 + 1; stops at C-TAILMONO); a stop in the run's second part reports a plant as FIRED
  when it is that plant's own stop;
- PIECES = all (or none) selects every piece, so that TAIL can follow.
v1_7_1's changes from v1_7 (the row 4310; the v1_7 quote note):
- G-PIN requires a TRIAL_SET line on every record in CERTIFIED mode, and one TRIAL_SET value across the five records whenever any record
  carries one (pk25's form: "N4 ts_N4_...json:<sha256>, N3 ts_N3_...json:<sha256>");
- C-ORIENT (a stop): c_x(-1) > 0 on every MR_SPECTRAL row (row 4089: u_x along e1), and every exact end's x amplitude (MR_EXACT h-1, h0,
  t-1, a0; Axc in v4) has the sign of the bulk x amplitude of the same insertion in MR_INSERT (xc in v4) wherever both are strict; this
  stops a set whose producers orient u_x differently;
- plants ORIENT (c_x(-1)'s sign flipped on one row) and XORIENT (one t-1 row's x amplitude flipped) stop at C-ORIENT;
- wording: xc and Axc are intervals that enclose the x coefficient over the piece (xc_lo <= h_x / t <= xc_hi for every t of the piece).
v1_7's changes from v1_6 (the rows 4266, 4273, 4274; M2 plan v1_1 sect. 3; the engine v1_6 delta N1):
- MR_INPUT_KV_v4 is read beside v3 (one FORMAT for the five records). MR_INSERT adds xc_lo xc_hi with X_POWER = "h 1, t 0, a 0" (an interval
  enclosing the x coefficient over the piece: h_x / t for h, v_x itself for t and a); MR_EXACT adds Axc_lo Axc_hi with X_POWER = "h-1 1, h0 1, t-1 0, a0 0"; a factored
  MR_CRUDEX has FIELDS jlo jhi ehat_hi env_delta0_hi env_r_hi, E_DEFINITION "ehat_hi >= |a_x(h, d) - v_x| / t at every J of the piece" and
  D_MAX, with the items _h1.._hD_MAX, and the envelope e-hat(d) <= env_delta0 env_r^(d+1) covers d > D_MAX; a split MR_CRUDEX keeps v3's
  fields and lines;
- the factored-x mode, only with a factored v4 MR_CRUDEX: a crude h end's coefficient is xc + [-e-hat(d), e-hat(d)], an exact h end's is
  Axc, and a t or a end's is its x interval; X = 0 when the product of the two coefficient intervals is certified >= 0, else v1_6's X. The
  unfactored e(d) is t_hi e-hat(d) at every d >= 1 (rows, then the envelope); the plain bound is not used in this mode (the v1_7 N-1). With v3 records or a split
  MR_CRUDEX every row is v1_6's;
- G-FACTX (a stop): t xc inside [vx_lo, vx_hi] at both ends of each piece for h (relative rounding slack 1e-14), xc = vx for t and a, the
  same for Axc against Ax, 0 < env_r < 1 on every row, one envelope per piece; C-SIGN (a flag that makes the run INVALID): e-hat(d) below
  the modulus of h's coefficient for every d <= D_MAX and at D_MAX + 1 through the envelope, which then covers every larger d;
- the frozen core mr_core_v1_3, with EXPECT to n = 30 from tools/count_todo_bf_v1.py's independent count, and prototype g6_engine_proto_v1_2;
- the plants XSIGN (h's coefficient sign opened on the first piece; fires on the margin), ENVR (env_r set to 1; stops at G-FACTX), FACTX
  (xc_hi of the first h row doubled; stops at G-FACTX) and CSTAT (owner PRODUCER lines in memory with the CERTIFIED status rule; stops at
  that rule, the engine v1_6 N1).
v1_6's changes from v1_5 (the engine v1_5 delta F1, N1, N2; the field check N4; G6 v1_5 sect. 0d item 4; the row 4206):
- G-PIN checks each record's PRODUCER: in CERTIFIED mode its first word must be the record's owner (G6 sect. 6: pk25 for MR_SPECTRAL,
  MR_INSERT and MR_CRUDEX; pk22 for MR_EXACT and MR_JOINT); in STANDIN mode the owner or pk24 (the stand-in writer). Plant PROD
  applies the owner rule to stand-in records and must stop at G-PIN; plant PRODOK puts owner PRODUCER lines in memory after the pin check
  and must pass the owner rule on all five records (a positive control);
- a non-stop plant fires only on its own failure (F1): OPN at G-POS, DELTA at G-DELTA, TAU2, SIGN and T2 on the margin alone. Each class
  keeps every reason it meets on any piece; the run prints the counts by reason, and the plant line repeats them;
- the G-FLOAT reference is the v1_5 realistic run with pk25's L3 table (mr_engine/v17/kt_mr_v1_5_NOF1_L3.out).
v1_5's changes from v1_3 (the rows 4153, 4170; v1_4 was withdrawn before any result, see the maker
tools/make_mrtemplates_v1_5.py):
- the frozen core mr_core_v1_2 (exact negation and modulus); the engine's own negations and moduli use copy_negate() and copy_abs(); C-IV
  also checks negation, amax, hull, pow and division with 50-digit endpoints (M1);
- kv_read stops on a repeated row key and on a line without "=" (M2, N5); G-UNIF requires every single upper bound (a *_hi field without a
  *_lo partner) to be >= 0 (M3); every output carries a PLANT line, and the merge accepts only PLANT = none (M4);
- plants for G-DELTA (DELTA), for the new G-UNIF checks (UNIF) and for repeated keys (DUPKEY) (N2); ENDS is cleared at start (N3); CODE and
  INPUT_PINS carry full sha256 (N6);
- MR_CRUDEX's header must state E_DEFINITION = "e_hi >= |a_x(h, d) - v_x| at every J of the piece" and CRUDEX_FORM = factored or split
  (pk25's ADD1_3);
- the Q1 rule: RUN_VERDICT VALID (STANDIN-VALID on stand-ins) iff every class's certified margin has a positive lower end on every piece
  and the gates pass (G-PIN, G-UNIF, G-COUNT, G-CORNER, G-POS, G-DELTA); G-FLOAT is INFO only (reference: the v1_5 realistic run); every row
  with float headroom H < 2 is printed as a WARN line (design target, not a rule).
Kept from v1_3: the optional exact vertical end at d' = 0 (MR_EXACT rows _a0, every piece or none). Kept from v1_2: MR_INPUT_KV_v3; the N-1
norms of M_c; the windowed T2; the m = 1 rest as the smaller of two forms; e(d) from MR_CRUDEX (d <= 3) or the plain bound (d >= 4);
Proposition J with PewJw <= tau Wc; the PIECES option (merged by mr_merge_v1_8_4.py); the ORIENTATION line.
For N in {3, 4}, every piece of the records' grid (or of the PIECES range) and every to-do class of P_3 x P_n (6 <= n <= NMAX), it evaluates
- Proposition MR on each channel class (m >= 1): margin = Y_lo - X - R - T2, X = max(0, -x_lo) of s_x^m a_x b_x (a crude h end enters as
  a_x = v_x + [-e(d), e(d)]); for an h-h pair the smaller of that and Lemma 4's s_x^m (e_L + e_R)^2 / 4; T2 = s_x^(2m-2) |S a| |S b+| e(d) e(d')
  / (1 - delta) with |S a| <= (s_x^2 A_x^2 + s_y^2 A_y^2 + N'^2)^1/2; a row PASSES on a piece iff margin_lo > 0, and L = margin_lo / (1 + delta_hi);
- Proposition J on each interior same-bond orbit in the exact form; L = L_J / (1 + delta)^2;
and writes one MR_ASSEMBLY_KV_v1 row per class (the least L over the pieces, its piece, the verdict, and the least float headroom).
Usage: kt_mr_assembly_v1_8_4.py RECDIR PINS_SHA256 MODE OUT [PLANT] [NMAX] [PIECES] [TAIL]
  MODE STANDIN or CERTIFIED; PLANT in {none, OPN, TAU2, SIGN, T2, DELTA, PIN, COUNT, UNIF, DUPKEY, PROD, PRODOK, XSIGN, ENVR, FACTX, CSTAT,
  ORIENT, XORIENT, TAILQ, TAILSIGN, TAILENV, YORIENT, IORIENT, OCHK, XDEF, FLOOR}; NMAX defaults to 14 (plants use 10) and may go up to 30;
  PIECES = a:b restricts the pieces to grid indices a <= index < b (both N) and writes a part record (RECORD MR_ASSEMBLY_PART) for the merge;
  all or none selects every piece;
  TAIL = D0:M0 (or D0:M0:D, a design run) runs the tail section and writes OUT.tail.
Gates: C-CORE, C-IV, G-PIN, G-UNIF, G-FACTX, G-COUNT (stops); G-CORNER and C-SIGN (flags that make the run INVALID); G-POS, G-DELTA
(row FAIL); G-FLOAT (INFO).
Interval arithmetic: mr_core_v1_3.Iv (decimal endpoints, prec 50, directed rounding, the directed square root, exact negation and modulus).
Inputs are decimal strings."""
import hashlib, importlib.util, inspect, os, random, re, sys
from fractions import Fraction
from decimal import Decimal as Dm

W = '/mnt/g2/release/root/code/'
CORE = (W + 'pk24/mr_engine/mr_core_v1_3.py', '7fe1e2d077fe468343e5a7956553ed364266cf7fea3a0243fda5300b68323263')
PROTO = (W + 'pk24/midrow/g6_engine_proto_v1_2.py', 'eac5eb42dda72e5ab13879ab8d767cd13a07c053add3df1eee55b19fea3b648d')
FREF = (W + 'pk24/mr_engine/v17/kt_mr_v1_5_NOF1_L3.out', '1893558d231dcc3db1a35a73d503f05e4dc4651a28e5ecc609de22f3d59881f7')
BLOCKS = ('span', 'image', 'canon', 'position', 'edges', 'todo', 'corner_twin')
RECS = ('MR_SPECTRAL', 'MR_INSERT', 'MR_EXACT', 'MR_CRUDEX', 'MR_JOINT')
JLOW = {4: Dm(350), 3: Dm(300)}
ENDS = {}
FIELDS = {'MR_SPECTRAL': 'jlo jhi sx_lo sx_hi sy_lo sy_hi tau_hi rho1_hi Rw_hi cxm1_lo cxm1_hi cym1_lo cym1_hi',
          'MR_INSERT': ('jlo jhi vx_lo vx_hi vy_lo vy_hi Pevw_hi Pev_hi vp_hi mxx_lo mxx_hi mxy_lo mxy_hi myy_lo myy_hi PeBwux_hi PeBwuy_hi win_hi '
                        'C_hi windowed'),
          'MR_EXACT': 'jlo jhi Ay_lo Ay_hi Ax_lo Ax_hi Np_hi Ay_mid',
          'MR_CRUDEX': 'jlo jhi e_hi',
          'MR_JOINT': 'jlo jhi Cb_lo Cb_hi Cb_mid wJwx_hi wJwy_hi PewJw_hi jfw_hi A0_hi ch_lo ch_hi ct_lo ct_hi bh_hi bt_hi Wc_hi'}
ORIENT = 'u_x along e1, u_y along e3'
E_DEF = 'e_hi >= |a_x(h, d) - v_x| at every J of the piece'
E_DEF_FACT = 'ehat_hi >= |a_x(h, d) - v_x| / t at every J of the piece'
FIELDS4 = dict(FIELDS, MR_INSERT=FIELDS['MR_INSERT'] + ' xc_lo xc_hi xf_hi', MR_EXACT=FIELDS['MR_EXACT'] + ' Axc_lo Axc_hi Axf_hi')
F_CRX_FACT = 'jlo jhi ehat_hi env_delta0_hi env_r_hi'
XPOW = {'MR_INSERT': 'h 1, t 0, a 0', 'MR_EXACT': 'h-1 1, h0 1, t-1 0, a0 0'}
XSLACK = Dm('1e-14')
XDEF = {'MR_INSERT': 'xc_lo t^p - xf_hi <= v_x <= xc_hi t^p + xf_hi at every J of the piece, p from X_POWER',
        'MR_EXACT': 'Axc_lo t^p - Axf_hi <= A_x <= Axc_hi t^p + Axf_hi at every J of the piece, p from X_POWER'}
ORIENT_RECS = ('MR_SPECTRAL', 'MR_INSERT', 'MR_EXACT')
ORIENT_RX = (r'^C-ORIENT PASS on every piece \(N4 (\d+), N3 (\d+)\): u~_x has a positive coefficient on the canonical e1 and u~_y on '
             r'the canonical e3; plant PLANT-ORIENT fired$')
PLANTS = ('OPN', 'TAU2', 'SIGN', 'T2', 'DELTA', 'PIN', 'COUNT', 'UNIF', 'DUPKEY', 'PROD', 'PRODOK', 'XSIGN', 'ENVR', 'FACTX', 'CSTAT',
          'ORIENT', 'XORIENT', 'TAILQ', 'TAILSIGN', 'TAILENV', 'YORIENT', 'IORIENT', 'OCHK', 'XDEF', 'FLOOR')
STOP_PLANTS = ('PIN', 'COUNT', 'UNIF', 'DUPKEY', 'PROD', 'ENVR', 'FACTX', 'CSTAT', 'ORIENT', 'XORIENT', 'TAILENV', 'YORIENT', 'IORIENT', 'OCHK',
               'XDEF', 'FLOOR')
TAIL_PLANTS = ('TAILQ', 'TAILSIGN', 'TAILENV')
STOP_GATE = {'PIN': 'G-PIN: MR_INSERT.kv sha256', 'UNIF': 'G-UNIF: MR_INSERT row', 'DUPKEY': 'G-PIN: MR_INSERT.kv repeats the row key',
             'PROD': 'G-PIN: MR_SPECTRAL PRODUCER pk24 is not its owner pk25', 'ENVR': 'G-FACTX: MR_CRUDEX ENV_R_HI',
             'FACTX': 'G-FACTX: MR_INSERT row', 'CSTAT': 'G-PIN: MR_SPECTRAL is not a VALID certified export',
             'ORIENT': 'C-ORIENT: MR_SPECTRAL row', 'XORIENT': 'C-ORIENT: MR_EXACT row', 'TAILENV': 'C-TAILMONO',
             'YORIENT': 'C-ORIENT: MR_SPECTRAL c_y(-1)', 'IORIENT': 'C-ORIENT: MR_INSERT row', 'OCHK': 'G-PIN: MR_INSERT has no valid ORIENT_CHECK line',
             'XDEF': 'G-PIN: MR_INSERT must state X_DEFINITION', 'FLOOR': 'G-FLOOR: MR_INSERT row'}
OWN_FAIL = {'OPN': 'G-POS', 'TAU2': 'MARGIN', 'SIGN': 'MARGIN', 'T2': 'MARGIN', 'DELTA': 'G-DELTA', 'XSIGN': 'MARGIN', 'TAILQ': 'TAIL-MTAIL',
            'TAILSIGN': 'TAIL-SIGN'}
FX = {}
FMT = set()
TSET = set()
TAILOUT = {}
OCHK = {}
PEX = set()
NFB = [0]


def sgn_iv(lo, hi):
    """+1 or -1 for an interval of one strict sign, 0 for one that meets 0"""
    return 1 if Dm(lo) > 0 else (-1 if Dm(hi) < 0 else 0)
OWNER = {'MR_SPECTRAL': 'pk25', 'MR_INSERT': 'pk25', 'MR_CRUDEX': 'pk25', 'MR_EXACT': 'pk22', 'MR_JOINT': 'pk22'}
OWNER_OK = []


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(p):
    return sha_bytes(open(p, 'rb').read())


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Stop(Exception):
    pass


def neg(x):
    return x.copy_negate()


def c_core():
    if sha(CORE[0]) != CORE[1]:
        raise Stop('C-CORE: mr_core_v1_3.py sha256 %s, pinned %s' % (sha(CORE[0])[:8], CORE[1][:8]))
    if sha(PROTO[0]) != PROTO[1]:
        raise Stop('C-CORE: prototype sha256 %s, pinned %s' % (sha(PROTO[0])[:8], PROTO[1][:8]))
    core = load_module(CORE[0], 'mr_core_v1_3')
    proto = load_module(PROTO[0], 'g6proto_ref')
    for b in BLOCKS:
        if inspect.getsource(getattr(core, b)) != inspect.getsource(getattr(proto, b)):
            raise Stop('C-CORE: block %s differs from the prototype' % b)
    for b in ('RX', 'ROW', 'EXPECT'):
        if (getattr(core, b).pattern if b == 'RX' else getattr(core, b)) != (getattr(proto, b).pattern if b == 'RX' else getattr(proto, b)):
            raise Stop('C-CORE: constant %s differs from the prototype' % b)
    print('C-CORE OK: mr_core_v1_3 %s; %d blocks and 3 constants equal to the prototype %s' % (CORE[1], len(BLOCKS), PROTO[1]))
    return core


def d50(rng, lo_exp=-1):
    """a decimal with 50 significant digits, |x| in [10^lo_exp, 10^(lo_exp + 1)), read exactly from its string"""
    dg = '%d' % rng.randrange(10 ** 49, 10 ** 50)
    s = ('-' if rng.random() < 0.5 else '') + dg[0] + '.' + dg[1:] + 'E%d' % lo_exp
    return Dm(s)


def c_iv(core):
    """every interval operation the engine uses, against exact rationals: add, sub, mul, inv, sqrt (15-digit endpoints), and negation,
    amax, hull, pow, division (50-digit endpoints)"""
    rng = random.Random(20261121)
    bad, nops = 0, 0
    for k in range(300):
        a = [Dm('%.15e' % rng.uniform(-3, 3)) for _ in range(4)]
        x, y = core.Iv(min(a[0], a[1]), max(a[0], a[1])), core.Iv(min(a[2], a[3]), max(a[2], a[3]))
        X = (Fraction(x.lo), Fraction(x.hi))
        Y = (Fraction(y.lo), Fraction(y.hi))
        for op, r in (('add', x + y), ('sub', x - y), ('mul', x * y)):
            cands = [p + q for p in X for q in Y] if op == 'add' else ([p - q for p in X for q in Y] if op == 'sub' else [p * q for p in X for q in Y])
            nops += 1
            if not (Fraction(r.lo) <= min(cands) and max(cands) <= Fraction(r.hi)):
                bad += 1
        z = core.Iv(a[0].copy_abs() + Dm('0.1'), a[0].copy_abs() + Dm('0.1') + a[1].copy_abs())
        inv = z.inv()
        nops += 2
        if not (Fraction(inv.lo) <= 1 / Fraction(z.hi) and 1 / Fraction(z.lo) <= Fraction(inv.hi)):
            bad += 1
        s = z.sqrt()
        if not (Fraction(s.lo) ** 2 <= Fraction(z.lo) and Fraction(z.hi) <= Fraction(s.hi) ** 2):
            bad += 1
    for k in range(300):
        b = sorted([d50(rng, rng.randint(-8, 1)) for _ in range(2)])
        c = sorted([d50(rng, rng.randint(-8, 1)) for _ in range(2)])
        x, y = core.Iv(b[0], b[1]), core.Iv(c[0], c[1])
        X = (Fraction(x.lo), Fraction(x.hi))
        ng = -x
        nops += 5
        if not (Fraction(ng.lo) == -X[1] and Fraction(ng.hi) == -X[0]):
            bad += 1
        if Fraction(x.amax()) != max(abs(X[0]), abs(X[1])):
            bad += 1
        hl = x.hull(y)
        if not (Fraction(hl.lo) == min(X[0], Fraction(y.lo)) and Fraction(hl.hi) == max(X[1], Fraction(y.hi))):
            bad += 1
        kk = rng.randint(0, 5)
        pw = x ** kk
        cands = [p ** kk for p in X] + ([Fraction(0)] if (kk > 0 and X[0] < 0 < X[1]) else [])
        if not (Fraction(pw.lo) <= min(cands) and max(cands) <= Fraction(pw.hi)):
            bad += 1
        yp = core.Iv(c[0].copy_abs() + Dm('1E-9'), c[0].copy_abs() + Dm('1E-9') + c[1].copy_abs())
        dv = x / yp
        cands = [p / q for p in X for q in (Fraction(yp.lo), Fraction(yp.hi))]
        if not (Fraction(dv.lo) <= min(cands) and max(cands) <= Fraction(dv.hi)):
            bad += 1
    if bad:
        raise Stop('C-IV: %d of %d enclosures fail' % (bad, nops))
    print('C-IV OK: %d operations (add, sub, mul, inv, sqrt; negation, amax, hull, pow, division with 50-digit endpoints) enclose or equal the '
          'exact rational results' % nops)


def kv_read(path, raw=None):
    raw = open(path, 'rb').read() if raw is None else raw
    fields, rows, head = None, {}, {}
    for ln in raw.decode().splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        if '=' not in ln:
            raise Stop('G-PIN: %s has a line without "=": %s' % (os.path.basename(path), ln[:60]))
        k, v = [x.strip() for x in ln.split('=', 1)]
        if k == 'FIELDS':
            fields = v.split()
        elif fields is None:
            if k in head:
                raise Stop('G-PIN: %s repeats the header key %s' % (os.path.basename(path), k))
            head[k] = v
        else:
            vals = v.split()
            if len(vals) != len(fields):
                raise Stop('G-PIN: %s row %s has %d values for %d fields' % (os.path.basename(path), k, len(vals), len(fields)))
            if k in rows:
                raise Stop('G-PIN: %s repeats the row key %s' % (os.path.basename(path), k))
            rows[k] = dict(zip(fields, vals))
    return head, fields, rows


def g_pin(recdir, pins_sha, mode, plant):
    pp = os.path.join(recdir, 'PINS.txt')
    if sha(pp) != pins_sha:
        raise Stop('G-PIN: PINS.txt sha256 %s, expected %s' % (sha(pp)[:8], pins_sha[:8]))
    pins = dict((l.split()[1], l.split()[0]) for l in open(pp).read().splitlines() if l.strip())
    recs, heads = {}, {}
    for r in RECS:
        raw = open(os.path.join(recdir, r + '.kv'), 'rb').read()
        if plant == 'PIN' and r == 'MR_INSERT':
            raw = raw.replace(b'0', b'1', 1)
        h = sha_bytes(raw)
        if h != pins.get(r + '.kv'):
            raise Stop('G-PIN: %s.kv sha256 %s against PINS %s' % (r, h[:8], str(pins.get(r + '.kv'))[:8]))
        if plant == 'DUPKEY' and r == 'MR_INSERT':
            last = [l for l in raw.decode().splitlines() if l.strip() and not l.startswith('#')][-1]
            raw = raw + (last + '\n').encode()
        head, fields, rows = kv_read(os.path.join(recdir, r + '.kv'), raw)
        if plant == 'OCHK' and r == 'MR_INSERT':
            head.pop('ORIENT_CHECK', None)
        if plant == 'XDEF' and r == 'MR_INSERT':
            head['X_DEFINITION'] = 'v_x <= xc_hi t^p at every J of the piece'
        fmt = head.get('FORMAT')
        if fmt not in ('MR_INPUT_KV_v3', 'MR_INPUT_KV_v4') or head.get('RECORD') != r:
            raise Stop('G-PIN: %s header not MR_INPUT_KV_v3 or MR_INPUT_KV_v4' % r)
        FMT.add(fmt)
        if len(FMT) > 1:
            raise Stop('G-PIN: the records mix MR_INPUT_KV_v3 and MR_INPUT_KV_v4')
        want = (FIELDS if fmt == 'MR_INPUT_KV_v3' else FIELDS4)[r]
        if r == 'MR_CRUDEX' and fmt == 'MR_INPUT_KV_v4' and head.get('CRUDEX_FORM') == 'factored':
            want = F_CRX_FACT
        if fields != want.split() and not (r == 'MR_EXACT' and fields == want.split() + ['Pe_hi']):
            raise Stop('G-PIN: %s FIELDS are not those of %s' % (r, fmt))
        if r == 'MR_EXACT' and fields[-1] == 'Pe_hi':
            PEX.add(r)
        if fmt == 'MR_INPUT_KV_v4' and r in XPOW and head.get('X_POWER') != XPOW[r]:
            raise Stop('G-PIN: %s X_POWER is not "%s"' % (r, XPOW[r]))
        if fmt == 'MR_INPUT_KV_v4' and r in XDEF and head.get('X_DEFINITION') != XDEF[r]:
            raise Stop('G-PIN: %s must state X_DEFINITION = "%s"' % (r, XDEF[r]))
        if r in ORIENT_RECS:
            mo_ = re.match(ORIENT_RX, head.get('ORIENT_CHECK', ''))
            if not mo_:
                raise Stop('G-PIN: %s has no valid ORIENT_CHECK line (the rows 4335, 4340): "%s"' % (r, head.get('ORIENT_CHECK', '')[:90]))
            OCHK[r] = (int(mo_.group(1)), int(mo_.group(2)))
        if head.get('ORIENTATION') != ORIENT:
            raise Stop('G-PIN: %s ORIENTATION is not "%s"' % (r, ORIENT))
        ts_ = head.get('TRIAL_SET', '').strip()
        if mode == 'CERTIFIED' and not ts_:
            raise Stop('G-PIN: %s has no TRIAL_SET line (the row 4310)' % r)
        if ts_:
            TSET.add(ts_)
            if len(TSET) > 1:
                raise Stop('G-PIN: the records name different TRIAL_SET lines')
        prod = head.get('PRODUCER', '').split()
        if plant in ('PRODOK', 'CSTAT'):
            prod = [OWNER[r], 'plant', plant]
        owner_rule = mode == 'CERTIFIED' or plant in ('PROD', 'PRODOK', 'CSTAT')
        if not prod or prod[0] not in ((OWNER[r],) if owner_rule else (OWNER[r], 'pk24')):
            raise Stop('G-PIN: %s PRODUCER %s is not its owner %s%s' % (r, prod[0] if prod else '(none)', OWNER[r],
                                                                       '' if owner_rule else ' or pk24'))
        if owner_rule:
            OWNER_OK.append(r)
        if r == 'MR_CRUDEX':
            fact4 = fmt == 'MR_INPUT_KV_v4' and head.get('CRUDEX_FORM') == 'factored'
            if head.get('E_DEFINITION') != (E_DEF_FACT if fact4 else E_DEF) or head.get('CRUDEX_FORM') not in ('factored', 'split'):
                raise Stop('G-PIN: MR_CRUDEX must state E_DEFINITION = "%s" and CRUDEX_FORM = factored or split' % (E_DEF_FACT if fact4 else E_DEF))
            if fact4 and not re.match(r'^[1-9][0-9]*$', head.get('D_MAX', '')):
                raise Stop('G-PIN: a factored MR_INPUT_KV_v4 MR_CRUDEX must state D_MAX, a positive integer')
        if (mode == 'CERTIFIED' or plant == 'CSTAT') and not (head.get('EXPORT_STATUS') == 'CERTIFIED' and head.get('RUN_VERDICT') == 'VALID'):
            raise Stop('G-PIN: %s is not a VALID certified export' % r)
        if mode == 'STANDIN' and head.get('STATUS') != 'FLOAT-STANDIN':
            raise Stop('G-PIN: %s is not a stand-in record' % r)
        recs[r], heads[r] = rows, head
        print('G-PIN %s.kv %s OK (PRODUCER %s%s)%s' % (r, h, prod[0], ', owner rule' if owner_rule else '',
                                                       ' (CRUDEX_FORM %s)' % head['CRUDEX_FORM'] if r == 'MR_CRUDEX' else ''))
    return recs, heads, pins


def g_unif(recs, heads, plant):
    grid = {}
    if plant == 'UNIF':
        k0 = sorted(recs['MR_INSERT'])[0]
        recs['MR_INSERT'][k0] = dict(recs['MR_INSERT'][k0], Pev_hi='-' + recs['MR_INSERT'][k0]['Pev_hi'])
    if plant == 'FACTX':
        kh = sorted(k for k in recs['MR_INSERT'] if k.endswith('_h'))[0]
        recs['MR_INSERT'][kh] = dict(recs['MR_INSERT'][kh], xc_hi=str(Dm(recs['MR_INSERT'][kh]['xc_hi']) * 2))
    if plant == 'ENVR':
        kc = sorted(recs['MR_CRUDEX'])[0]
        recs['MR_CRUDEX'][kc] = dict(recs['MR_CRUDEX'][kc], env_r_hi='1')
    if plant == 'ORIENT':
        ks = sorted(recs['MR_SPECTRAL'])[0]
        r0 = recs['MR_SPECTRAL'][ks]
        recs['MR_SPECTRAL'][ks] = dict(r0, cxm1_lo=str(Dm(r0['cxm1_hi']).copy_negate()), cxm1_hi=str(Dm(r0['cxm1_lo']).copy_negate()))
    if plant == 'XORIENT':
        ke = sorted(k for k in recs['MR_EXACT'] if k.endswith('_t-1'))[0]
        r0 = dict(recs['MR_EXACT'][ke])
        for f0, f1 in (('Ax_lo', 'Ax_hi'), ('Axc_lo', 'Axc_hi')):
            if f0 in r0:
                r0[f0], r0[f1] = str(Dm(r0[f1]).copy_negate()), str(Dm(r0[f0]).copy_negate())
        recs['MR_EXACT'][ke] = r0
    if plant == 'YORIENT':
        ks = sorted(recs['MR_SPECTRAL'])[0]
        r0 = recs['MR_SPECTRAL'][ks]
        recs['MR_SPECTRAL'][ks] = dict(r0, cym1_lo=str(Dm(r0['cym1_hi']).copy_negate()), cym1_hi=str(Dm(r0['cym1_lo']).copy_negate()))
    if plant == 'IORIENT':
        kt = sorted(k for k in recs['MR_INSERT'] if k.endswith('_t'))[0]
        r0 = dict(recs['MR_INSERT'][kt])
        for f0, f1 in (('vx_lo', 'vx_hi'), ('xc_lo', 'xc_hi')):
            if f0 in r0:
                r0[f0], r0[f1] = str(Dm(r0[f1]).copy_negate()), str(Dm(r0[f0]).copy_negate())
        recs['MR_INSERT'][kt] = r0
    if plant == 'FLOOR':
        kh = sorted(k for k in recs['MR_INSERT'] if k.endswith('_h'))[0]
        recs['MR_INSERT'][kh] = dict(recs['MR_INSERT'][kh], xf_hi='1e-6')
    for r in RECS:
        if not heads[r].get('J_UNIFORMITY'):
            raise Stop('G-UNIF: %s has no J_UNIFORMITY line' % r)
    for k, row in recs['MR_SPECTRAL'].items():
        mm = re.match(r'^N(\d)_P(\d+)$', k)
        if not mm:
            raise Stop('G-UNIF: MR_SPECTRAL key %s' % k)
        grid.setdefault(int(mm.group(1)), {})[int(mm.group(2))] = (row['jlo'], row['jhi'])
    for N in (4, 3):
        g = grid.get(N)
        if not g:
            raise Stop('G-UNIF: no grid for N = %d' % N)
        idx = sorted(g)
        for a, b in zip(idx, idx[1:]):
            if b != a + 1 or g[a][1] != g[b][0]:
                raise Stop('G-UNIF: N = %d grid not contiguous at pieces %d, %d' % (N, a, b))
        if not (Dm(g[idx[0]][0]) <= JLOW[N] < (Dm(g[idx[0]][1]) if g[idx[0]][1] != 'inf' else Dm('Infinity'))) or g[idx[-1]][1] != 'inf':
            raise Stop('G-UNIF: N = %d grid does not run from J_low to inf' % N)
    for r_ in ORIENT_RECS:
        if OCHK.get(r_) != (len(grid[4]), len(grid[3])):
            raise Stop('G-PIN: %s ORIENT_CHECK names N4 %s, N3 %s pieces against the record grid\'s %d, %d' % (
                r_, OCHK.get(r_, ('-', '-'))[0], OCHK.get(r_, ('-', '-'))[1], len(grid[4]), len(grid[3])))
    canon = {}
    for r in RECS:
        canon[r] = {}
        for k, row in recs[r].items():
            mm = re.match(r'^N(\d)_P(\d+)(_\S+)?$', k)
            if not mm or int(mm.group(1)) not in grid or grid[int(mm.group(1))].get(int(mm.group(2))) != (row['jlo'], row['jhi']):
                raise Stop('G-UNIF: %s row %s off the grid' % (r, k))
            ck = 'N%s_P%04d%s' % (mm.group(1), int(mm.group(2)), mm.group(3) or '')
            if ck in canon[r]:
                raise Stop('G-UNIF: %s has two rows for %s' % (r, ck))
            for f, v in row.items():
                if f in ('jlo', 'jhi', 'windowed'):
                    continue
                try:
                    ok = Dm(v).is_finite()
                except Exception:
                    ok = False
                if not ok:
                    raise Stop('G-UNIF: %s row %s field %s = %s is not a finite decimal' % (r, k, f, v))
            for f in row:
                if f.endswith('_lo') and Dm(row[f]) > Dm(row[f[:-3] + '_hi']):
                    raise Stop('G-UNIF: %s row %s has %s > %s_hi' % (r, k, f, f[:-3]))
                if f.endswith('_hi') and (f[:-3] + '_lo') not in row and Dm(row[f]) < 0:
                    raise Stop('G-UNIF: %s row %s has the upper bound %s = %s < 0' % (r, k, f, row[f]))
            if r == 'MR_SPECTRAL' and not (Dm(row['sx_lo']) > 0 and Dm(row['sy_lo']) > 0 and Dm(row['tau_hi']) > 0 and Dm(row['Rw_hi']) > 0
                                           and Dm(row['rho1_hi']) > 0):
                raise Stop('G-UNIF: MR_SPECTRAL row %s: sx_lo, sy_lo, tau_hi, Rw_hi, rho1_hi must be positive' % k)
            if r == 'MR_INSERT' and row['windowed'] not in ('0', '1'):
                raise Stop('G-UNIF: MR_INSERT row %s: windowed = %s' % (k, row['windowed']))
            canon[r][ck] = row
    fact4 = heads['MR_CRUDEX'].get('FORMAT') == 'MR_INPUT_KV_v4' and heads['MR_CRUDEX'].get('CRUDEX_FORM') == 'factored'
    dmax = int(heads['MR_CRUDEX']['D_MAX']) if fact4 else 3
    need = {'MR_INSERT': ('_h', '_t', '_a'), 'MR_EXACT': ('_h-1', '_h0', '_t-1'), 'MR_CRUDEX': tuple('_h%d' % d for d in range(1, dmax + 1)),
            'MR_JOINT': ('',)}
    for N in (4, 3):
        for P in grid[N]:
            for r, sfx in need.items():
                for s_ in sfx:
                    if 'N%d_P%04d%s' % (N, P, s_) not in canon[r]:
                        raise Stop('G-UNIF: %s has no row for N = %d piece %d item %s' % (r, N, P, s_ or '-'))
            if canon['MR_INSERT']['N%d_P%04d_a' % (N, P)]['windowed'] != '0' or any(
                    canon['MR_INSERT']['N%d_P%04d_%s' % (N, P, X)]['windowed'] != '1' for X in 'ht'):
                raise Stop('G-UNIF: N = %d piece %d: h and t must be windowed, a unwindowed' % (N, P))
    a0 = [k for k in canon['MR_EXACT'] if k.endswith('_a0')]
    if a0 and len(a0) != len(grid[4]) + len(grid[3]):
        raise Stop('G-UNIF: MR_EXACT has a0 rows for %d of %d pieces (all or none)' % (len(a0), len(grid[4]) + len(grid[3])))
    if heads['MR_INSERT'].get('FORMAT') == 'MR_INPUT_KV_v4':
        nchk, nfl = 0, 0
        for N in (4, 3):
            for P in sorted(grid[N]):
                base = 'N%d_P%04d' % (N, P)
                jlo, jhi = grid[N][P]
                ts = [Fraction(1) / Fraction(Dm(jlo))] + ([Fraction(0)] if jhi == 'inf' else [Fraction(1) / Fraction(Dm(jhi))])
                for r, it, f0, f1, g0, g1, pw in (('MR_INSERT', '_h', 'vx_lo', 'vx_hi', 'xc_lo', 'xc_hi', 1),
                                                  ('MR_INSERT', '_t', 'vx_lo', 'vx_hi', 'xc_lo', 'xc_hi', 0),
                                                  ('MR_INSERT', '_a', 'vx_lo', 'vx_hi', 'xc_lo', 'xc_hi', 0),
                                                  ('MR_EXACT', '_h-1', 'Ax_lo', 'Ax_hi', 'Axc_lo', 'Axc_hi', 1),
                                                  ('MR_EXACT', '_h0', 'Ax_lo', 'Ax_hi', 'Axc_lo', 'Axc_hi', 1),
                                                  ('MR_EXACT', '_t-1', 'Ax_lo', 'Ax_hi', 'Axc_lo', 'Axc_hi', 0),
                                                  ('MR_EXACT', '_a0', 'Ax_lo', 'Ax_hi', 'Axc_lo', 'Axc_hi', 0)):
                    row = canon[r].get(base + it)
                    if row is None:
                        continue
                    lo, hi, clo, chi = (Fraction(Dm(row[f])) for f in (f0, f1, g0, g1))
                    fn_ = 'xf_hi' if r == 'MR_INSERT' else 'Axf_hi'
                    ff = Fraction(Dm(row[fn_]))
                    nchk += 1
                    if ff > 0:
                        nfl += 1
                        if jhi != 'inf' or pw != 1:
                            raise Stop('G-FLOOR: %s row %s%s: the floor %s = %s is off the last piece or on a power-0 row (the row 4325: '
                                       'Way B only on the last piece, for h)' % (r, base, it, fn_, row[fn_]))
                    if pw == 0:
                        if clo != lo or chi != hi:
                            raise Stop('G-FACTX: %s row %s%s: with power 0 the coefficient must equal the amplitude' % (r, base, it))
                        continue
                    slack = Fraction(XSLACK) * max(abs(lo), abs(hi))
                    for t in ts:
                        if t * clo - ff < lo - slack or t * chi + ff > hi + slack:
                            raise Stop('G-FACTX: %s row %s%s: t times the coefficient, with the floor %s, leaves the amplitude at t = %.6e' % (
                                r, base, it, row[fn_], float(t)))
                if fact4:
                    rows_ = [canon['MR_CRUDEX']['%s_h%d' % (base, d)] for d in range(1, dmax + 1)]
                    for x in rows_:
                        if not (Dm(0) < Dm(x['env_r_hi']) < Dm(1)):
                            raise Stop('G-FACTX: MR_CRUDEX ENV_R_HI = %s at %s must lie in (0, 1)' % (x['env_r_hi'], base))
                    if len(set((x['env_delta0_hi'], x['env_r_hi']) for x in rows_)) != 1:
                        raise Stop('G-FACTX: MR_CRUDEX piece %s carries more than one envelope' % base)
        print('G-FACTX OK: %d x-coefficient rows inside their amplitudes with their floors (power 1) or equal to them (power 0); %d rows with a '
              'Way B floor (last piece, h)%s' % (nchk, nfl, '; one envelope per piece with 0 < env_r < 1' if fact4 else ''))
    nori = 0
    for N in (4, 3):
        for P in sorted(grid[N]):
            base = 'N%d_P%04d' % (N, P)
            sp_ = canon['MR_SPECTRAL'][base]
            if not Dm(sp_['cxm1_lo']) > 0:
                raise Stop('C-ORIENT: MR_SPECTRAL row %s: c_x(-1) = [%s, %s] must be > 0 under "u_x along e1" (the rows 4089, 4310)' % (
                    base, sp_['cxm1_lo'], sp_['cxm1_hi']))
            if not Dm(sp_['cym1_lo']) > 0:
                raise Stop('C-ORIENT: MR_SPECTRAL c_y(-1) on row %s = [%s, %s] must be > 0 under "u_y along e3" (the row 4340)' % (
                    base, sp_['cym1_lo'], sp_['cym1_hi']))
            for X_, f_ in (('t', 'vx_lo'), ('a', 'vx_lo'), ('h', 'vy_lo'), ('t', 'vy_lo'), ('a', 'vy_lo')):
                v_ = canon['MR_INSERT']['%s_%s' % (base, X_)][f_]
                if not Dm(v_) > 0:
                    raise Stop('C-ORIENT: MR_INSERT row %s_%s: %s = %s must be > 0 under the row 4089 convention (the row 4340)' % (
                        base, X_, f_, v_))
            for it, X in (('_h-1', 'h'), ('_h0', 'h'), ('_t-1', 't'), ('_a0', 'a')):
                ex = canon['MR_EXACT'].get(base + it)
                if ex is None:
                    continue
                in_ = canon['MR_INSERT'][base + '_' + X]
                fe = ('Axc_lo', 'Axc_hi') if 'Axc_lo' in ex else ('Ax_lo', 'Ax_hi')
                fi = ('xc_lo', 'xc_hi') if 'xc_lo' in in_ else ('vx_lo', 'vx_hi')
                se, si = sgn_iv(ex[fe[0]], ex[fe[1]]), sgn_iv(in_[fi[0]], in_[fi[1]])
                nori += 1
                if se and si and se != si:
                    raise Stop('C-ORIENT: MR_EXACT row %s%s: the x amplitude has sign %+d against %+d for the bulk %s in MR_INSERT' % (
                        base, it, se, si, X))
    print('C-ORIENT OK: c_x(-1) > 0 and c_y(-1) > 0 on every MR_SPECTRAL row; t and a v_x > 0, h, t and a v_y > 0 on every MR_INSERT row; %d '
          'exact ends checked against the sign of their bulk x amplitude; ORIENT_CHECK on MR_SPECTRAL, MR_INSERT and MR_EXACT with the grid\'s '
          'piece counts' % nori)
    print('A0X %s' % ('ON: the vertical end at d\' = 0 is exact (MR_EXACT a0 rows on every piece)' if a0 else 'OFF: no MR_EXACT a0 rows'))
    print('G-UNIF OK: N = 4 %d pieces, N = 3 %d pieces; every record on the same grid with every row; last piece to inf; decimal fields '
          'finite, lo <= hi, single upper bounds >= 0, the spectral data positive' % (len(grid[4]), len(grid[3])))
    return dict((N, sorted(grid[N])) for N in grid), canon


def float_ref():
    if sha(FREF[0]) != FREF[1]:
        raise Stop('G-FLOAT: reference sha256 %s, pinned %s' % (sha(FREF[0])[:8], FREF[1][:8]))
    ref = {}
    for ln in open(FREF[0]):
        mm = re.match(r'^SUMMARY N=(\d) n=(\d+): .* least headroom (\S+) at', ln)
        if mm:
            ref[(int(mm.group(1)), int(mm.group(2)))] = float(mm.group(3))
    return ref


def evaluate(core, recs, grid, N, n, plant, classes, tail=None):
    Iv, iv2, up = core.Iv, core.iv2, core.up
    out = {}
    for P in grid:
        key = 'N%d_P%04d' % (N, P)
        sp = recs['MR_SPECTRAL'][key]
        sx, sy = iv2(sp['sx_lo'], sp['sx_hi']), iv2(sp['sy_lo'], sp['sy_hi'])
        tau = up(sp['tau_hi'])
        if plant == 'TAU2':
            tau = tau * 10
        rho1, Rw = up(sp['rho1_hi']), up(sp['Rw_hi'])
        if plant == 'DELTA':
            Rw = Rw * 1000
        cxm, cym = iv2(sp['cxm1_lo'], sp['cxm1_hi']), iv2(sp['cym1_lo'], sp['cym1_hi'])
        cmin = lambda z: min(z.lo.copy_abs(), z.hi.copy_abs()) if ((z.lo > 0 and z.hi > 0) or (z.lo < 0 and z.hi < 0)) else Dm(0)
        p2 = Rw * Rw - Iv(cmin(cxm)) * Iv(cmin(cxm)) - Iv(cmin(cym)) * Iv(cmin(cym))
        pem1 = Iv(max(p2.lo, Dm(0)), max(p2.hi, Dm(0))).sqrt()
        e_ = lambda d: Rw * (rho1 ** (d + 1))
        pen = lambda d: (tau ** (d + 1)) * pem1
        cx = lambda d: (sx ** (d + 1)) * cxm
        cy = lambda d: (sy ** (d + 1)) * cym
        rsx_lo, rsy_lo = Iv(sx.lo).sqrt(), Iv(sy.lo).sqrt()
        rsx_hi, rsy_hi = Iv(sx.hi).sqrt(), Iv(sy.hi).sqrt()
        rtau = Iv(tau.hi).sqrt()
        INS = dict((X, recs['MR_INSERT']['%s_%s' % (key, X)]) for X in ('h', 't', 'a'))
        EXA = dict((e, recs['MR_EXACT']['%s_%s' % (key, e)]) for e in ('h-1', 'h0', 't-1', 'a0') if '%s_%s' % (key, e) in recs['MR_EXACT'])
        vxh = iv2(INS['h']['vx_lo'], INS['h']['vx_hi'])
        if plant == 'SIGN' and P == grid[0]:
            vxh = Iv(neg(vxh.amax()), vxh.amax())
        fx = bool(FX)
        if fx:
            thi = Iv(Dm(1)) / iv2(sp['jlo'], sp['jlo'])
            xch = iv2(INS['h']['xc_lo'], INS['h']['xc_hi'])
            if plant == 'XSIGN' and P == grid[0]:
                xch = Iv(neg(xch.amax()), xch.amax())
                vxh = Iv(neg(vxh.amax()), vxh.amax())
            c1 = recs['MR_CRUDEX']['%s_h1' % key]
            envd0, envr = up(c1['env_delta0_hi']), up(c1['env_r_hi'])

        def ehat(dd):
            """e-hat(d) >= |E(d)| / t on the piece: MR_CRUDEX's factored rows up to D_MAX, then the envelope"""
            if dd <= FX['dmax']:
                return up(recs['MR_CRUDEX']['%s_h%d' % (key, dd)]['ehat_hi'])
            return envd0 * (envr ** (dd + 1))

        def exact_ax(dd):
            r = EXA['h%d' % dd]
            ax = iv2(r['Ax_lo'], r['Ax_hi'])
            return Iv(neg(ax.amax()), ax.amax()) if (plant == 'SIGN' and P == grid[0]) else ax

        def crude_e(dd):
            if fx:
                return Iv((thi * ehat(dd)).hi)
            if dd <= 3:
                return up(recs['MR_CRUDEX']['%s_h%d' % (key, dd)]['e_hi'])
            r = INS['h']
            mxx, mxy = iv2(r['mxx_lo'], r['mxx_hi']), iv2(r['mxy_lo'], r['mxy_hi'])
            pbx = peb('h', 'x') / sx
            vp = up(r['vp_hi'])
            return (Iv(cx(dd).amax()) * Iv(mxx.amax()) + Iv(cy(dd).amax()) * Iv(mxy.amax()) + pbx * pen(dd - 1) +
                    vp * e_(dd) * Iv(cx(dd).amax()))

        def peb(X, a):
            """|P_e B^w u_a| for h, t: the record's value, capped by tau C s_a^1/2 (G6 sect. 4.3)"""
            r = INS[X]
            rec = up(r['PeBwux_hi'] if a == 'x' else r['PeBwuy_hi'])
            if r['windowed'] != '1':
                return rec
            cap = rtau * rtau * up(r['C_hi']) * (rsx_hi if a == 'x' else rsy_hi)
            return Iv(min(rec.hi, cap.hi))

        def end(X, d, env=False):
            """(Ay, Ax, N', |P_e a| or None, |S a|, Ay central (float)); Ax of an h end is filled by the caller. env (crude ends only): the
            envelope for every d' >= d (G6 v1_6_1 sect. 5b), the leading terms entering two-sided by their moduli"""
            if (X == 'h' and d <= 0) or (X in ('t', 'a') and d <= -1) or (X == 'a' and d == 0 and 'a0' in EXA):
                r = EXA['a0'] if (X == 'a' and d == 0) else EXA['%s%d' % ('t' if X == 'a' else X, d)]
                Ay, Ax, npr = iv2(r['Ay_lo'], r['Ay_hi']), iv2(r['Ax_lo'], r['Ax_hi']), up(r['Np_hi'])
                Sa = (sx * sx * Iv(Ax.amax()) * Iv(Ax.amax()) + sy * sy * Iv(Ay.amax()) * Iv(Ay.amax()) + npr * npr).sqrt()
                return Ay, Ax, npr, (up(r['Pe_hi']) if 'Pe_hi' in r else None), Sa, float(r['Ay_mid'])
            r = INS[X]
            mxx, mxy, myy = iv2(r['mxx_lo'], r['mxx_hi']), iv2(r['mxy_lo'], r['mxy_hi']), iv2(r['myy_lo'], r['myy_hi'])
            vx, vy = iv2(r['vx_lo'], r['vx_hi']), iv2(r['vy_lo'], r['vy_hi'])
            vp, win = up(r['vp_hi']), up(r['win_hi'])
            if r['windowed'] == '1':
                pbx, pby = peb(X, 'x') / sx, peb(X, 'y') / sy
                dB, dP = d, d
                rem_y = pby * pen(dB - 1) + vp * e_(dB) * Iv(cy(dP).amax())
                rem_x = pbx * pen(dB - 1) + vp * e_(dB) * Iv(cx(dP).amax())
                npr = (up(r['Pevw_hi']) + Iv(cx(dB).amax()) * pbx + Iv(cy(dB).amax()) * pby + win * pen(dB - 1) +
                       vp * e_(dB) * tau * pen(dP))
                Cx = up(r['C_hi'])
                pe1 = (up(r['Pev_hi']) + Iv(cx(dB).amax()) * Cx / rsx_lo + Iv(cy(dB).amax()) * Cx / rsy_lo + Cx * rtau * pen(dB - 1) +
                       vp * e_(dB) * pen(dP))
                pe2 = up(r['Pev_hi']) + Cx * rsx_hi * e_(dB - 1) + vp * e_(dB) * pen(dP)
                pe = Iv(min(pe1.hi, pe2.hi))
            else:
                pbx, pby = up(r['PeBwux_hi']), up(r['PeBwuy_hi'])
                dB, dP = d - 1, d
                rem_y = pby * pen(dB) + vp * e_(dB) * Iv(cy(dP).amax())
                rem_x = pbx * pen(dB) + vp * e_(dB) * Iv(cx(dP).amax())
                core_ = up(r['Pev_hi']) + Iv(cx(dB).amax()) * pbx + Iv(cy(dB).amax()) * pby + vp * e_(dB) * pen(dP)
                npr = tau * (core_ + win * pen(dB))
                pe = core_ + win * pen(dB)
            lead_y = cx(dB) * mxy + cy(dB) * myy
            lead_x = cx(dB) * mxx + cy(dB) * mxy
            if env:
                ly = Iv(cx(dB).amax()) * Iv(mxy.amax()) + Iv(cy(dB).amax()) * Iv(myy.amax())
                lx = Iv(cx(dB).amax()) * Iv(mxx.amax()) + Iv(cy(dB).amax()) * Iv(mxy.amax())
                lead_y, lead_x = Iv(neg(ly.hi), ly.hi), Iv(neg(lx.hi), lx.hi)
            if plant == 'OPN':
                bar = (win * e_(dB - 1)) / sy if r['windowed'] == '1' else win * e_(dB)
                Ay = vy + Iv(neg(bar.hi), bar.hi)
            else:
                Ay = vy + lead_y + Iv(neg(rem_y.hi), rem_y.hi)
            Ax = vx + lead_x + Iv(neg(rem_x.hi), rem_x.hi)
            Sa = (sx * sx * Iv(Ax.amax()) * Iv(Ax.amax()) + sy * sy * Iv(Ay.amax()) * Iv(Ay.amax()) + npr * npr).sqrt()
            ayc = float((vy.lo + vy.hi) / 2 + (lead_y.lo + lead_y.hi) / 2)
            return Ay, Ax, npr, pe, Sa, ayc

        cache = ENDS.setdefault((N, P), {})

        def endc(X, d):
            if (X, d) not in cache:
                cache[(X, d)] = end(X, d)
            return cache[(X, d)]

        def hx_and_e(d):
            """h's x amplitude at d and e = |a_x(h, d) - v_x|_hi (MR_CRUDEX or the plain bound if d >= 1; MR_EXACT against v_x if d <= 0)"""
            if ('hx', d) in cache:
                return cache[('hx', d)]
            if d >= 1:
                e = crude_e(d)
                cache[('hx', d)] = (vxh + Iv(neg(e.hi), e.hi), e)
            else:
                ax = exact_ax(d)
                cache[('hx', d)] = (ax, Iv(max(core.CC.subtract(ax.hi, vxh.lo), core.CC.subtract(vxh.hi, ax.lo))))
            return cache[('hx', d)]

        def alpha_h(d):
            """h's x coefficient interval at d (factored mode): xc + [-e-hat(d), e-hat(d)] for a crude end, Axc for an exact end; a row
            with a Way B floor gives [-1, 1], no certified sign, so X falls back to v1_6's form and the tail's (c) fails there"""
            if d >= 1:
                if Dm(INS['h'].get('xf_hi', '0')) > 0:
                    return Iv(Dm(-1), Dm(1))
                eh = ehat(d)
                return xch + Iv(neg(eh.hi), eh.hi)
            if Dm(EXA['h%d' % d].get('Axf_hi', '0')) > 0:
                return Iv(Dm(-1), Dm(1))
            a_ = iv2(EXA['h%d' % d]['Axc_lo'], EXA['h%d' % d]['Axc_hi'])
            return Iv(neg(a_.amax()), a_.amax()) if (plant in ('SIGN', 'XSIGN') and P == grid[0]) else a_

        def end_tuple(X, d):
            """X's end at d as (A_y, A_x, N', |P_e a| or None, |S a|, A_y central, e or None, x coefficient or None, e(d)): an h end takes
            A_x and e from hx_and_e and, in the factored mode, its coefficient from alpha_h; a t or a end's coefficient is its A_x"""
            Ay, Ax, npr, pe, Sa, ayc = endc(X, d)
            e4 = None
            if X == 'h':
                Ax, e4 = hx_and_e(d)
            co = (alpha_h(d) if X == 'h' else Ax) if fx else None
            return (Ay, Ax, npr, pe, Sa, ayc, e4, co, e_(d))

        def margin(ty, EL, ER, m, lab, count=False):
            """Proposition MR's margin Y_lo - X - R - T2 for the h end EL and the partner end ER of type ty at m (G6 sect. 3), as
            (margin, Y_lo, X, R, T2, delta, why)"""
            AyL, AxL, nL, peL, SaL, aycL, eL4, aL, eL = EL
            AyR, AxR, nR, peR, SaR, aycR, eR4, aR, eR = ER
            why = ''
            if AyL.lo <= 0 or AyR.lo <= 0:
                Ylo = Iv(Dm(0))
                why = 'G-POS'
            else:
                Ylo = (Iv(sy.lo) ** m) * Iv(AyL.lo) * Iv(AyR.lo)
            sgn_ok = False
            if fx:
                sgn_ok = (aL.lo > 0 and aR.lo > 0) or (aL.hi < 0 and aR.hi < 0)
                if count and not sgn_ok:
                    NFB[0] += 1
            x = (sx ** m) * AxL * AxR
            X = Iv(neg(x.lo)) if x.lo < 0 else Iv(Dm(0))
            if sgn_ok:
                X = Iv(Dm(0))
            elif ty == 'h':
                X4 = (Iv(sx.hi) ** m) * (eL4 + eR4) * (eL4 + eR4) / 4
                if X4.hi < X.hi:
                    X = Iv(X4.hi)
            if m >= 2:
                R = (tau ** (m - 2)) * nL * nR
            else:
                cand = [z.hi for z in ((peL * nR) if peL is not None else None, (nL * peR) if peR is not None else None) if z is not None]
                if not cand:
                    raise Stop('m = 1 class %s with two exact ends: no rest bound' % lab)
                R = Iv(min(cand))
            dz = (Iv(sx.hi) ** m) * eL * eR
            if not dz.hi < 1:
                why = why or 'G-DELTA'
                T2 = Iv(Dm(0))
            else:
                T2 = (Iv(sx.hi) ** (2 * m - 2)) * SaL * SaR * eL * eR / (Iv(Dm(1)) - dz)
            if plant == 'T2':
                T2 = T2 * 1000
            return Ylo - X - R - T2, Ylo, X, R, T2, dz, why

        def tail_piece():
            """G6 v1_6_1 sect. 5b on this piece: the crude end envelopes at D0, the envelope classes (m < M0), Lemma T(b)'s m-tail at M0,
            the sign condition (c) and Proposition J's envelope orbits"""
            D0, M0 = tail[0], tail[1]
            for nm_, z_ in (('s_x', sx.hi), ('s_y', sy.hi), ('tau', tau.hi), ('rho_1', rho1.hi), ('env_r', envr.hi)):
                if not z_ < 1:
                    raise Stop('C-TAILMONO N%d piece %d: the upper end %s of %s is not below 1' % (N, P, z_, nm_))
            De = D0 + 1 if plant == 'TAILENV' else D0
            dmax = FX['dmax']
            sup = max([ehat(dd).hi for dd in range(De, dmax + 1)] + [ehat(max(De, dmax + 1)).hi])
            env = {}
            for X in ('h', 't', 'a'):
                Ay, Ax, npr, pe, Sa, ayc = end(X, De, env=True)
                if X == 'h':
                    e4 = Iv((thi * Iv(sup)).hi)
                    coh = Iv(Dm(-1), Dm(1)) if Dm(INS['h'].get('xf_hi', '0')) > 0 else xch + Iv(neg(sup), sup)
                    env[X] = (Ay, vxh + Iv(neg(e4.hi), e4.hi), npr, pe, Sa, ayc, e4, coh, e_(De))
                else:
                    env[X] = (Ay, Ax, npr, pe, Sa, ayc, None, Ax, e_(De))
            if plant == 'TAILSIGN' and P == grid[0]:
                ct_ = env['t'][7]
                env['t'] = env['t'][:7] + (Iv(neg(ct_.hi), neg(ct_.lo)),) + env['t'][8:]
            for X in ('h', 't', 'a'):
                E = env[X]
                for dd in sorted(set(list(range(D0, D0 + 13)) + [dmax, dmax + 1])):
                    T_ = end_tuple(X, dd)
                    bad = [nm_ for nm_, ok_ in (
                        ('A_y', E[0].lo <= T_[0].lo and T_[0].hi <= E[0].hi), ('A_x', E[1].lo <= T_[1].lo and T_[1].hi <= E[1].hi),
                        ("N'", T_[2].hi <= E[2].hi), ('|P_e a|', T_[3] is None or (E[3] is not None and T_[3].hi <= E[3].hi)),
                        ('|S a|', T_[4].hi <= E[4].hi), ('e', T_[8].hi <= E[8].hi),
                        ('coefficient', X != 'h' or (T_[6].hi <= E[6].hi and E[7].lo <= T_[7].lo and T_[7].hi <= E[7].hi))) if not ok_]
                    if bad:
                        raise Stop('C-TAILMONO N%d piece %d: the %s envelope at D0 = %d does not enclose the end at d = %d (%s)' % (
                            N, P, X, D0, dd, ', '.join(bad)))
            dl_ = list(range(-1, D0))
            nenv, nfe, best = 0, 0, None
            for ty in ('t', 'a', 'h'):
                for m in range(2 if ty == 'h' else 1, M0):
                    for dL, dR in [('E', z) for z in dl_] + [(z, 'E') for z in dl_] + [('E', 'E')]:
                        EL = env['h'] if dL == 'E' else end_tuple('h', dL)
                        ER = env[ty] if dR == 'E' else end_tuple(ty, dR)
                        lab = 'h%s-%s%s/m%d' % ('D0+' if dL == 'E' else dL, ty, 'D0+' if dR == 'E' else dR, m)
                        marg, Ylo, X, R, T2, dz, why = margin(ty, EL, ER, m, lab)
                        ok = marg.lo > 0 and not why
                        L = (marg / (Iv(Dm(1)) + dz)).lo if ok else marg.lo
                        nenv += 1
                        nfe += 0 if ok else 1
                        if best is None or L < best[0]:
                            best = (L, lab)
            Ast, Npst, Nst = {}, {}, {}
            for X in ('h', 't', 'a'):
                ends_ = [end_tuple(X, z) for z in dl_] + [env[X]]
                Ast[X] = min(E[0].lo for E in ends_)
                Npst[X] = max(E[2].hi for E in ends_)
                Nst[X] = max(E[4].hi for E in ends_)
            if plant == 'TAILQ':
                Npst = dict((X, v * 1000000) for X, v in Npst.items())
            th_ = up(tau.hi)
            qR, qT = th_ / Iv(sy.lo), Iv(sx.hi) * Iv(sx.hi) / Iv(sy.lo)
            dst = (Iv(sx.hi) ** M0) * Rw * Rw
            mt = []
            for T in ('t', 'a', 'h'):
                if not (qR.hi < 1 and qT.hi < 1 and dst.hi < 1 and Ast['h'] > 0 and Ast[T] > 0):
                    mt.append((None, T))
                    continue
                lhs = (Iv(Ast['h']) * Iv(Ast[T]) - (qR ** M0) / (th_ * th_) * Iv(Npst['h']) * Iv(Npst[T]) -
                       (qT ** M0) / (Iv(sx.hi) * Iv(sx.hi)) * Iv(Nst['h']) * Iv(Nst[T]) * Rw * Rw / (Iv(Dm(1)) - dst))
                mt.append((lhs.lo, T))
            sh, st = set(), set()
            for z in dl_:
                co = end_tuple('h', z)[7]
                sh.add(sgn_iv(co.lo, co.hi))
                for X in ('t', 'a'):
                    co = end_tuple(X, z)[7]
                    st.add(sgn_iv(co.lo, co.hi))
            sh.add(sgn_iv(env['h'][7].lo, env['h'][7].hi))
            for X in ('t', 'a'):
                st.add(sgn_iv(env[X][7].lo, env[X][7].hi))
            sign_ok = len(sh) == 1 and len(st) == 1 and 0 not in sh and 0 not in st and min(sh) * min(st) == 1
            lj = [(sb_piece(core, recs, key, D0, z)[0].lo, z) for z in range(0, D0 + 1)]
            return {'nenv': nenv, 'envfail': nfe, 'envL': best[0], 'envlab': best[1], 'mt': mt, 'qR': qR.hi, 'qT': qT.hi, 'sign': sign_ok,
                    'sup': sup, 'dmax': dmax,
                    'lj': min(lj), 'ljfail': sum(1 for v, z in lj if not v > 0)}

        for c in classes:
            ty, d, kr, dp, ori = core.position(c[0], c[1], n)
            m = kr + 2 if ty in ('t', 'h') else kr + 1
            if m == 0:
                continue
            EL, ER = end_tuple('h', d), end_tuple(ty, dp)
            AyL, AyR, aycL, aycR = EL[0], ER[0], EL[5], ER[5]
            route = 'chan-crude' if (d >= 1 or (ty == 'h' and dp >= 1)) else 'chan-exact'
            marg, Ylo, X, R, T2, dz, why = margin(ty, EL, ER, m, '%s-%s' % ori, count=True)
            ok = marg.lo > 0 and not why
            fl = set()
            if AyL.lo <= 0 or AyR.lo <= 0:
                fl.add('G-POS')
            if not dz.hi < 1:
                fl.add('G-DELTA')
            if not ok and not fl:
                fl.add('MARGIN')
            L = (marg / (Iv(Dm(1)) + dz)).lo if ok else marg.lo
            yc = float(sy.lo) ** m * aycL * aycR
            den = yc - float(Ylo.lo) + float(X.hi) + float(R.hi) + float(T2.hi)
            H = yc / den if den > 0 else float('inf')
            lab = '%s-%s' % ori
            prev = out.get(c)
            if prev is None:
                out[c] = {'lab': lab, 'route': route, 'd': d, 'k': kr, 'dp': dp, 'm': m, 'L': L, 'P': P, 'H': H, 'ok': ok, 'why': why,
                          'Lp': {P: L}, 'fl': set(fl)}
            else:
                prev['Lp'][P] = L
                if L < prev['L']:
                    prev['L'], prev['P'] = L, P
                prev['H'] = min(prev['H'], H)
                prev['ok'] = prev['ok'] and ok
                prev['why'] = prev['why'] or why
                prev['fl'] = prev['fl'] | fl
        if tail is not None:
            TAILOUT[(N, P)] = tail_piece()
    return out


def sb_piece(core, recs, key, dL, dR):
    """Proposition J's L_J on one piece for a same-bond orbit with end exponents dL, dR (the exact form), as (L_J, delta, Cb_mid)"""
    Iv, iv2, up = core.Iv, core.iv2, core.up
    sp = recs['MR_SPECTRAL'][key]
    j = recs['MR_JOINT'][key]
    ih, it = recs['MR_INSERT'][key + '_h'], recs['MR_INSERT'][key + '_t']
    sx, sy = iv2(sp['sx_lo'], sp['sx_hi']), iv2(sp['sy_lo'], sp['sy_hi'])
    tau, rho1, Rw = up(sp['tau_hi']), up(sp['rho1_hi']), up(sp['Rw_hi'])
    cxm, cym = iv2(sp['cxm1_lo'], sp['cxm1_hi']), iv2(sp['cym1_lo'], sp['cym1_hi'])
    cmin = lambda z: min(z.lo.copy_abs(), z.hi.copy_abs()) if ((z.lo > 0 and z.hi > 0) or (z.lo < 0 and z.hi < 0)) else Dm(0)
    p2 = Rw * Rw - Iv(cmin(cxm)) * Iv(cmin(cxm)) - Iv(cmin(cym)) * Iv(cmin(cym))
    pem1 = Iv(max(p2.lo, Dm(0)), max(p2.hi, Dm(0))).sqrt()
    e_ = lambda d: Rw * (rho1 ** (d + 1))
    pen = lambda d: (tau ** (d + 1)) * pem1
    ax_ = lambda d: Iv(((sx ** (d + 1)) * cxm).amax())
    ay_ = lambda d: Iv(((sy ** (d + 1)) * cym).amax())
    ch, ct = Iv(iv2(j['ch_lo'], j['ch_hi']).amax()), Iv(iv2(j['ct_lo'], j['ct_hi']).amax())
    hx, hy = Iv(iv2(ih['vx_lo'], ih['vx_hi']).amax()), Iv(iv2(ih['vy_lo'], ih['vy_hi']).amax())
    tx, ty_ = Iv(iv2(it['vx_lo'], it['vx_hi']).amax()), Iv(iv2(it['vy_lo'], it['vy_hi']).amax())
    PewJw = Iv(min(up(j['PewJw_hi']).hi, (tau * up(j['Wc_hi'])).hi))
    F1 = Iv(Dm(0))
    B1 = Iv(Dm(0))
    C1 = Iv(Dm(0))
    for dd in (dL, dR):
        F1 = F1 + ax_(dd - 1) * up(j['wJwx_hi']) + ay_(dd - 1) * up(j['wJwy_hi']) + pen(dd - 1) * PewJw
        B1 = B1 + hx * ax_(dd) + hy * ay_(dd) + up(ih['Pev_hi']) * pen(dd)
        C1 = C1 + tx * ax_(dd) + ty_ * ay_(dd) + up(it['Pev_hi']) * pen(dd)
    dl = ax_(dL) * ax_(dR) + ay_(dL) * ay_(dR) + pen(dL) * pen(dR)
    ee = e_(dL - 1) * e_(dR - 1)
    br2 = up(j['jfw_hi']) * ee + up(j['A0_hi']) * dl + B1 * C1
    A1 = F1 + ch * C1 + ct * B1
    B2 = up(j['bh_hi']) * ee + ch * dl
    C2 = up(j['bt_hi']) * ee + ct * dl
    br3 = dl * A1 + B1 * C2 + B2 * C1
    A2 = (up(j['jfw_hi']) + ch * up(j['bt_hi']) + ct * up(j['bh_hi']) + Iv(Dm(2)) * ch * ct * sx * sx) * ee
    br4 = dl * A2 + B2 * C2
    LJ = Iv(Dm(j['Cb_lo'])) - F1 - br2 - br3 - br4
    return LJ, dl, float(j['Cb_mid'])


def samebond(core, recs, grid, N, n):
    Iv = core.Iv
    res = []
    for i in range(2, n // 2 + 1):
        best = None
        for P in grid:
            LJ, dl, cbm = sb_piece(core, recs, 'N%d_P%04d' % (N, P), i - 2, n - i - 2)
            ok = LJ.lo > 0
            L = (LJ / ((Iv(Dm(1)) + dl) * (Iv(Dm(1)) + dl))).lo if ok else LJ.lo
            HJ = cbm / (cbm - float(LJ.lo)) if cbm > float(LJ.lo) else float('inf')
            if best is None:
                best = (L, P, HJ, ok)
            else:
                best = (min(best[0], L), best[1] if best[0] <= L else P, min(HJ, best[2]), best[3] and ok)
        res.append((i, best))
    return res


def main():
    ENDS.clear()
    del OWNER_OK[:]
    FMT.clear()
    FX.clear()
    TSET.clear()
    TAILOUT.clear()
    OCHK.clear()
    PEX.clear()
    NFB[0] = 0
    recdir, pins_sha, mode, outp = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    plant = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != 'none' else None
    nmax = int(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] != 'default' else (14 if plant is None else 10)
    pieces = sys.argv[7] if len(sys.argv) > 7 and sys.argv[7] not in ('all', 'none') else None
    targ = sys.argv[8] if len(sys.argv) > 8 and sys.argv[8] != 'none' else None
    tail = None
    if targ:
        tz = targ.split(':')
        assert len(tz) in (2, 3) and (len(tz) == 2 or tz[2] == 'D'), 'TAIL must be D0:M0 or D0:M0:D'
        tail = (int(tz[0]), int(tz[1]), len(tz) == 3)
        assert tail[0] >= 1 and tail[1] >= 2, 'TAIL needs D0 >= 1 and M0 >= 2'
    assert mode in ('STANDIN', 'CERTIFIED') and (plant is None or plant in PLANTS)
    assert plant not in TAIL_PLANTS or tail is not None, 'the tail plants need TAIL'
    if tail is not None:
        print('TAIL ARGUMENT %s: D0 %d, M0 %d, n0 = 2 D0 + M0 + 1 = %d%s' % (targ, tail[0], tail[1], 2 * tail[0] + tail[1] + 1,
                                                                          ' (design run)' if tail[2] else ''))
    print('kt_mr_assembly_v1_8_4 (%s): RECDIR %s MODE %s PLANT %s NMAX %d PIECES %s' % (sha(__file__), recdir.replace(W, ''), mode,
                                                                                      plant or 'none', nmax, pieces or 'all'))
    try:
        core = c_core()
        c_iv(core)
        recs, heads, pins = g_pin(recdir, pins_sha, mode, plant)
        grids, recs = g_unif(recs, heads, plant)
        if FMT == {'MR_INPUT_KV_v4'} and heads['MR_CRUDEX'].get('CRUDEX_FORM') == 'factored':
            FX['dmax'] = int(heads['MR_CRUDEX']['D_MAX'])
        print('XMODE %s' % (('FACTORED: x signs read on the coefficient intervals (MR_INPUT_KV_v4, factored MR_CRUDEX, D_MAX %d)' % FX['dmax'])
                            if FX else ('UNFACTORED: the rows of v1_6 (%s, CRUDEX_FORM %s)' % (sorted(FMT)[0], heads['MR_CRUDEX'].get('CRUDEX_FORM')))))
        print('ROUTE V %s' % ('ON: MR_EXACT carries Pe_hi (the exact end\'s unwindowed flip-even |P_e a|), and the m = 1 rest takes the least '
                               'of |P_e a_L| N\'_R and N\'_L |P_e a_R| over the ends that give |P_e a| (the row 4376)' if PEX else
                               'OFF: MR_EXACT has no Pe_hi; the m = 1 rest uses the crude ends\' |P_e a| only'))
        ref = float_ref()
        if tail is not None:
            if not FX:
                raise Stop('G-TAIL: the tail section needs the factored mode (MR_INPUT_KV_v4 with a factored MR_CRUDEX)')
            if not tail[2] and nmax < 2 * tail[0] + tail[1] + 1:
                raise Stop('G-TAIL: NMAX %d is below n0 = 2 D0 + M0 + 1 = %d, so the finite check does not reach n0' % (
                    nmax, 2 * tail[0] + tail[1] + 1))
    except Stop as ex:
        print('STOP %s' % ex)
        fired = plant in STOP_GATE and str(ex).startswith(STOP_GATE[plant])
        print('PLANT %s: %s' % (plant, 'FIRED' if fired else 'NOT FIRED (UNEXPECTED STOP)') if plant else 'RUN_VERDICT STOPPED')
        return 0 if fired else 8
    if pieces:
        a_, b_ = [int(z) for z in pieces.split(':')]
        grids = dict((N, [P for P in grids[N] if a_ <= P < b_]) for N in grids)
        if not grids[4] or not grids[3]:
            print('STOP PIECES %s selects no piece for some N' % pieces)
            return 8
    rows, nfail, flags, infos = [], 0, [], []
    nwhy = {'G-POS': 0, 'G-DELTA': 0, 'MARGIN': 0, 'TAIL-ENV': 0, 'TAIL-MTAIL': 0, 'TAIL-SIGN': 0, 'TAIL-J': 0}
    if FX:
        nsg, Iv_ = 0, core.Iv
        for N in (4, 3):
            for P in grids[N]:
                key = 'N%d_P%04d' % (N, P)
                xc_ = core.iv2(recs['MR_INSERT'][key + '_h']['xc_lo'], recs['MR_INSERT'][key + '_h']['xc_hi'])
                mod = xc_.lo if xc_.lo > 0 else (neg(xc_.hi) if xc_.hi < 0 else Dm(0))
                c1 = recs['MR_CRUDEX'][key + '_h1']
                ehs = [core.up(recs['MR_CRUDEX']['%s_h%d' % (key, d)]['ehat_hi']).hi for d in range(1, FX['dmax'] + 1)]
                ehs.append((core.up(c1['env_delta0_hi']) * (core.up(c1['env_r_hi']) ** (FX['dmax'] + 2))).hi)
                nsg += 1
                if not max(ehs) < mod:
                    flags.append('C-SIGN N%d piece %d: e-hat up to %.4e against the coefficient modulus %.4e' % (N, P, float(max(ehs)), float(mod)))
        print('C-SIGN %s: %d pieces, e-hat(d) for d = 1..%d and the envelope at %d against the modulus of h\'s coefficient' % (
            'FAILED' if any(f.startswith('C-SIGN') for f in flags) else 'OK', nsg, FX['dmax'], FX['dmax'] + 1))
    try:
        for N in (4, 3):
            for n in range(6, nmax + 1):
                classes = core.todo(n)
                if plant == 'COUNT' and n == 10:
                    classes = classes[:-1]
                if len(classes) != core.EXPECT[n]:
                    print('STOP G-COUNT N=%d n=%d: %d to-do orbits against %d' % (N, n, len(classes), core.EXPECT[n]))
                    print('PLANT %s: %s' % (plant, 'FIRED' if plant == 'COUNT' else 'NOT FIRED (UNEXPECTED STOP)') if plant else 'RUN_VERDICT STOPPED')
                    return 0 if plant == 'COUNT' else 8
                res = evaluate(core, recs, grids[N], N, n, plant, classes)
                for c in res:
                    for tw in core.corner_twin(c[0], c[1], n):
                        if tw in res and tw != c and c < tw and any(res[c]['Lp'][P] != res[tw]['Lp'][P] for P in grids[N]):
                            flags.append('G-CORNER N%d n%d %s/%s' % (N, n, res[c]['lab'], res[tw]['lab']))
                sb = samebond(core, recs, grids[N], N, n)
                hmin = min(r_['H'] for r_ in res.values())
                href = ref.get((N, n))
                if plant is None and not pieces:
                    infos.append('G-FLOAT INFO N%d n%d: least headroom %.4f, reference %s%s' % (
                        N, n, hmin, ('%.4f' % href) if href else '-', '' if (href is not None and abs(hmin - href) <= 1e-3 * href + 0.005) else
                        ' (differs)'))
                npass = sum(1 for r_ in res.values() if r_['ok'])
                nf_n = len(res) - npass + sum(1 for i, b in sb if not b[3])
                nfail += nf_n
                for why_ in ('G-POS', 'G-DELTA', 'MARGIN'):
                    nwhy[why_] += sum(1 for r_ in res.values() if why_ in r_['fl'])
                nwhy['MARGIN'] += sum(1 for i, b in sb if not b[3])
                worst = min(res.values(), key=lambda r_: r_['H'])
                print('SUMMARY N=%d n=%d: to-do orbits %d; channel classes %d, PASS %d; least headroom %.3f at %s (piece %d); reference %s; '
                      'same-bond orbits %d, least H_J %.2f; FAIL %d' % (N, n, len(classes), len(res), npass, hmin, worst['lab'], worst['P'],
                                                                        ('%.3f' % href) if href else '-', len(sb), min([b[2] for i, b in sb] or [0]), nf_n))
                for c in sorted(res, key=lambda c: res[c]['lab']):
                    r_ = res[c]
                    rows.append(('N%d_n%02d_%s' % (N, n, r_['lab']), [r_['route'], str(r_['d']), str(r_['k']), str(r_['dp']), str(r_['m']), str(r_['L']),
                                                                      str(r_['P']), 'PASS' if r_['ok'] else 'FAIL', '%.6g' % r_['H']]))
                    if not r_['ok'] or (n == 6 and plant is None and not pieces):
                        print('CLASS N=%d n=%d %-9s %s d=%d k=%d dp=%d m=%d: L %.6e at piece %d, H %.3f %s %s' % (
                            N, n, r_['lab'], r_['route'], r_['d'], r_['k'], r_['dp'], r_['m'], float(r_['L']), r_['P'], r_['H'],
                            'PASS' if r_['ok'] else 'FAIL', r_['why']))
                for i, b in sb:
                    rows.append(('N%d_n%02d_h%d-t%d' % (N, n, i, i), ['same-bond', str(i - 2), '-2', str(n - i - 2), '0', str(b[0]), str(b[1]),
                                                                      'PASS' if b[3] else 'FAIL', '%.6g' % b[2]]))
        if tail is not None:
            for N in (4, 3):
                evaluate(core, recs, grids[N], N, 0, plant, [], tail)
    except Stop as ex:
        print('STOP %s' % ex)
        fired = plant in STOP_GATE and str(ex).startswith(STOP_GATE[plant])
        if plant:
            print('PLANT %s: %s' % (plant, 'FIRED' if fired else 'NOT FIRED (UNEXPECTED STOP)'))
        return 0 if fired else 8
    for f in infos:
        print(f)
    for f in flags[:20]:
        print(f)
    if FX:
        print('FACTORED SIGN FALLBACK: %d class-piece evaluations had no certified sign for the product of the two x coefficients, so X took '
              'v1_6\'s form there (the v1_7 N-2)' % NFB[0])
    print('FAIL REASONS: classes failing at G-POS %d, at G-DELTA %d, on the margin alone %d (same-bond failures count as margin)' % (
        nwhy['G-POS'], nwhy['G-DELTA'], nwhy['MARGIN']))
    tpass, tail_ok, trows = True, True, []
    if tail is not None:
        for N in (4, 3):
            tr = [(P, TAILOUT[(N, P)]) for P in grids[N]]
            fe = sum(v['envfail'] for P, v in tr)
            be = min(tr, key=lambda pv: pv[1]['envL'])
            mts = [(lhs, T, P) for P, v in tr for lhs, T in v['mt']]
            fm = sum(1 for lhs, T, P in mts if lhs is None or not lhs > 0)
            bm = min(mts, key=lambda z: (z[0] is not None, z[0] if z[0] is not None else Dm(0)))
            fs = sum(1 for P, v in tr if not v['sign'])
            fj = sum(v['ljfail'] for P, v in tr)
            bj = min(tr, key=lambda pv: pv[1]['lj'][0])
            nwhy['TAIL-ENV'] += fe
            nwhy['TAIL-MTAIL'] += fm
            nwhy['TAIL-SIGN'] += fs
            nwhy['TAIL-J'] += fj
            print('TAIL N=%d D0 %d M0 %d: envelope classes %d per piece, FAIL %d, least L %.6e at %s (piece %d); m-tail at M0: FAIL %d, least '
                  'lower end %s (pair h-%s, piece %d), q_R <= %.4f, q_T <= %.4f; sign condition (c): FAIL on %d pieces; Proposition J envelope '
                  'orbits: FAIL %d, least L_J %.6e (d_R %d, piece %d)' % (
                      N, tail[0], tail[1], tr[0][1]['nenv'], fe, float(be[1]['envL']), be[1]['envlab'], be[0], fm,
                      ('%.6e' % float(bm[0])) if bm[0] is not None else 'none (q < 1, delta* < 1 or A* > 0 fails)', bm[1], bm[2],
                      float(max(v['qR'] for P, v in tr)), float(max(v['qT'] for P, v in tr)), fs, fj, float(bj[1]['lj'][0]), bj[1]['lj'][1], bj[0]))
            dmx_ = tr[0][1]['dmax']
            print('C-TAILMONO OK N=%d: %d pieces; s_x, s_y, tau, rho_1 and env_r below 1; the envelope at D0 = %d encloses the end at d = %d..%d, '
                  '%d and %d (A_y, A_x, N\', |P_e a|, |S a|, e; for h also the coefficient and e)' % (
                      N, len(tr), tail[0], tail[0], tail[0] + 12, dmx_, dmx_ + 1))
            sups = [v['sup'] for P, v in tr]
            print('TAIL SUP N=%d: sup over d >= D0 = %d of e-hat(d) = max(rows %d..%d, envelope at %d): least %.6e, largest %.6e over the pieces; '
                  'it enters h\'s envelope as the coefficient xc -+ sup and the x amplitude v_x -+ t_hi sup (the h end at every d >= D0)' % (
                      N, tail[0], tail[0], dmx_, max(tail[0], dmx_ + 1), float(min(sups)), float(max(sups))))
            for P, v in tr:
                ok_ = v['envfail'] == 0 and all(l is not None and l > 0 for l, T in v['mt']) and v['sign'] and v['ljfail'] == 0
                tpass = tpass and ok_
                mtd = dict((T, l) for l, T in v['mt'])
                trows.append(('N%d_P%04d' % (N, P), [str(tail[0]), str(tail[1]), str(v['nenv']), str(v['envfail']), str(v['envL']), v['envlab']] +
                              [str(mtd[T]) if mtd[T] is not None else 'none' for T in ('t', 'a', 'h')] +
                              [str(v['qR']), str(v['qT']), 'OK' if v['sign'] else 'FAIL', str(v['lj'][0]), str(v['lj'][1]), str(v['ljfail']),
                               'PASS' if ok_ else 'FAIL']))
        tail_ok = tpass or tail[2]
        print('TAIL REASONS: envelope classes failing %d, m-tail pairs failing %d, pieces failing the sign condition %d, Proposition J '
              'envelope orbits failing %d' % (nwhy['TAIL-ENV'], nwhy['TAIL-MTAIL'], nwhy['TAIL-SIGN'], nwhy['TAIL-J']))
    tline = ('%d %d %d%s' % (tail[0], tail[1], 2 * tail[0] + tail[1] + 1, ' DESIGN' if tail[2] else '')) if tail else 'none'
    tverd = (('DESIGN-' if tail[2] else '') + ('PASS' if tpass else 'FAIL')) if tail else 'none'
    if tail is not None:
        print('TAIL_VERDICT %s (TAIL = %s)' % (tverd, tline))
    warns = [(k, v) for k, v in rows if float(v[8]) < 2]
    print('WARN BLOCK: %d rows with float headroom H < 2 (design target 2; not an acceptance rule)' % len(warns))
    for k, v in sorted(warns, key=lambda kv: float(kv[1][8])):
        print('WARN %s H %s %s' % (k, v[8], v[7]))
    verdict = 'VALID' if (nfail == 0 and not flags and tail_ok) else 'INVALID'
    if mode == 'STANDIN' and verdict == 'VALID':
        verdict = 'STANDIN-VALID'
    head = ['# MR_ASSEMBLY: kt_mr_assembly_v1_8_4 output (%s)' % ('stand-in inputs; not a certificate' if mode == 'STANDIN' else 'certified inputs'),
            'FORMAT = MR_ASSEMBLY_KV_v1', 'RECORD = %s' % ('MR_ASSEMBLY_PART' if pieces else 'MR_ASSEMBLY_%s' % (plant or 'BASE')),
            'PRODUCER = pk24 kt_mr_assembly_v1_8_4', 'CODE = pk24/mr_engine/kt_mr_assembly_v1_8_4.py:%s' % sha(__file__),
            'INPUT_PINS = %s' % ' '.join('%s:%s' % (k, v) for k, v in sorted(pins.items())), 'MODE = %s' % mode, 'PLANT = %s' % (plant or 'none'),
            'NMAX = %d' % nmax, 'INPUT_FORMAT = %s' % sorted(FMT)[0], 'XMODE = %s' % ('factored' if FX else 'unfactored'),
            'TRIAL_SET = %s' % (sorted(TSET)[0] if TSET else 'none'), 'TAIL = %s' % tline, 'TAIL_VERDICT = %s' % tverd, 'ROUTE_V = %s' % ('on' if PEX else 'off'), 'PIECES_N4 = %s' % ' '.join(str(P) for P in grids[4]), 'PIECES_N3 = %s' % ' '.join(str(P) for P in grids[3]),
            'WARN_ROWS = %d' % len(warns), 'RUN_VERDICT = %s' % (('PART-' + verdict) if pieces else verdict),
            'FIELDS = route d k dp m Lmin piece verdict Hmin']
    body = ['%s = %s' % (k, ' '.join(v)) for k, v in rows]
    cnt = ['COUNT = rows %d pass %d fail %d' % (len(rows), sum(1 for k, v in rows if v[7] == 'PASS'), sum(1 for k, v in rows if v[7] == 'FAIL'))]
    with open(outp, 'x') as fh:
        fh.write('\n'.join(head + body + cnt) + '\n')
    print('WROTE %s %s (%d rows); FAIL rows %d; gate lines %d; WARN rows %d' % (sha(outp)[:8], outp.replace(W, ''), len(rows), nfail, len(flags),
                                                                               len(warns)))
    if tail is not None:
        tp = outp + '.tail'
        tv = ('PART-' if pieces else '') + tverd
        thead = ['# MR_TAIL: kt_mr_assembly_v1_8_4 tail section of G6 v1_6_1 sect. 5b (%s)' % (
                     'stand-in inputs; not a certificate' if mode == 'STANDIN' else 'certified inputs'),
                 'FORMAT = MR_TAIL_KV_v1', 'RECORD = %s' % ('MR_TAIL_PART' if pieces else 'MR_TAIL_%s' % (plant or 'BASE')),
                 'PRODUCER = pk24 kt_mr_assembly_v1_8_4', 'CODE = pk24/mr_engine/kt_mr_assembly_v1_8_4.py:%s' % sha(__file__),
                 'INPUT_PINS = %s' % ' '.join('%s:%s' % (k, v) for k, v in sorted(pins.items())), 'MODE = %s' % mode,
                 'PLANT = %s' % (plant or 'none'), 'TAIL = %s' % tline, 'PIECES_N4 = %s' % ' '.join(str(P) for P in grids[4]),
                 'PIECES_N3 = %s' % ' '.join(str(P) for P in grids[3]), 'TAIL_VERDICT = %s' % tv,
                 'FIELDS = D0 M0 nenv envfail envL envclass mtail_t mtail_a mtail_h qR qT sign LJmin LJdR LJfail verdict']
        tbody = ['%s = %s' % (k, ' '.join(v)) for k, v in trows]
        tcnt = ['COUNT = rows %d pass %d fail %d' % (len(trows), sum(1 for k, v in trows if v[-1] == 'PASS'), sum(1 for k, v in trows if v[-1] == 'FAIL'))]
        with open(tp, 'x') as fh:
            fh.write('\n'.join(thead + tbody + tcnt) + '\n')
        print('WROTE TAIL %s %s (%d rows); TAIL_VERDICT %s' % (sha(tp)[:8], tp.replace(W, ''), len(trows), tv))
    if plant is None:
        print('RUN_VERDICT %s' % (('PART-' + verdict) if pieces else verdict))
        return 0 if verdict in ('VALID', 'STANDIN-VALID') else 9
    if plant in STOP_PLANTS:
        print('PLANT %s: NOT FIRED (the run did not stop)' % plant)
        return 9
    if plant == 'PRODOK':
        fired = len(OWNER_OK) == len(RECS) and nfail == 0 and not flags
        print('PLANT PRODOK: %s (the owner rule passed on %d of %d records with owner PRODUCER lines; FAIL rows %d, gate lines %d; a positive '
              'control)' % ('FIRED' if fired else 'NOT FIRED', len(OWNER_OK), len(RECS), nfail, len(flags)))
        return 0 if fired else 9
    own = OWN_FAIL[plant]
    fired = nwhy[own] > 0
    print('PLANT %s: %s on its own failure %s (classes failing at G-POS %d, at G-DELTA %d, on the margin alone %d; FAIL rows %d, gate '
          'lines %d)' % (plant, 'FIRED' if fired else 'NOT FIRED', own, nwhy['G-POS'], nwhy['G-DELTA'], nwhy['MARGIN'], nfail, len(flags)))
    return 0 if fired else 9


if __name__ == '__main__':
    sys.exit(main())
