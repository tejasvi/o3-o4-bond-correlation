#!/usr/bin/env python3
"""kt_s9h_crudex_v1.py (pk25, code/pk25/asm/; G5 C11, the P0_LOG rows 4443, 4444, 4446): MR_CRUDEX's split rows e_hi(d), d = 1, 2, 3, on every piece of
R4's grid, from pk25's certified MR_INPUT_KV_v4 records mr/v4/MR_SPECTRAL.kv and mr/v4/MR_INSERT.kv alone (pk25/C11_DESIGN_v1.md;
pk24/MIDROW_G6_SPEC_v1_6_2.md sect. 0d item 1 and 4.2). For a crude h end at end exponent d:
  E(d) = a_x(h, d) - v_x = H1(d) - H2(d),  H1(d) = c_x(d) m_xx + c_y(d) m_xy + O(d),  H2(d) = beta(d) c_x(d),  c_a(d) = s_a^(d+1) c_a(-1),
  beta(d) = <v, eps(d)> = s_x^(d+1) v_x c_x(-1) + s_y^(d+1) v_y c_y(-1) + <P_e S v, P_e eps(d - 1)>   (spectral split; eps(d) = S eps(d - 1)),
  O(d) = <P_e M_c u_x, P_e eps(d)> = <P_e B^w u_x, P_e eps(d - 1)> / s_x   (B^w = S M_c S),
  |P_e eps(d - 1)| <= tau4^d |P_e eps(-1)|,  |P_e eps(-1)|^2 <= R_w^2 - c_x(-1)^2 - c_y(-1)^2   (Parseval: eps(-1) is flip-even, orthogonal to u),
so |E(d)| <= e_hi(d) := |c_x(d)| |m_xx| + |c_y(d)| |m_xy| + PeBwu_x tau4^d pe / s_x + (|beta_spec(d)| + Pevw tau4^d pe) |c_x(d)|, pe the
Parseval bound, beta_spec the first two terms of beta(d); every input an enclosure over the whole piece (the last piece's to t = 0). The split
keeps the halves apart (no t^0 cancellation is used). The P_e overlap takes the window form (Lemma 3's plain bound, the row 4444); with no
x(x)y split, R_xy does not enter (the XY_ROUTE header line says so; a factored MR_CRUDEX for M2 is a later record).
MODE dry or cert (cert only under the approval naming this file's sha8): the record to mr/v4/MR_CRUDEX.kv; a dry run's to asm/dry_<TAG>/. Usage:
kt_s9h_crudex_v1.py dry|cert TAG"""
import ast
import hashlib
import os
import re
import sys
import time
from decimal import Decimal, Context, ROUND_CEILING
from fractions import Fraction

MODES = ('dry', 'cert')
if len(sys.argv) != 3 or sys.argv[1] not in MODES or not re.fullmatch(r'[A-Za-z0-9_]{1,40}', sys.argv[2]):
    print('usage: kt_s9h_crudex_v1.py dry|cert TAG')
    sys.exit(2)
MODE, TAG = sys.argv[1], sys.argv[2]
SELF = os.path.abspath(__file__)
LABEL = os.path.splitext(os.path.basename(SELF))[0]
W18 = '/mnt/g2/release/root/code'
OWN = W18 + '/pk25'
ASM = OWN + '/asm'
OUT_DIR = ASM + '/out'
OUT_PATH = os.path.join(OUT_DIR, 'out_%s_%s_%s.out' % (LABEL, MODE, TAG))
SPEC4 = OWN + '/mr/v4/MR_SPECTRAL.kv'
INS4 = OWN + '/mr/v4/MR_INSERT.kv'
M1ENG = W18 + '/pk24/mr_engine/kt_mr_assembly_v1_8_4.py'
PINS = {
    '/mnt/g2/release/root/code/pk25/mr/v4/MR_SPECTRAL.kv': '4a609ccf717c0aedd9504ee4db47e7c98a679bc25df2ca2a187b415011470937',
    '/mnt/g2/release/root/code/pk25/mr/v4/MR_INSERT.kv': 'e372a2a674132e4f28203b814843c582004983243a643ccb734753ad3f5d9cde',
    '/mnt/g2/release/root/code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py': '28a340e7b38b0f37a40b4eb2df4c0f03b58dedf0b80755a659c0157c1094a56c',
}
DMAX = 3
if not (os.path.isdir(OUT_DIR) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUT_DIR)):
    print('output path check failed')
    sys.exit(2)
