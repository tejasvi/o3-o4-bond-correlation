#!/usr/bin/env python3
"""kt_s9h_v1_3_readers.py -- pk07 (code/pk07/). The side-effect-free readers of kt_s9h_v1_3 (f89faabf), for pk15's
kt_p2_assembly_v1_36 certified read-back (the approval on (A), 2026-11-08). Importing this file sets no rlimit, installs no signal handler,
opens no file, reads no argv and never exits; it uses a private mpmath interval context at kt_s9h_v1_3's 25 digits, so the importer's
mpmath.iv and mpmath.mp settings stay as they are.

Every function and constant below the import block is copied verbatim, byte for byte, from kt_s9h_v1_3.py f89faabf.
test_v1_3_readers_v1.py checks the source text of each against that file, runs joint_read and t_read through both files on
kt_p2_assembly_v1_35's MOCK exports, and checks this file's import for side effects in its own process. Only this header (the imports and
the private interval context) is new.

Interface:
  rec = s4u_read_port(text); grid = joint_grid()           # joint_grid reads v2_2's pinned export (V22_EXPORT) when called
  J, problems = joint_read(rec, grid)                       # the joint export, six- or seven-column layout by FIELDS
  T, problems = t_read(rec, grid, R, aa)                    # R = dict(record='EXPORT_P2_T_v1', fmt='S4U_KV_v1', status='CERTIFIED')
  ok = bound_ok(base_name, sha256_hex, run_output_text)     # the run output's binding (needs its final VERDICT line)
An empty problems list is the pass; ValueError only for an unparsable line, a repeated key or a token that is not a decimal."""
import os
import re
import hashlib
from fractions import Fraction
from mpmath.ctx_iv import MPIntervalContext

iv = MPIntervalContext()              # private: the importer's mpmath.iv is not touched
iv.dps = 25                           # kt_s9h_v1_3's interval precision (its l.469)
IVT = type(iv.mpf(1))


CODEDIR = '/mnt/g2/release/root/code'


V22_EXPORT = ('pk07/out/export_kt_s67_cert_v2_2_sweep.kv', '6fe9ab65f5207dc3658c98ff4f3696bd2db6aa784b0dec84b33881b2da579c34')


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def pt(x):
    """a point interval (exact for floats, ints, strings rounded outward)."""
    return x if isinstance(x, IVT) else iv.mpf(x)


def dec_frac(s):
    """an S4U_KV_v1 number (a decimal with optional sign, fraction and exponent) as an exact rational; anything else is an error."""
    if not isinstance(s, str) or re.fullmatch(r'-?[0-9]+(\.[0-9]+)?(e[+-]?[0-9]+)?', s) is None:
        raise ValueError('not a decimal number: %r' % (s,))
    return Fraction(s)


def dec_iv(s):
    """the exact decimal s as an mp.iv enclosure: numerator / denominator in outward interval arithmetic (no decimal string rounding)."""
    q = dec_frac(s)
    return pt(q.numerator) / pt(q.denominator)


def verdict_lines_ok(lines):
    """a producing output is accepted only if its VERDICT lines are exactly ['VERDICT VALID'], by equality; a variant
    such as 'VERDICT VALID-PRECERT' or 'VERDICT VALID-STUB', or a second VERDICT line, refuses it."""
    return [ln for ln in lines if ln.startswith('VERDICT')] == ['VERDICT VALID']


def marked_precert(rec):
    """a record whose FORMAT, RECORD, END or any CLAIM* key marks it PRECERT or STUB is refused. True if marked."""
    return any(('PRECERT' in v.upper() or 'STUB' in v.upper()) for k, v in rec.items()
               if k in ('FORMAT', 'RECORD', 'END') or k.startswith('CLAIM'))


def s4u_read_port(text):
    """the port's reader of format S4U_KV_v1 (S3): the text split at newlines; a line starting with # is a comment and a blank line
    carries nothing; every other line is KEY = value with KEY of [A-Z][A-Z0-9_]*, cut at its first ' = ', the value kept as it stands;
    any other line or a repeated KEY is an error. It shares no code with the reference parser (S4U_REF), which C-FMT holds it against."""
    rec = {}
    for no, ln in enumerate(text.split('\n'), 1):
        if ln.startswith('#') or ln.strip() == '':
            continue
        key, sep, val = ln.partition(' = ')
        if sep != ' = ' or re.fullmatch(r'[A-Z][A-Z0-9_]*', key) is None or key in rec:
            raise ValueError('S4U_KV_v1, port reader: line %d is not a new KEY = value' % no)
        rec[key] = val
    return rec


