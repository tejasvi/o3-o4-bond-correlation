#!/usr/bin/env python3
"""make_cw_comb_v2_x3.py (pk23, C_w variant B): make_cw_comb_v2_x2.py (4af99db6, never run) with the row 4655: C-FINITE gets a plant.
- PLANT-FINITE: on the first piece, TT00 with a_1 = -a_0/t_mid (t_mid the piece's middle t) makes the 1 + eps of TT00's inverse hold 0 over
  the piece's ball T; the piece must be refused, i.e. its x1t_hi or c_h' enclosure is not finite (the C-FINITE predicate). The plant checks
  that 1 + eps does hold 0 (so the plant is effective), and counts an exception as a refusal too.
- So that the plant and the gated pieces share one code path, cw_comb_v2_0's per-piece lines for C-KAPPA's factor and for x1t_hi and the c_h'
  enclosure move, unchanged, into two helpers fac_of and x1t_chp inside run_n.
Otherwise as make_cw_comb_v2_x2.py (pk25's record notes for P3; the N-1 and N-2 with C-FINITE): makes pk23/cw/cw_comb_<VERSION>.py
from cw_comb_v2_0.py (c7d317fc) by exact replacements with asserted counts, and writes the diff. The new version reads IhR,10',b through
pk22's law certificate m3_lawcert_c3k_v2 (records m3_c3kp_*), loaded by pk23's reader fork m3_reader_cw_v1_1, pins that reader, that
producer and the P2 table it is given, and writes the record with STATUS = CERTIFIED when every gate passes, every plant fires, both N run on
state 10' and the P2 table's header says STATUS = CERTIFIED and RUN_VERDICT = VALID; otherwise STATUS = DRY with the DRY inputs named. Its
VERDICT line is exactly VERDICT VALID when every gate passes and every plant fires, and a STATUS line follows it.
Usage: make_cw_comb_v2_x3.py VERSION READER_SHA8 C3K2_SHA8 P2PATH P2_SHA8 (VERSION like v2_1; P2PATH relative to code/; each SHA8 the first 8
hex digits of that file's sha256, from its producer's frozen manifest or message; the maker checks them against the files). VERSION selftest
skips the reader and producer checks (they need not exist yet), writes only pk23/cw/out/SCRATCH_cw_comb_selftest_v2.py and no diff, for a
syntax check of the generated code; that file is never run or cited."""
import difflib, hashlib, os, re, sys
W18 = '/mnt/g2/release/root/code'
CWD = W18 + '/pk23/cw'
SRC = CWD + '/cw_comb_v2_0.py'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


assert len(sys.argv) == 6, __doc__.split('Usage: ')[1]
VER, R8, C8, P2P, P8 = sys.argv[1:]
SELFTEST = VER == 'selftest'
assert (SELFTEST or re.fullmatch(r'v2_[1-9][0-9]*', VER)) and all(re.fullmatch('[0-9a-f]{8}', x) for x in (R8, C8, P8)) and re.fullmatch(r'[A-Za-z0-9_./-]+', P2P)
DST, DIFF = CWD + '/cw_comb_%s.py' % VER, CWD + '/diff_cw_comb_v2_0_to_%s.txt' % VER
if SELFTEST:
    DST, DIFF = CWD + '/out/SCRATCH_cw_comb_selftest_v2.py', None
for p in (DST, DIFF):
    if p and os.path.exists(p):
        sys.exit('STOP exists %s' % p)
PS = sha(SRC)
assert PS.startswith('53c02836'), PS
RF, CF, PF = W18 + '/pk23/pev/m3_reader_cw_v1_1.py', W18 + '/pk22/m3/m3_lawcert_c3k_v2.py', W18 + '/' + P2P
SH = {}
for f, h8 in ((RF, R8), (CF, C8), (PF, P8)):
    if SELFTEST and f != PF:
        SH[f] = h8 + '0' * 56   # a stand-in, never written to a real version
        continue
    SH[f] = sha(f)
    assert SH[f].startswith(h8), '%s sha256 %s does not start with %s' % (f, SH[f], h8)
print('PARENT cw_comb_v2_0 %s; reader %s; producer %s; P2 %s %s%s' % (PS, SH[RF], SH[CF], P2P, SH[PF], '; SELFTEST' if SELFTEST else ''))