FH = open(OUT_PATH, 'x')


def out(line):
    FH.write(line + '\n')
    FH.flush()


class Refused(Exception):
    pass


def sha_file(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def gate(fails, name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


def plant(nofire, name, fn):
    """a must-fire plant: fn must raise Refused."""
    try:
        fn()
    except Refused as e:
        out('%s: refused (%s) -> FIRES' % (name, e))
        return
    except Exception as e:
        out('%s: raised %r instead of a refusal -> DOES NOT FIRE' % (name, e))
        nofire.append(name)
        return
    out('%s: accepted -> DOES NOT FIRE' % name)
    nofire.append(name)


def read_kv(path, pins=None):
    """a pinned MR_INPUT_KV record: (header dict, FIELDS list, [(key, values)]) by the M1 engine's kv_read rules (header keys until FIELDS,
    no repeated key, '=' on every line, unique row keys, one value per field)."""
    pins = PINS if pins is None else pins
    if pins.get(path) is None or sha_file(path) != pins[path]:
        raise Refused('C-HASH: %s does not match its pin' % os.path.relpath(path, W18))
    head, flds, rows, seen = {}, None, [], set()
    for ln in open(path).read().splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        if '=' not in ln:
            raise Refused('C-REC: %s has a line without "="' % os.path.basename(path))
        k, v = [x.strip() for x in ln.split('=', 1)]
        if k == 'FIELDS':
            flds = v.split()
        elif flds is None:
            if k in head:
                raise Refused('C-REC: %s repeats the header key %s' % (os.path.basename(path), k))
            head[k] = v
        else:
            vals = v.split()
            if k in seen or len(vals) != len(flds):
                raise Refused('C-REC: %s row %s repeated or with %d values for %d fields' % (os.path.basename(path), k, len(vals), len(flds)))
            seen.add(k)
            rows.append((k, vals))
    return head, flds, rows


def m1_texts(pins=None):
    """the M1 engine's texts read by ast from its pinned file: FIELDS (MR_SPECTRAL, MR_INSERT, MR_CRUDEX), the v4 MR_INSERT suffix, E_DEF
    (the split E_DEFINITION) and ORIENT."""
    pins = PINS if pins is None else pins
    if pins.get(M1ENG) is None or sha_file(M1ENG) != pins[M1ENG]:
        raise Refused('C-M1-TEXTS: the M1 engine does not match its pin')
    got, suffix = {}, None
    for node in ast.parse(open(M1ENG).read()).body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
            continue
        nm = node.targets[0].id
        if nm in ('FIELDS', 'E_DEF', 'ORIENT'):
            got[nm] = ast.literal_eval(node.value)
        elif nm == 'FIELDS4':
            for kw in getattr(node.value, 'keywords', []):
                if kw.arg == 'MR_INSERT' and isinstance(kw.value, ast.BinOp) and isinstance(kw.value.right, ast.Constant):
                    suffix = kw.value.right.value
    if sorted(got) != ['E_DEF', 'FIELDS', 'ORIENT'] or suffix is None:
        raise Refused('C-M1-TEXTS: FIELDS, FIELDS4, E_DEF or ORIENT not found as expected')
    return dict(spec=got['FIELDS']['MR_SPECTRAL'], ins=got['FIELDS']['MR_INSERT'] + suffix, crx=got['FIELDS']['MR_CRUDEX'],
                edef=got['E_DEF'], orient=got['ORIENT'])


def check_rec(head, flds, want_fields, record, TX):
    """C-REC: a certified, VALID MR_INPUT_KV_v4 record of pk25 with the M1 engine's FIELDS and ORIENTATION."""
    ok = (head.get('FORMAT') == 'MR_INPUT_KV_v4' and head.get('RECORD') == record and head.get('STATUS') == 'CERTIFIED' and
          head.get('EXPORT_STATUS') == 'CERTIFIED' and head.get('RUN_VERDICT') == 'VALID' and head.get('PRODUCER', '').split()[:1] == ['pk25'] and
          head.get('ORIENTATION') == TX['orient'] and flds == want_fields.split() and head.get('TRIAL_SET', '').strip() != '')
    if not ok:
        raise Refused('C-REC: %s is not a certified VALID pk25 MR_INPUT_KV_v4 record with the engine\'s FIELDS' % record)
    return True


def iv(lo, hi):
    """an arb ball holding the decimal interval [lo, hi] (decimal strings, rounded outward by arb)."""
    a, b = arb(lo), arb(hi)
    if not (a.lower() <= b.upper()):
        raise Refused('C-REC: a field with lo above hi')
    return a.lower().union(b.upper())


def dec_hi(x):
    """an arb's upper end as a decimal string rounded up (17 significant digits)."""
    u = x.upper()
    m, e = u.mid().man_exp()
    f = Fraction(int(m)) * (Fraction(2) ** int(e))
    c = Context(prec=17, rounding=ROUND_CEILING)
    return str(c.divide(Decimal(f.numerator), Decimal(f.denominator)))


def crudex_rows(spec, ins, plant=None):
    """the split rows: for every MR_SPECTRAL piece and d = 1..DMAX, e_hi(d) by the module docstring's bound; returns ([(key, [jlo, jhi,
    e_hi])], per-row INFO dict). plant: 'PE' (R_w set to c_x(-1)'s lower end; C-PE must refuse), 'GRID' (the first MR_INSERT h row
    dropped; C-GRID must refuse)."""
    sp = dict((k, v) for k, v in spec[2])
    ix_s = dict((f, i) for i, f in enumerate(spec[1]))
    ih = dict((k, v) for k, v in ins[2] if k.endswith('_h'))
    if plant == 'GRID':
        ih.pop(sorted(ih)[0])
    ix_i = dict((f, i) for i, f in enumerate(ins[1]))
    rows, info = [], {}
    for key, v in spec[2]:
        h = ih.get(key + '_h')
        if h is None or (h[ix_i['jlo']], h[ix_i['jhi']]) != (v[ix_s['jlo']], v[ix_s['jhi']]):
            raise Refused('C-GRID: piece %s has no MR_INSERT h row with its jlo, jhi' % key)
        g = lambda f: iv(v[ix_s[f + '_lo']], v[ix_s[f + '_hi']])
        G = lambda f: iv(h[ix_i[f + '_lo']], h[ix_i[f + '_hi']])
        sx, sy, cx, cy = g('sx'), g('sy'), g('cxm1'), g('cym1')
        tau, rw = arb(v[ix_s['tau_hi']]).upper(), arb(v[ix_s['Rw_hi']]).upper()
        if plant == 'PE':
            rw = cx.lower()
        vx, vy, mxx, mxy = G('vx'), G('vy'), G('mxx'), G('mxy')
        pevw, pebw = arb(h[ix_i['Pevw_hi']]).upper(), arb(h[ix_i['PeBwux_hi']]).upper()
        cxl = cx.lower() if cx.lower() > 0 else (-cx.upper() if cx.upper() < 0 else arb(0))
        cyl = cy.lower() if cy.lower() > 0 else (-cy.upper() if cy.upper() < 0 else arb(0))
        rad = rw * rw - cxl * cxl - cyl * cyl
        if not (rad > 0):
            raise Refused('C-PE: R_w^2 - c_x(-1)^2 - c_y(-1)^2 is not certainly positive at %s' % key)
        pe = rad.sqrt().upper()
        if not (sx.lower() > 0 and sy.lower() > 0):
            raise Refused('C-S: s_x or s_y is not certainly positive at %s' % key)
        for d in range(1, DMAX + 1):
            cxd, cyd = sx ** (d + 1) * cx, sy ** (d + 1) * cy
            bspec = sx ** (d + 1) * vx * cx + sy ** (d + 1) * vy * cy
            win = (tau ** d * pe).upper()
            h2 = ((abs(bspec).upper() + pevw * win) * abs(cxd).upper()).upper()
            h1 = (abs(cxd).upper() * abs(mxx).upper() + abs(cyd).upper() * abs(mxy).upper() + pebw * win / sx.lower()).upper()
            e = (h1 + h2).upper()
            if not (e > 0 and e < arb(1)):
                raise Refused('C-POS: e_hi(%d) at %s is not in (0, 1)' % (d, key))
            rows.append(('%s_h%d' % (key, d), [v[ix_s['jlo']], v[ix_s['jhi']], dec_hi(e)]))
            info[(key, d)] = dict(e=e, h1=h1, h2=h2, half=(abs(vy).upper() * abs(cyd).upper() * abs(cxd).upper()).upper(),
                                  xrow=(abs(cxd).upper() * abs(mxx).upper() + abs(cyd).upper() * abs(mxy).upper()).upper(), ow=(pebw * win / sx.lower()).upper())
    return rows, info


def rec_text(TX, rows, trial_set, source, edef=None):
    """the MR_CRUDEX v4 split record text."""
    cert = MODE == 'cert'
    head = ['# MR_CRUDEX (pk25, %s %s): written by %s' % (LABEL, MODE, LABEL),
            'FORMAT = MR_INPUT_KV_v4', 'RECORD = MR_CRUDEX', 'PRODUCER = pk25 %s' % LABEL, 'CODE = pk25/asm/%s.py:%s' % (LABEL, sha_file(SELF)),
            'STATUS = %s' % ('CERTIFIED' if cert else 'DRY'), 'EXPORT_STATUS = %s' % ('CERTIFIED' if cert else 'DRY'), 'RUN_VERDICT = VALID',
            'SOURCE = %s' % source,
            'J_UNIFORMITY = PER-PIECE: every row holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf (t = 0)',
            'ORIENTATION = %s' % TX['orient'], 'TRIAL_SET = %s' % trial_set, 'E_DEFINITION = %s' % (TX['edef'] if edef is None else edef),
            'CRUDEX_FORM = split',
            'XY_ROUTE = the P_e overlap by the window form PeBwu_x tau4^d |P_e eps(-1)| / s_x (Lemma 3\'s plain bound, the row 4444); no x(x)y '
            'split, so R_xy does not enter; m_xx, m_xy from MR_INSERT (O(t), law-based Ritz problem)',
            'FIELDS = %s' % TX['crx']]
    return '\n'.join(head + ['%s = %s' % (k, ' '.join(v)) for k, v in rows]) + '\n'


def readback(text, TX, rows, tamper=None):
    """C-WRITE: the text by the M1 engine's rules: FORMAT, RECORD, ORIENTATION, PRODUCER pk25, E_DEFINITION equal to the engine's E_DEF,
    CRUDEX_FORM split, FIELDS, rows equal to memory with unique keys, e_hi finite and > 0, and the items _h1.._h3 on every piece."""
    if tamper == 'ROW':
        k0, v0 = rows[0]
        text = text.replace('%s = %s' % (k0, ' '.join(v0)), '%s = %s' % (k0, ' '.join(v0[:2] + ['-' + v0[2]])), 1)
    head, got, flds = {}, [], None
    for ln in text.splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        if '=' not in ln:
            raise Refused('C-WRITE: a line without "="')
        k, v = [x.strip() for x in ln.split('=', 1)]
        if k == 'FIELDS':
            flds = v.split()
        elif flds is None:
            if k in head:
                raise Refused('C-WRITE: repeated header key %s' % k)
            head[k] = v
        else:
            got.append((k, v.split()))
    if (head.get('FORMAT'), head.get('RECORD'), head.get('ORIENTATION'), head.get('CRUDEX_FORM')) != ('MR_INPUT_KV_v4', 'MR_CRUDEX', TX['orient'], 'split'):
        raise Refused('C-WRITE: FORMAT, RECORD, ORIENTATION or CRUDEX_FORM')
    if head.get('PRODUCER', '').split()[:1] != ['pk25'] or head.get('E_DEFINITION') != TX['edef']:
        raise Refused('C-WRITE: PRODUCER or E_DEFINITION')
    if flds != TX['crx'].split() or got != [(k, list(v)) for k, v in rows] or len(set(k for k, _ in got)) != len(got):
        raise Refused('C-WRITE: FIELDS or rows differ from memory')
    pieces = {}
    for k, v in got:
        base, it = k.rsplit('_', 1)
        if not re.fullmatch(r'-?[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?', v[2]) or not (Decimal(v[2]) > 0 and Decimal(v[2]).is_finite()):
            raise Refused('C-WRITE: row %s has e_hi = %s' % (k, v[2]))
        pieces.setdefault(base, set()).add(it)
    if any(s != set('h%d' % d for d in range(1, DMAX + 1)) for s in pieces.values()):
        raise Refused('C-WRITE: a piece without its items h1..h%d' % DMAX)
    return len(got)


def main():
    t0 = time.time()
    fails, nofire, EXEC = [], [], []

    def run_plant(name, fn):
        EXEC.append(name)
        plant(nofire, name, fn)

    def flag(fn):
        try:
            fn()
            return True
        except Refused as e:
            out('  refused: %s' % e)
            return False
    out('%s sha256 %s MODE=%s TAG=%s (MR_CRUDEX split rows from the certified v4 MR_SPECTRAL and MR_INSERT; %s)' % (
        LABEL, sha_file(SELF), MODE, TAG, 'CERTIFIED record to mr/v4' if MODE == 'cert' else 'DRY record to asm/dry_%s' % TAG))
    bad = ['%s %s' % (os.path.basename(p), sha_file(p)[:8]) for p in sorted(PINS) if sha_file(p) != PINS[p]]
    out('C-HASH %s (%d pinned files)%s' % ('PASS' if not bad else 'FAIL', len(PINS), (': ' + '; '.join(bad)) if bad else ''))
    if bad:
        out('VERDICT INVALID (C-HASH)')
        return 2
    run_plant('PLANT-PIN', lambda: read_kv(SPEC4, dict(PINS, **{SPEC4: '0' * 64})))
    try:
        TX = m1_texts()
        SPEC, INS = read_kv(SPEC4), read_kv(INS4)
        check_rec(SPEC[0], SPEC[1], TX['spec'], 'MR_SPECTRAL', TX)
        check_rec(INS[0], INS[1], TX['ins'], 'MR_INSERT', TX)
        ok = SPEC[0]['TRIAL_SET'] == INS[0]['TRIAL_SET']
        if not ok:
            out('  refused: the two records name different TRIAL_SET lines')
    except Refused as e:
        out('  refused: %s' % e)
        ok = False
    out('C-REC: %s (%s) and %s (%s): certified VALID MR_INPUT_KV_v4 records of pk25 with the M1 engine\'s FIELDS (%s), one TRIAL_SET -> %s' % (
        os.path.relpath(SPEC4, W18), PINS[SPEC4][:8], os.path.relpath(INS4, W18), PINS[INS4][:8], PINS[M1ENG][:8], gate(fails, 'C-REC', ok)))
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2
    try:
        rows, info = crudex_rows(SPEC, INS)
        ok = True
    except Refused as e:
        out('  refused: %s' % e)
        rows, info, ok = [], {}, False
    npc = dict((N, sum(1 for k, _v in SPEC[2] if k.startswith('N%d_' % N))) for N in (4, 3))
    out('C-ROWS: e_hi(d), d = 1..%d, on every piece (N4 %d, N3 %d pieces; C-GRID, C-PE, C-S, C-POS on each) -> %s' % (
        DMAX, npc[4], npc[3], gate(fails, 'C-ROWS', ok and len(rows) == DMAX * (npc[4] + npc[3]))))
    run_plant('PLANT-PE', lambda: crudex_rows(SPEC, INS, plant='PE'))
    run_plant('PLANT-GRID', lambda: crudex_rows(SPEC, INS, plant='GRID'))
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2
    for N in (4, 3):
        keys = [k for k, _v in SPEC[2] if k.startswith('N%d_' % N)]
        for lab, k in (('first', keys[0]), ('last', keys[-1])):
            out('INFO N=%d %s piece %s: %s' % (N, lab, k, '; '.join(
                'd=%d e_hi %s (half %s, x-row %s, window O(d) %s, |H2| %s)' % (d, dec_hi(info[(k, d)]['e']), dec_hi(info[(k, d)]['half']),
                                                                       dec_hi(info[(k, d)]['xrow']), dec_hi(info[(k, d)]['ow']), dec_hi(info[(k, d)]['h2']))
                for d in range(1, DMAX + 1))))
        for d in range(1, DMAX + 1):
            m = max((float(info[(k, d)]['e']), k) for k in keys)
            out('INFO N=%d d=%d: e_hi largest %.4e (piece %s), on the last piece %.4e' % (N, d, m[0], m[1], float(info[(keys[-1], d)]['e'])))
    source = 'mr/v4 MR_SPECTRAL %s, mr/v4 MR_INSERT %s (pk25, certified); the M1 engine %s for FIELDS and E_DEF' % (
        PINS[SPEC4][:8], PINS[INS4][:8], PINS[M1ENG][:8])
    text = rec_text(TX, rows, SPEC[0]['TRIAL_SET'], source)
    out('C-WRITE: the MR_CRUDEX v4 split text read back by the M1 engine\'s rules (%d rows) -> %s' % (
        len(rows), gate(fails, 'C-WRITE', flag(lambda: readback(text, TX, rows)))))
    run_plant('PLANT-WRITE', lambda: readback(text, TX, rows, tamper='ROW'))
    run_plant('PLANT-EDEF', lambda: readback(rec_text(TX, rows, SPEC[0]['TRIAL_SET'], source, edef='e_hi >= a_x(h, d) - v_x'), TX, rows))
    unrun = [p for p in PLANT_NAMES if p not in EXEC] + [p for p in EXEC if p not in PLANT_NAMES or EXEC.count(p) != 1]
    out('PLANTS: %d of %d must-fire plants ran (not run or repeated: %s); not firing: %s' % (
        len(set(EXEC)), len(PLANT_NAMES), ' '.join(unrun) if unrun else 'none', ' '.join(nofire) if nofire else 'none'))
    if nofire or unrun:
        fails.append('PLANTS')
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2
    recdir = OWN + '/mr/v4' if MODE == 'cert' else os.path.join(ASM, 'dry_%s' % TAG)
    if MODE == 'dry':
        os.mkdir(recdir)
    if not os.path.isdir(recdir) or os.path.realpath(recdir) not in (os.path.realpath(OWN + '/mr/v4'), os.path.realpath(os.path.join(ASM, 'dry_%s' % TAG))):
        out('VERDICT INVALID (record folder)')
        return 2
    path = os.path.join(recdir, 'MR_CRUDEX.kv')
    with open(path, 'x') as fh:
        fh.write(text)
    if sha_file(path) != hashlib.sha256(text.encode()).hexdigest():
        out('VERDICT INVALID (the written MR_CRUDEX differs from memory)')
        return 2
    out('RECORD %s sha256 %s rows %d' % (os.path.relpath(path, W18), sha_file(path), len(rows)))
    out('RUN wall %.1f s' % (time.time() - t0))
    out('VERDICT VALID')
    return 0


PLANT_NAMES = ('PLANT-PIN', 'PLANT-PE', 'PLANT-GRID', 'PLANT-WRITE', 'PLANT-EDEF')


if __name__ == '__main__':
    from flint import arb, ctx
    ctx.prec = 256
    try:
        rc = main()
    except Refused as e:
        out('STOP Refused: %s' % e)
        out('VERDICT INVALID (refused)')
        rc = 2
    FH.close()
    sys.exit(rc)