T_FIELDS_NEED = ('jlo', 'jhi', 'At_lo', 'Vt_hi', 'Ot_hi', 'Xta_lo', 'Xtb_lo', 'Pt_hi', 'dtx_hi')   # read by name; Aa_lo optional


def bound_ok(name, sha, otext):
    """rule V2 for a producing output (EXPORT_READER's binding, here for pk15's records): its VERDICT lines are exactly
    ['VERDICT VALID'] and exactly one 'EXPORT <path> sha256 <hex> ...' line has the record's base name as <path>'s, with <hex> its sha256."""
    lines = otext.split('\n')
    hits = [h for h in (ln.split() for ln in lines if ln.startswith('EXPORT ')) if len(h) >= 4 and h[2] == 'sha256'
            and os.path.basename(h[1]) == name]
    return verdict_lines_ok(lines) and len(hits) == 1 and hits[0][3] == sha


def t_read(rec, grid, R, aa):
    """the t inputs from a parsed EXPORT_P2_TPROV_v1 record (pk15's kt_p2_assembly export; the Q1): ({(N, i): dict(At, Vt, Ot, Pt,
    Xta, Xtb, Aa)}, problems). Header: RECORD and END EXPORT_P2_TPROV_v1, FORMAT and EXPORT_STATUS the mode's (R: S4U_KV_v1 and
    CERTIFIED, or S4U_KV_v1 MOCK and MOCK), RUN_VERDICT VALID, FIELDS naming every field of T_FIELDS_NEED once (read by name), PRECERT or
    STUB refused; a CERTIFIED record must carry T_CERT_REQUIRE's keys and values. C-GRID: every row
    present with jlo, jhi string for string as the grid. C-FLIP, a declaration check (pk15's XTB_SOURCE = FLIP_OF_XTA
    ): the header declares FLIP_OF_XTA and every Xtb_lo equals its Xta_lo string for string. SIGN: A_t, A_a and X_ta certainly
    > 0. A_a is the record's Aa_lo when FIELDS names it, else aa[N] (S9(b)'s FLOAT stand-in, J-constant). v1_1 P-3: when FIELDS names
    ce_lo and ce_hi (pk15's route B), each row's c_e ball (ce_lo <= ce_hi) is kept as 'ce' for provide_bh."""
    bad, T = [], {}
    fields = rec.get('FIELDS', '').split(' ')
    idx = {f: k for k, f in enumerate(fields)}
    if (rec.get('RECORD') != R['record'] or rec.get('END') != R['record'] or rec.get('FORMAT') != R['fmt']
            or rec.get('EXPORT_STATUS') != R['status'] or rec.get('RUN_VERDICT') != 'VALID' or fields[:2] != ['jlo', 'jhi']
            or len(idx) != len(fields) or any(f not in idx for f in T_FIELDS_NEED)):
        bad.append('header')
        return T, bad
    if marked_precert(rec) or 'PRECERT' in rec.get('TAG', '').upper() or 'STUB' in rec.get('TAG', '').upper():
        bad.append('marked PRECERT or STUB')
    if rec.get('EXPORT_STATUS') == 'CERTIFIED' or rec.get('TAG', '').startswith('CERTIFIED'):
        bad += ['certified requirement %s' % k for k, v in T_CERT_REQUIRE.items() if rec.get(k) != v]
        if not float_in_empty(rec.get('FLOAT_IN')):                       # the rule: no FLOAT input under a CERTIFIED status
            bad.append('certified requirement FLOAT_IN empty')
        bad += cert_header_bad(rec)                                       # v1_3: OPEN_CONDITIONS none, J_UNIFORMITY PER-PIECE
    if rec.get('XTB_SOURCE') != 'FLIP_OF_XTA':
        bad.append('C-FLIP declaration XTB_SOURCE %r' % rec.get('XTB_SOURCE'))
    for N in (4, 3):
        if rec.get('N%d_PIECES' % N) != str(len(grid)):
            bad.append('N%d_PIECES' % N)
        for i, (jlo, jhi) in enumerate(grid):
            v = rec.get('N%d_P%04d' % (N, i), '').split(' ')
            if len(v) != len(fields) or v[0] != jlo or v[1] != jhi:
                bad.append('C-GRID N%d_P%04d' % (N, i))
                continue
            At, Vt, Ot, Pt, Xta, Xtb, dtx = (dec_iv(v[idx[f]]) for f in ('At_lo', 'Vt_hi', 'Ot_hi', 'Pt_hi', 'Xta_lo', 'Xtb_lo', 'dtx_hi'))
            Aa = dec_iv(v[idx['Aa_lo']]) if 'Aa_lo' in idx else aa[N]
            if v[idx['Xtb_lo']] != v[idx['Xta_lo']]:
                bad.append('C-FLIP N%d_P%04d' % (N, i))
            if not ((At > 0) is True and (Aa > 0) is True and (Xta > 0) is True):
                bad.append('SIGN N%d_P%04d' % (N, i))
            T[(N, i)] = dict(At=pt(At.a), Vt=pt(Vt.b), Ot=pt(Ot.b), Pt=pt(Pt.b), Xta=pt(Xta.a), Xtb=pt(Xtb.a), Aa=pt(Aa.a), dtx=pt(dtx.b))
            if 'ce_lo' in idx and 'ce_hi' in idx:                  # v1_1 P-3: c_e's ball for beta_H (pk15's route B)
                ce = (pt(dec_iv(v[idx['ce_lo']]).a), pt(dec_iv(v[idx['ce_hi']]).b))
                if not ((ce[0] <= ce[1]) is True):
                    bad.append('CE N%d_P%04d' % (N, i))
                T[(N, i)]['ce'] = ce
    return T, bad