def apply(src, repl):
    new = src
    for lab, old, rep, cnt in repl:
        n_ = new.count(old)
        assert n_ == cnt, '%s: %d occurrences, expected %d' % (lab, n_, cnt)
        new = new.replace(old, rep)
        print('REPL %s: %d replaced' % (lab, n_))
    return new


src = open(SRC).read()
HEAD = ('cw_comb_%s.py (pk23, C_w variant B): cw_comb_v2_0.py (sha256 %s) with IhR,10\',b read through pk22\'s law certificate\n'
        'm3_lawcert_c3k_v2 (sha256 %s; the records m3_c3kp_E4D/E4N_N<N>_J300_c3kp.json, loaded with load bound to m3_run_v1_9_3_asm.<N>_c3k2.out,\n'
        'and the certificate with load_lawcert bound to m3_lawcert_c3k_v2_<N>.out) through pk23\'s reader fork m3_reader_cw_v1_1 (sha256 %s),\n'
        'the P2 table %s (sha256 %s) pinned, and the record\'s STATUS decided by the run: CERTIFIED when every gate passes, every plant fires,\n'
        'both N run on state 10\' and the P2 table\'s header says STATUS = CERTIFIED and RUN_VERDICT = VALID; DRY otherwise, with the DRY inputs\n'
        'named on the DRY_INPUTS line. The VERDICT line is exactly VERDICT VALID when every gate passes and every plant fires; a STATUS line follows\n'
        'it. For P3 (pk25\'s confirmation of CW_X11_v1): jlo and jhi are MR_LEMMAP v3\'s tokens exactly; the header carries LEMMAP_SHA256,\n'
        'TRIAL_SET (MR_LEMMAP v3\'s line), TRIAL_SET_10P (psi_xy\'\'s trial file per N with its sha256) and DEFINITIONS. The notes on\n'
        'v2_0 (9994a402), closed here: C-SQ2\'s sentence below words the normalisation factors as additive O(t^2) corrections; yes, the\n'
        'T2 class carries the products of the first-order coefficients into R: __mul__\'s R holds c1 d1 (the exact t^2 remainder of the product),\n'
        'and inv\'s R holds (c1 + R t)^2 / (y0^3 (1 + eps)) from 1/(1 + e) = 1 - e + e^2/(1 + e), valid while 1 + eps does not hold 0 over the\n'
        'piece\'s ball T, which C-FINITE checks on every piece (an arb ball that holds 0 makes the result infinite). C-FINITE\'s plant (the row\n'
        '4655), PLANT-FINITE: on the first piece, TT00 with a_1 = -a_0/t_mid makes the 1 + eps of its inverse hold 0 over T, and the piece must be\n'
        'refused. cw_comb_v2_0\'s per-piece lines for C-KAPPA\'s factor and for x1t_hi and c_h\' move, unchanged, into the helpers fac_of and\n'
        'x1t_chp, which the plant shares. Made by make_cw_comb_v2_x3.py. cw_comb_v2_0\'s docstring follows.\n') % (VER, PS, SH[CF], SH[RF], P2P, SH[PF])
