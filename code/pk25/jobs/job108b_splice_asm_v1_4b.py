#!/usr/bin/env python3
"""job108b (pk25, C6a v3; job108 with the law block asm_v1_4b_law.py.txt, whose isect keeps exact interval ends, the P0_LOG row 4363): writes asm/src/kt_s9h_asm_v1_4.py.in from asm/src/kt_s9h_asm_v1_3.py.in (frozen): the law
block asm/src/asm_v1_4_law.py.txt goes in before piece_compute, piece_compute gets src ('rec': v2's computation; 'law': law_bp, law_e2ff),
main reads the law certificates (C-LAW-READ, PLANT-LAW-PIN), checks C-ALIAS (PLANT-ALIAS), computes every piece by piece_both, runs the four
piece plants on the law path, prints the v3 width ratios, and writes the records to mr/v3; the docstring, SOURCE line and MR_LEMMAP's header
say so. Every replaced text must occur exactly once; the output is written with 'x' and parsed only after the maker fills it."""
import hashlib
import os
import sys

D = '/mnt/g2/release/root/code/pk25/asm/src/'
SRC, OUT, LAW = D + 'kt_s9h_asm_v1_3.py.in', D + 'kt_s9h_asm_v1_4b.py.in', D + 'asm_v1_4b_law.py.txt'

V3_DOC = ('Made by asm/make_kt_s9h_asm_v1_3.py from asm/src/kt_s9h_asm_v1_4b.py.in (the v3 issue).\n'
          'v3 (the P0_LOG row 4363; records in mr/v3, mr/v2 kept): every piece is computed twice, with the S9 records\' entries (entry_piece;\n'
          'v2\'s computation byte for byte) and with the law certificates (G and T from S8 D\'s g and S8 N\'s T, Dx from S8 D\'s DY, E2\'s e,b and\n'
          'FF\'s z, each by entry_law_piece at the piece\'s J_lo through pk25\'s reader fork m3_reader_s9h_v1; Iht stays the S9 record\'s, which no\n'
          'row uses), and each written field is the intersection of the two (both are certified bounds of the same quantity: the larger lower end,\n'
          'the smaller upper end; single upper bounds the smaller, single lower bounds the larger). So no v3 field is wider than v2\'s computation.\n'
          'New gates: C-LAW-READ, C-ALIAS (the law certificates\' ak inside the records\' coefficient balls for G, T, Dx and E2\'s e,b, FF\'s z),\n'
          'C-COMBINE (no empty intersection); new plants PLANT-LAW-PIN and PLANT-ALIAS; PLANT-L3-GAP, PLANT-LK-GAP, PLANT-ORIENT and PLANT-RW run\n'
          'on the law path. The v2 text follows.')

INFO_V3 = ('    for N in (4, 3):\n'
           '        wx3 = [w[0] for w in wrs[N]]\n'
           '        wsy = [w[1] for w in wrs[N]]\n'
           '        out(\'INFO V3-WIDTH N=%d: written / record-computation width, ux3 from %.3e to %.3e, s_y from %.3e to %.3e over %d pieces\' % (\n'
           '            N, min(wx3), max(wx3), min(wsy), max(wsy), len(wx3)))\n')

LAWREAD = ('\n    try:\n'
           '        IN[\'RD\'] = load_rdr()\n'
           '        IN[\'LW\'] = dict((N, load_laws_c6a(IN[\'RD\'], N)) for N in (4, 3))\n'
           '        lok = True\n'
           '    except Refused as e:\n'
           '        out(\'  refused: %s\' % e)\n'
           '        lok = False\n'
           '    out(\'C-LAW-READ: S8 D, E2, E3, FF with m3_lawcert_v1_1 and S8 N with m3_lawcert_v1_2 (N4 %s %s, N3 %s %s) through m3_reader_s9h_v1 (%s), \'\n'
           '        \'records bound to their asm outputs, trial sets as pinned -> %s\' % (\n'
           '            PINS[S8CERT[4][\'v1_1\'][0]][:8], PINS[S8CERT[4][\'v1_2\'][0]][:8], PINS[S8CERT[3][\'v1_1\'][0]][:8], PINS[S8CERT[3][\'v1_2\'][0]][:8],\n'
           '            PINS[RDR][:8], gate(fails, \'C-LAW-READ\', lok)))\n'
           '    if lok:\n'
           '        run_plant(\'PLANT-LAW-PIN\', lambda: load_laws_c6a(IN[\'RD\'], 4, dict(PINS, **{S8CERT[4][\'v1_1\'][0]: \'0\' * 64})))\n'
           '        out(\'C-ALIAS: the law certificates\\\' ak lie in the records\\\' coefficient balls for G, T, Dx (S9 records) and E2 e,0 e,1 e,3, FF z \'\n'
           '            \'(S8 records), both N -> %s\' % gate(fails, \'C-ALIAS\', flag(lambda: check_alias3(IN))))\n'
           '        run_plant(\'PLANT-ALIAS\', lambda: check_alias3(IN, tamper=True))')