JOINT_CLASSES = (('D3', 3), ('D4', 2), ('D4M', 2))   # (class, w_X): D3 (t_i, bb_i+-1), D4 (t_i, b_i), D4M (t_i, b_i+1); flip images by symmetry


JOINT_FIELDS = 'jlo jhi Cov_inf_lo pX_hi normX_hi E2_hi'          # the six-column layout (kt_p2_assembly up to v1_34; the mocks)


JOINT_FIELDS_ROUTE = JOINT_FIELDS + ' ROUTE'                      # v1_3 (the (b)): kt_p2_assembly_v1_35's layout, NOTE 32d3e069 sect. 1


ROUTE_ADMISSIBLE = dict(SINGLE=('D3', 'D4', 'D4M'), DOUBLE=('D4', 'D4M'), CS=('D3',))   # The review point (1f060903); NOTE 32d3e069 sect. 1


def joint_grid():
    """P2-14: the piece grid as strings, [(jlo, jhi)] in piece order, from v2_2's pinned export (V22_EXPORT, full sha256 of the bytes read):
    fields 1 and 2 of its N4 piece rows (the grid is the same for both N)."""
    with open(os.path.join(CODEDIR, V22_EXPORT[0]), 'rb') as fh:
        raw = fh.read()
    if sha_bytes(raw) != V22_EXPORT[1]:
        raise RuntimeError('P2-14: v2_2\'s export differs from its pin')
    rec = s4u_read_port(raw.decode('utf-8'))
    n = int(rec['N4_PIECES'])
    return [tuple(rec['N4_P%04d' % i].split(' ')[:2]) for i in range(n)]


JOINT_CERT_REQUIRE = dict(VACUUM_CORRECTION='S3_LEMMA_E', CENTRING='DOUBLE_TRICK_MEAN_BALLS',
                          NORMX_BOUND='MIN_OPERATOR_BOX_PLUS_SCHUR_TAIL_HS_INV')


T_CERT_REQUIRE = dict(VT_FORM='GRAM_PLUS_Q4', PT_FORM='JOINT_GRAM')


def float_in_empty(v):
    """the status rule for pk15's exports: a CERTIFIED record carries FLOAT_IN = none, exactly (pk15's empty form, what its
    export_status writes for all-empty lists; an allow-list). Anything else, an absent FLOAT_IN included, is not empty: such
    a record reads CERTIFIED_GIVEN_FLOAT_IN with '<record>: <tokens>' entries and is refused as certified."""
    return v == 'none'


J_UNIF_CERT = ('UNIFORM-J PER-PIECE (M4): every row holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf '
               '(t = 0)')   # v1_3: pk15's exact J_UNIFORMITY value for its certified t, joint and means exports after M4


def cert_header_bad(rec):
    """v1_3 (P-2): two more header rules for a CERTIFIED t or joint export of pk15's: OPEN_CONDITIONS = none, exactly; and
    J_UNIFORMITY = J_UNIF_CERT, exactly (pk15's PER-PIECE value after M4; 'UNIFORM-J ASSUMED (M4)', NOTE_M4_SCOPE_v1, means the J = 300
    values on every piece are not yet certified for every J >= 300, and an absent key is refused too). Returns the failures, as
    'certified requirement ...' strings."""
    bad = [] if rec.get('OPEN_CONDITIONS') == 'none' else ['certified requirement OPEN_CONDITIONS none']
    return bad + ([] if rec.get('J_UNIFORMITY') == J_UNIF_CERT else ['certified requirement J_UNIFORMITY PER-PIECE'])