new = apply(src, [
    ('docstring head', '"""cw_comb_v2_0.py (pk23, C_w variant B; ', '"""' + HEAD + 'cw_comb_v2_0.py (pk23, C_w variant B; ', 1),
    ('C-SQ2 wording (N-1)',
     "  multiple of psi_xy'(0) = x_1 (x) y exactly (state 10'), and X11 is its squared norm times factors 1 + O(t^2) (C-KAPPA); so on the piece\n"
     "  X11 <= t^2 max(R_hi, 0).\n",
     "  multiple of psi_xy'(0) = x_1 (x) y exactly (state 10'), and X11 main_D is its squared norm plus (a0/a2 - 1) A - ((a0/a1)^2 - 1)\n"
     "  P^2/|psi_xy'|^2 (C-KAPPA's notation), additive corrections that are O(t^2) since a0 - a_k = |r|^2 - <r, S^k r> = O(t^2) for psi_0 =\n"
     "  alpha u + r; so on the piece X11 <= t^2 max(R_hi, 0).\n", 1),
    ('P2 path', "P2F = CODEDIR + '/pk25/p2/dry_d2/MR_LEMMAP_V3F.kv'\n", "P2F = CODEDIR + '/%s'\n" % P2P, 1),
    ('reader and producer', "RDRF = HLD + '/m3_reader_cw_v1.py'\n",
     "RDRF = HLD + '/m3_reader_cw_v1_1.py'\nC3K2F = CODEDIR + '/pk22/m3/m3_lawcert_c3k_v2.py'\n", 1),
    ('pins', "P2F: '4a464522', MRJ: 'b0331e56', RDRF: 'aff9ad90'}", "P2F: '%s', MRJ: 'b0331e56', RDRF: '%s', C3K2F: '%s'}" % (P8, R8, C8), 1),
    ('raw tokens', "            rows[m.group(1)] = dict((f, (None if x == 'inf' else (x if x in ('True', 'False') else float(x)))) for f, x in zip(fields, v))\n",
     "            rows[m.group(1)] = dict((f, (None if x == 'inf' else (x if x in ('True', 'False') else float(x)))) for f, x in zip(fields, v))\n"
     "            rows[m.group(1)]['_tok'] = dict(zip(fields, v))   # the table's own tokens (the record copies jlo and jhi exactly)\n", 1),
    ('c3kp through the law certificate',
     "    if STATE == '10p':   # pk22's c3k rerun on 10' (DRY until its law certificate: the record's own laws)\n"
     "        for f in ('E4D', 'E4N'):\n"
     "            C3KP[f] = RDR.load(S3O + '/m3_c3kp_%s_N%d_J300_c3kp.json' % (f, N), S3O + '/m3_run_v1_9_3_asm.%d_c3k2.out' % N, 300, N)\n"
     "        out('C3KP N=%d: %s (record laws: DRY until the law certificate)' % (N, ', '.join('%s %s' % (r_['name'], r_['sha256'][:16]) for r_ in C3KP.values())))\n"
     "    for b in (0, 1, 3):\n"
     "        IT['IhR%d' % b] = (LawItem('E4N:IhR,10p,%d' % b, C3KP['E4N']['laws']['IhR,10,%d' % b]) if STATE == '10p'\n"
     "                           else LI('c3k', 'E4N', 'IhR,10,%d' % b))\n",
     "    if STATE == '10p':   # pk22's c3k rerun on 10', through its law certificate m3_lawcert_c3k_v2\n"
     "        for f in ('E4D', 'E4N'):\n"
     "            C3KP[f] = RDR.load(S3O + '/m3_c3kp_%s_N%d_J300_c3kp.json' % (f, N), S3O + '/m3_run_v1_9_3_asm.%d_c3k2.out' % N, 300, N)\n"
     "        CERTS['c3kp'] = RDR.load_lawcert(S3O + '/m3_lawcert_c3k_v2_N%d.json' % N, S3O + '/m3_lawcert_c3k_v2_%d.out' % N, 300, N, C3KP)\n"
     "        out('LAWCERT c3kp N=%d: m3_lawcert_c3k_v2_N%d.json (%s), %d entries; records %s' % (N, N, CERTS['c3kp']['producer'], len(CERTS['c3kp']['entries']),\n"
     "                                                                                    ', '.join('%s %s' % (r_['name'], r_['sha256'][:16]) for r_ in C3KP.values())))\n"
     "    for b in (0, 1, 3):\n"
     "        IT['IhR%d' % b] = LI('c3kp', 'E4N', 'IhR,10,%d' % b) if STATE == '10p' else LI('c3k', 'E4N', 'IhR,10,%d' % b)\n", 1),
    ('helpers and finite flag',
     "        return kapL * N11 - sub, sub, ch, N11, g\n"
     "\n"
     "    rows_rec, first, worst, worst11, last_info, sq2_all, ccor = [], None, None, None, None, True, 0.0\n",
     "        return kapL * N11 - sub, sub, ch, N11, g\n"
     "\n"
     "    def fac_of(key, r, last, jlo, jhi):\n"
     "        \"\"\"C-KAPPA's factor over t^2 on a piece (cw_comb_v2_0's lines, unchanged, moved here so that PLANT-FINITE shares them).\"\"\"\n"
     "        if last:\n"
     "            p = P2[key]\n"
     "            dt = ab(Fr(amax(p, 'u0pt')) + Fr(amax(p, 'u01t')) + Fr(amax(p, 'u03t'))) + (2 * (ab(Fr(p['q0t_hi'])) ** 2 + ab(Fr(p['eps_x0t_hi'])) ** 2\n"
     "                                                                                        + ab(Fr(p['eps_y0t_hi'])) ** 2)).sqrt()\n"
     "            dmax = dt / ab(Fr(jlo))\n"
     "            return 2 * dt * dt / (1 - dmax * dmax) ** 2\n"
     "        d = ab(Fr(max(abs(1 - r['u0p_lo']), abs(1 - r['u0p_hi']))) + Fr(amax(r, 'u01')) + Fr(amax(r, 'u03'))) + (\n"
     "            2 * (ab(Fr(r['q0_hi'])) ** 2 + ab(Fr(r['eps_x0_hi'])) ** 2 + ab(Fr(r['eps_y0_hi'])) ** 2)).sqrt()\n"
     "        return 2 * d * d / (1 - d * d) ** 2 * ab(Fr(jhi)) ** 2\n"
     "\n"
     "    def x1t_chp(X11, sub, ch, g, fac, key):\n"
     "        \"\"\"x1t_hi, chp_lo, chp_hi, R_hi and the C-KAPPA term on a piece (cw_comb_v2_0's lines, unchanged, moved here so that PLANT-FINITE\n"
     "        shares them).\"\"\"\n"
     "        g11lo = g['g11'].value().lower()\n"
     "        assert lo(g11lo) > 0, 'g11 not positive on %s' % key\n"
     "        RX = X11.R.upper()\n"
     "        RX = arb(0) if hi(RX) <= 0 else RX\n"
     "        corr = sub.value().upper() * fac\n"
     "        y2 = ((RX + corr) / g11lo).upper()\n"
     "        chv = ch.value()\n"
     "        return hi(y2.sqrt()), lo(chv), hi(chv), RX, corr\n"
     "\n"
     "    rows_rec, first, worst, worst11, last_info, sq2_all, ccor, fin_all = [], None, None, None, None, True, 0.0, True\n", 1),
    ('PLANT-FINITE', "            first = key\n",
     "            pif = dict(IT)   # PLANT-FINITE (the row 4655): TT00 with a_1 = -a_0/t_mid, so the 1 + eps of its inverse holds 0 over T\n"
     "            pt = copy.copy(IT['TT00'])\n"
     "            pt.ak = [pt.ak[0], -pt.ak[0] / ((Fr(1) / Fr(jlo) + Fr(1) / Fr(jhi)) / 2)] + pt.ak[2:]\n"
     "            pif['TT00'] = pt\n"
     "            gtt = pt.t2(Fr(jlo), Fr(jhi), T)\n"
     "            onef = 1 + (gtt.c1 * T + gtt.R * T * T) / gtt.c0\n"
     "            try:\n"
     "                Xf, subf, chf, _, gf = x11_of(pif, jlo, jhi, T, XDATA[STATE])\n"
     "                xf = x1t_chp(Xf, subf, chf, gf, fac_of(key, r, False, jlo, jhi), key)\n"
     "                refused, shown = not all(math.isfinite(v_) for v_ in xf[:3]), 'x1t_hi %s, c_h\\' [%s, %s]' % xf[:3]\n"
     "            except (ZeroDivisionError, ValueError, ArithmeticError) as exc_:\n"
     "                refused, shown = True, 'the piece raised %s' % type(exc_).__name__\n"
     "            plant('PLANT-FINITE', onef.contains(arb(0)) and refused,\n"
     "                  '(N=%d: TT00 with a_1 = -a_0/t_mid makes 1 + eps of its inverse hold 0 over the first piece (1 + eps %s), and C-FINITE must '\n"
     "                  'refuse the piece: %s)' % (N, onef.str(3), shown))\n"
     "            first = key\n", 1),
    ('per-piece lines through the helpers',
     "        g11lo = g['g11'].value().lower()\n"
     "        assert lo(g11lo) > 0, 'g11 not positive on %s' % key\n"
     "        RX = X11.R.upper()\n"
     "        RX = arb(0) if hi(RX) <= 0 else RX\n"
     "        if last:\n"
     "            p = P2[key]\n"
     "            dt = ab(Fr(amax(p, 'u0pt')) + Fr(amax(p, 'u01t')) + Fr(amax(p, 'u03t'))) + (2 * (ab(Fr(p['q0t_hi'])) ** 2 + ab(Fr(p['eps_x0t_hi'])) ** 2\n"
     "                                                                                        + ab(Fr(p['eps_y0t_hi'])) ** 2)).sqrt()\n"
     "            dmax = dt / ab(Fr(jlo))\n"
     "            fac = 2 * dt * dt / (1 - dmax * dmax) ** 2\n"
     "        else:\n"
     "            d = ab(Fr(max(abs(1 - r['u0p_lo']), abs(1 - r['u0p_hi']))) + Fr(amax(r, 'u01')) + Fr(amax(r, 'u03'))) + (\n"
     "                2 * (ab(Fr(r['q0_hi'])) ** 2 + ab(Fr(r['eps_x0_hi'])) ** 2 + ab(Fr(r['eps_y0_hi'])) ** 2)).sqrt()\n"
     "            fac = 2 * d * d / (1 - d * d) ** 2 * ab(Fr(jhi)) ** 2\n"
     "        corr = sub.value().upper() * fac\n"
     "        y2 = ((RX + corr) / g11lo).upper()\n"
     "        x1t = hi(y2.sqrt())\n"
     "        chv = ch.value()\n"
     "        chp_lo, chp_hi = lo(chv), hi(chv)\n",
     "        x1t, chp_lo, chp_hi, RX, corr = x1t_chp(X11, sub, ch, g, fac_of(key, r, last, jlo, jhi), key)\n"
     "        fin_all = fin_all and all(math.isfinite(v_) for v_ in (x1t, chp_lo, chp_hi))\n", 1),
    ('rows with tokens', "        rows_rec.append((key, jlo, jhi, x1t, chp_lo, chp_hi))\n",
     "        rows_rec.append((key, jlo, jhi, x1t, chp_lo, chp_hi, r['_tok']['jlo'], r['_tok']['jhi']))\n", 1),
    ('C-FINITE gate', "        N, STATE, len(rows_rec), last_info[0] if last_info else float('nan')))\n",
     "        N, STATE, len(rows_rec), last_info[0] if last_info else float('nan')))\n"
     "    gate('C-FINITE', fin_all, '(N=%d: x1t_hi and [chp_lo, chp_hi] are finite on all %d pieces, so every inverse 1/(y0 (1 + eps)) of the T2 class '\n"
     "         'stayed away from 0 over the piece\\'s ball T (the condition on N-2; its plant is PLANT-FINITE))' % (N, len(rows_rec)))\n", 1),
    ('record header',
     "L = ['# CW_X11 (pk23, cw_comb_v2_0 DRY): written by cw_comb_v2_0', 'FORMAT = CW_X11_KV_v1', 'RECORD = CW_X11', 'PRODUCER = pk23 cw_comb_v2_0',\n"
     "     'CODE = pk23/cw/cw_comb_v2_0.py:%s' % code_sha, 'STATUS = DRY', 'RUN_VERDICT = %s' % verdict,\n",
     ("P2HEAD = kv_table(P2F, 4)[0]\n"
      "dry_parts = (['N%d STATE 10 (state 10 for 10\\')' % n for n in (4, 3) if STN[n] != '10p'] +\n"
      "             ([] if (P2HEAD.get('STATUS') == 'CERTIFIED' and P2HEAD.get('RUN_VERDICT') == 'VALID') else\n"
      "              ['P2 %s (STATUS %s) for the last piece\\'s C-KAPPA term' % (os.path.relpath(P2F, CODEDIR), P2HEAD.get('STATUS'))]))\n"
      "status = 'CERTIFIED' if verdict == 'VALID' and not dry_parts else 'DRY'\n") +
     ("L = ['# CW_X11 (pk23, cw_comb_%s %%s): written by cw_comb_%s' %% status, 'FORMAT = CW_X11_KV_v1', 'RECORD = CW_X11', 'PRODUCER = pk23 cw_comb_%s',\n"
      "     'CODE = pk23/cw/cw_comb_%s.py:%%s' %% code_sha, 'STATUS = %%s' %% status, 'RUN_VERDICT = %%s' %% verdict,\n" % (VER, VER, VER, VER)), 1),
    ('DRY_INPUTS and SOURCE',
     "     'DRY_INPUTS = N4 STATE %s, N3 STATE %s; the c3kp laws from the records (law certificate pending); P2 dry_d2 (4a464522) for the last piece\\'s '\n"
     "     'C-KAPPA term' % (STN[4], STN[3]),\n"
     "     'SOURCE = pk23 m3_lawcert_cw_v1 9087afc2, m3_lawcert_hl_v1_1 8d5fe3c7, reader m3_reader_cw_v1 876b6184; pk03 m3_lawcert_v1_1, v1_2; '\n"
     "     'pk22 m3_lawcert_c3k_v1, c3kp records, psixy_exact_d_v1, v2; pk25 MR_LEMMAP v3 3164b778, P2 dry_d2 4a464522',\n",
     "     'DRY_INPUTS = %s' % ('; '.join(dry_parts) or 'none'),\n"
     "     'SOURCE = pk23 m3_lawcert_cw_v1 9087afc2, m3_lawcert_hl_v1_1 8d5fe3c7, reader m3_reader_cw_v1_1 %s; pk03 m3_lawcert_v1_1, v1_2; '\n"
     "     'pk22 m3_lawcert_c3k_v1, m3_lawcert_c3k_v2 %s (c3kp records), psixy_exact_d_v1, v2 (MANIFEST_PSIXY_10P_v1); pk25 MR_LEMMAP v3 3164b778, '\n"
     "     'P2 %s %s; MR_INSERT v4b 54691bc1, MR_SPECTRAL v4 0e4d8177 and pk22 MR_JOINT 80bc8d81 for the DRY |Q f|/t only' % (\n"
     "         sha(RDRF)[:8], sha(C3K2F)[:8], os.path.relpath(P2F, CODEDIR), sha(P2F)[:8]),\n", 1),
    ('header lines for P3',
     "     'TRIAL_SET = N4 %s, N3 %s' % (TS_LINE[4], TS_LINE[3]), 'FIELDS = jlo jhi x1t_hi chp_lo chp_hi']\n",
     "     'LEMMAP_SHA256 = %s' % sha(MRL3), 'TRIAL_SET = %s' % kv_table(MRL3, 4)[0]['TRIAL_SET'],\n"
     "     'TRIAL_SET_10P = N4 %s, N3 %s (the trial file of psi_xy\\' per N, as psixy_exact_d names it: state 10\\' when the run\\'s STATE is 10p; '\n"
     "     'C-10P)' % (TS_LINE[4], TS_LINE[3]),\n"
     "     'DEFINITIONS = x1t_hi >= |Q_xy S M_c\\' x_1| / t at every J of the piece (t = 1/J, the last piece to t = 0); x_1 = psi_1/|psi_1| (state 1 of '\n"
     "     'TRIAL_SET); Q_xy = I - |psi_xy\\'><psi_xy\\'| / |psi_xy\\'|^2 with psi_xy\\' the state 10\\' of TRIAL_SET_10P (pk22\\'s exact c\\'(t), '\n"
     "     'psixy_exact_d_v2); M_c\\' = M_h - c_h\\' with c_h\\' = Mh00/TT00 = <S psi_0, M_h S psi_0> / <S psi_0, S psi_0> (pk23\\'s Pev laws); '\n"
     "     'chp_lo <= c_h\\' <= chp_hi on the piece; ran Q_ext lies in ran Q_xy, so x1t_hi t >= |Q_ext S M_c\\' x_1| too',\n"
     "     'FIELDS = jlo jhi x1t_hi chp_lo chp_hi']\n", 1),
    ('writer with tokens', "    for key, jlo, jhi, x1t, a, b in REC_ROWS[N]:\n"
     "        L.append('%s = %r %s %r %r %r' % (key, jlo, 'inf' if jhi is None else repr(jhi), x1t, a, b))\n",
     "    for key, jlo, jhi, x1t, a, b, tlo, thi in REC_ROWS[N]:\n"
     "        L.append('%s = %s %s %r %r %r' % (key, tlo, thi, x1t, a, b))\n", 1),
    ('verdict lines',
     "out('VERDICT %s' % ('DRY (record STATUS DRY; gates and plants: %s)' % ('all PASS / FIRE' if verdict == 'VALID' else\n"
     "                                                                         'FAIL ' + ', '.join(FAILS + ['%s did not fire' % x for x in NOFIRE]))))\n",
     "out('VERDICT %s' % ('VALID' if verdict == 'VALID' else 'INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % x for x in NOFIRE])))\n"
     "out('STATUS %s (DRY inputs: %s)' % (status, '; '.join(dry_parts) or 'none'))\n", 1),
])
with open(DST, 'x') as fh:
    fh.write(new)
print('WROTE %s %s' % (sha(DST), DST))
if DIFF:
    with open(DIFF, 'x') as fh:
        fh.writelines(difflib.unified_diff(src.splitlines(True), new.splitlines(True), 'cw_comb_v2_0.py', 'cw_comb_%s.py' % VER))
    print('WROTE %s %s' % (sha(DIFF), DIFF))