CONSTS = ("\nRDR = OWN + '/m3/m3_reader_s9h_v1.py'\n"
          "M3O = CODEDIR + '/pk03/out/'\n"
          "S8REC = dict((N, dict((F, (M3O + 'm3_s8v3_%s_N%d_J300_v1_8_1.json' % (F, N), M3O + 'm3_run_v1_8_1_asmP.%d.out' % N)) for F in ('D', 'E2', 'E3', 'FF')))\n"
          "             for N in (4, 3))\n"
          "for _N in (4, 3):\n"
          "    S8REC[_N]['N'] = (M3O + 'm3_s8v3_N_N%d_J300_v1_8_2.json' % _N, M3O + 'm3_run_v1_8_2_asmN.%d.out' % _N)\n"
          "S8CERT = dict((N, {'v1_1': (M3O + 'm3_lawcert_v1_1_N%d.json' % N, M3O + 'm3_lawcert_v1_1_%d.out' % N),\n"
          "                   'v1_2': (M3O + 'm3_lawcert_v1_2_N%d.json' % N, M3O + 'm3_lawcert_v1_2_%d.out' % N)}) for N in (4, 3))")


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    if os.path.exists(OUT):
        print('STOP: %s exists' % OUT)
        return 6
    txt = open(SRC).read()
    law = open(LAW).read().rstrip('\n')
    reps = [
        ('Made by asm/make_kt_s9h_asm_v1.py from asm/src/kt_s9h_asm_v1.py.in.', V3_DOC),
        ('written to mr/v2/ (MR_SPECTRAL.kv and', 'written to mr/v3/ (MR_SPECTRAL.kv and'),
        ("RECDIR = OWN + '/mr/v2' if MODE == 'cert' else os.path.join(ASM, 'dry_%s' % TAG)",
         "RECDIR = OWN + '/mr/v3' if MODE == 'cert' else os.path.join(ASM, 'dry_%s' % TAG)"),
        ("ENDW = dict((N, CODEDIR + '/pk03/out/m3_endw_N%d_J300_v1_7.json' % N) for N in (4, 3))",
         "ENDW = dict((N, CODEDIR + '/pk03/out/m3_endw_N%d_J300_v1_7.json' % N) for N in (4, 3))" + CONSTS),
        ('def piece_compute(N, idx, jlo, jhi, IN, plant=None):', law + "\n\n\ndef piece_compute(N, idx, jlo, jhi, IN, plant=None, src='rec'):"),
        ('    negated), RW (R_w times 0.9)."""',
         "    negated), RW (R_w times 0.9). v3: src 'rec' takes the S9 records' entries and S8's E2, FF balls (v2's computation byte for byte),\n"
         "    src 'law' the law certificates (law_bp, law_e2ff).\"\"\""),
        ("    Bp = dict((k, entry_piece(IN['RE'][N][k], tb)) for k in RITZ_KEYS)",
         "    Bp = law_bp(IN, N, tb, t_ends(jlo, jhi)[1], JL) if src == 'law' else dict((k, entry_piece(IN['RE'][N][k], tb)) for k in RITZ_KEYS)"),
        ("    e = [entry_piece(IN['E2'][N]['E2']['e,%d' % b], tb) for b in REVEN]\n    z = entry_piece(IN['E2'][N]['FF']['z'], tb)",
         "    if src == 'law':\n        e, z = law_e2ff(IN, N, tb, t_ends(jlo, jhi)[1], JL)\n    else:\n"
         "        e = [entry_piece(IN['E2'][N]['E2']['e,%d' % b], tb) for b in REVEN]\n        z = entry_piece(IN['E2'][N]['FF']['z'], tb)"),
        ("    run_plant('PLANT-E2-TRIAL', lambda: load_e2ff(4, plant='TRIAL'))",
         "    run_plant('PLANT-E2-TRIAL', lambda: load_e2ff(4, plant='TRIAL'))" + LAWREAD),
        ('    perr, D1, DL, DM, cwid, l3dom = {}, {}, {}, {}, {}, {}', '    perr, D1, DL, DM, cwid, l3dom, wrs = {}, {}, {}, {}, {}, {}, {}'),
        ('                D = piece_compute(N, idx, jlo, jhi, IN)', '                D = piece_both(N, idx, jlo, jhi, IN)'),
        ("            cw[0], cw[1] = max(cw[0], float(wx.upper())), max(cw[1], float(wy.upper()))",
         "            cw[0], cw[1] = max(cw[0], float(wx.upper())), max(cw[1], float(wy.upper()))\n            wrs.setdefault(N, []).append(D['wr'])"),
        ('    for N in (4, 3):\n        idx, jlo, jhi, D = DL[N]\n', INFO_V3 + '    for N in (4, 3):\n        idx, jlo, jhi, D = DL[N]\n'),
        ("    run_plant('PLANT-L3-GAP', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'L3GAP'))",
         "    run_plant('PLANT-L3-GAP', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'L3GAP', 'law'))"),
        ("    run_plant('PLANT-LK-GAP', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'LKGAP'))",
         "    run_plant('PLANT-LK-GAP', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'LKGAP', 'law'))"),
        ("    run_plant('PLANT-ORIENT', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'ORIENT'))",
         "    run_plant('PLANT-ORIENT', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'ORIENT', 'law'))"),
        ("    run_plant('PLANT-RW', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'RW'))",
         "    run_plant('PLANT-RW', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'RW', 'law'))"),
        ("os.path.realpath(OWN + '/mr/v2')", "os.path.realpath(OWN + '/mr/v3')"),
        ("'PLANT-S0', 'PLANT-CXSWAP', 'PLANT-F2', 'PLANT-WRITE', 'PLANT-CX0-SIGN')",
         "'PLANT-S0', 'PLANT-CXSWAP', 'PLANT-F2', 'PLANT-WRITE', 'PLANT-CX0-SIGN', 'PLANT-ALIAS', 'PLANT-LAW-PIN')"),
        ("'Rw_hi); S8 E2 N4 %s N3 %s and FF N4 %s N3 %s (pk03); R4 %s (CORE)' % (",
         "'Rw_hi); S8 E2 N4 %s N3 %s and FF N4 %s N3 %s (pk03); R4 %s (CORE); v3: law certificates m3_lawcert_v1_1 N4 %s N3 %s and '\n"
         "                   'm3_lawcert_v1_2 N4 %s N3 %s (pk03) through m3_reader_s9h_v1 %s, each field the intersection with the record computation' % ("),
        ("PINS[S67[0]][:8], PINS[E2REC[4][0]][:8], PINS[E2REC[3][0]][:8], PINS[FFREC[4][0]][:8], PINS[FFREC[3][0]][:8], R4_SHA[:8]))",
         "PINS[S67[0]][:8], PINS[E2REC[4][0]][:8], PINS[E2REC[3][0]][:8], PINS[FFREC[4][0]][:8], PINS[FFREC[3][0]][:8], R4_SHA[:8],\n"
         "                       PINS[S8CERT[4]['v1_1'][0]][:8], PINS[S8CERT[3]['v1_1'][0]][:8], PINS[S8CERT[4]['v1_2'][0]][:8],\n"
         "                       PINS[S8CERT[3]['v1_2'][0]][:8], PINS[RDR][:8]))"),
        ("              'ROUNDING = *_hi rounded up, *_lo rounded down, 17 significant digits; tau_hi copied from the S4(c) v1_1 claim'])):",
         "              'ROUNDING = *_hi rounded up, *_lo rounded down, 17 significant digits; tau_hi copied from the S4(c) v1_1 claim',\n"
         "              'COMPUTATION = v3: per piece each field is the intersection of the S9-record computation (v2) and the law-certificate '\n"
         "              'computation (S8 D, E2, FF under m3_lawcert_v1_1, S8 N under v1_2)'])):"),
    ]
    for old, new in reps:
        n = txt.count(old)
        if n != 1:
            print('STOP: %d occurrences of %r' % (n, old[:90]))
            return 6
        txt = txt.replace(old, new)
    with open(OUT, 'x') as fh:
        fh.write(txt)
    print('SPLICE %s sha256 %s lines %d (from %s %s and %s %s; %d replacements)' % (
        os.path.basename(OUT), sha(OUT), txt.count('\n'), os.path.basename(SRC), sha(SRC)[:8], os.path.basename(LAW), sha(LAW)[:8], len(reps)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