def joint_read(rec, grid):
    """P2-14: the joint inputs from a parsed record: ({(cls, N, i): dict(Cov, pX, normX, E2, route)}, problems). C-GRID: every row present
    with jlo, jhi string for string as the grid; C-SRC-J: pX_hi^2 >= E2_hi - Cov_inf_lo^2 where Cov_inf_lo > 0 (certain comparisons on
    exact decimals); the header's CLASSES, WX_* and RUN_VERDICT = VALID (T48 for KV records) as agreed; PRECERT or STUB refused; a record
    whose TAG reads CERTIFIED must carry JOINT_CERT_REQUIRE's keys and values. v1_3 (the (b), NOTE 32d3e069):
    FIELDS selects the layout, JOINT_FIELDS (six tokens per row, route None) or JOINT_FIELDS_ROUTE (seven, the 7th the route); C-ROUTE: a
    route must be admissible for its class (ROUTE_ADMISSIBLE); a CERTIFIED record must use the ROUTE layout."""
    bad, J = [], {}
    want = dict(CLASSES=' '.join(c for c, _ in JOINT_CLASSES), RUN_VERDICT='VALID', **{'WX_%s' % c: str(w) for c, w in JOINT_CLASSES})
    bad += ['header %s' % k for k, v in want.items() if rec.get(k) != v]
    ncol = {JOINT_FIELDS: 6, JOINT_FIELDS_ROUTE: 7}.get(rec.get('FIELDS'))
    if ncol is None:
        bad.append('header FIELDS')
    if marked_precert(rec) or 'PRECERT' in rec.get('TAG', '').upper() or 'STUB' in rec.get('TAG', '').upper():
        bad.append('marked PRECERT or STUB')
    if rec.get('EXPORT_STATUS') == 'CERTIFIED' or rec.get('TAG', '').startswith('CERTIFIED'):
        bad += ['certified requirement %s' % k for k, v in JOINT_CERT_REQUIRE.items() if rec.get(k) != v]
        if ncol != 7:                                                     # v1_3: certified joint inputs carry their routes
            bad.append('certified requirement FIELDS with ROUTE')
        if not float_in_empty(rec.get('FLOAT_IN')):                       # the rule: no FLOAT input under a CERTIFIED status
            bad.append('certified requirement FLOAT_IN empty')
        bad += cert_header_bad(rec)                                       # v1_3: OPEN_CONDITIONS none, J_UNIFORMITY PER-PIECE
    for cls, _ in JOINT_CLASSES:
        for N in (4, 3):
            if rec.get('N%d_%s_PIECES' % (N, cls)) != str(len(grid)):
                bad.append('N%d_%s_PIECES' % (N, cls))
            for i, (jlo, jhi) in enumerate(grid):
                v = rec.get('N%d_%s_P%04d' % (N, cls, i), '').split(' ')
                if ncol is None or len(v) != ncol or v[0] != jlo or v[1] != jhi:
                    bad.append('C-GRID N%d_%s_P%04d' % (N, cls, i))
                    continue
                route = v[6] if ncol == 7 else None
                if ncol == 7 and cls not in ROUTE_ADMISSIBLE.get(route, ()):
                    bad.append('C-ROUTE N%d_%s_P%04d %s' % (N, cls, i, route))
                cov, px, nx, e2 = dec_iv(v[2]), dec_iv(v[3]), dec_iv(v[4]), dec_iv(v[5])
                if (cov > 0) is not True:                                   # the C-S check needs Cov_inf_lo > 0
                    bad.append('C-SRC-J Cov_inf_lo not > 0 N%d_%s_P%04d' % (N, cls, i))
                elif (px * px >= e2 - cov * cov) is not True:
                    bad.append('C-SRC-J N%d_%s_P%04d' % (N, cls, i))
                J[(cls, N, i)] = dict(Cov=pt(cov.a), pX=pt(px.b), normX=pt(nx.b), E2=pt(e2.b), route=route)
    return J, bad


def joint_route_layout(rec):
    """v1_3: the record in the ROUTE layout, as the base of the certified-header control and plants and of PLANT-ROUTE: a six-column
    record gets FIELDS = JOINT_FIELDS_ROUTE and the route SINGLE (admissible for every class) appended to every row; a ROUTE-layout record
    comes back unchanged."""
    if rec.get('FIELDS') != JOINT_FIELDS:
        return rec
    rows = re.compile(r'N[34]_(%s)_P[0-9]{4}' % '|'.join(c for c, _ in JOINT_CLASSES))
    return dict({k: (v + ' SINGLE' if rows.fullmatch(k) else v) for k, v in rec.items()}, FIELDS=JOINT_FIELDS_ROUTE)


