#!/usr/bin/env python3
"""assemble_nunote_v1.py (pk24; the pattern of assemble_m2plan_v1_3.py): writes pk24/NU_G_NOTE_v1.md from
notes_src/NU_G_NOTE_body_v1.md and MANIFEST_NU_G_NOTE_v1.sha256. Fills {{DATE}}, {{SHA8:path}}, {{LINES}} (source lines by prefix, cut at 600
characters) and {{FILES}}. Mode 'x' for both. Every {{SHA8:path}} must be a listed file, and every prefix must give at least one line."""
import os, re, sys, hashlib, datetime

W18 = '/mnt/g2/release/root/code'
O = W18 + '/pk24'
BODY = O + '/notes_src/NU_G_NOTE_body_v1.md'
NOTE = O + '/NU_G_NOTE_v1.md'
MAN = O + '/MANIFEST_NU_G_NOTE_v1.sha256'
KT = 'pk02/kt_cert_v1_9.py'
SRC = [(KT, ('A_ = (3 + SQ21) / 6', 'B_ = (3 * SQ5 - SQ21) / 12', 'TRI = [A_, A_, B_]', 'PAIRS = [(0, 1), (1, 2), (0, 2)]',
             'RHO_M, RHO_E = 0.55, 0.6', 'def xi_pair(iu, iv, iq):', '    return ser([pvar(iq, NVX, arb(1) / 2)]', 'def anh(iu, iv, c):',
             'def vac_poly(xs):', 'def state_poly(xs, b):', '    H0 = zero()', '        H0 = H0 + anh(XS[r], XS[s], TRI[p])',
             '    EL, E0 = HL.exp(), H0.exp()', "    pS = {'psi': vac_poly(xiS)", '    bas = {g: restrict6(E0 * pS[g]) for g in pS}',
             '    m = solve_mid([[B0(basis[i], basis[j])', '    """B0(f, h) = E_D[', 'a_m, a_e = RHO_M ** 2, RHO_E ** 2', 'c_m, c_e = (up_float(',
             'ED_ = ', 'LD = lap_a(ED_, 6)', 'BD = gauge_basis_a(6, range(6))', '    G1, n1 = tilted_cov_a(LD, BD, [c_m * t] * 6)',
             '    nP = nsqrt(n1 * w1.E2(Pg, Pg))', '    """L0 side:', '    """F3: P = r0', '    mg = [abs(sum((arb(m[j][gi]) * t ** j',
             '    """sup |F| of the item', 'GK = {')),
       ('pk02/arbeng_c2b_v2.py', ('    """pseries.w_coeffs', '    """condg.sigma_to_g', '    """wishart.Wishart in balls')),
       ('pk02/SPEC_M1_CERT_v1_1_ADD2_v1.md', ('B = (near^2 + far_out)^{1/2} + gB bounds', '- **(i) Weighted one-column norms are Schur bounds.**',
                                                  '  - Take h = W P and w = W.', '  - Engine A evaluates exactly that quantity',
                                                  '  - The tilts (rates c_m t, c_e t)', '- **(ii) Pointwise majorants.**',
                                                  '- **(iii) Far and bad parts.**', '- **(v) The m_g.**')),
       ('pk10/PK10_NOTES.md', ('### 12.2 The expansion', '- **Centre-of-mass gauge [derived; checked].**',
                                     '- **Exact chart identity on the upper hemisphere:**')),
       ('rv02/REVIEW_KTCERT_RE_DEFINITION_rv02.md', ('- Hence r0 = s0', '- Since r0 lies in W(0)')),
       ('rv02/REVIEW_KTCERT_RE_DEFINITION_ADD1_rv02.md', ('  - (b) Add t sum_g',)),
       ('rv02/REVIEW_P2_V2_1_rv02.md', ('- With r0 = sum_g delta_g psi_g(0)', '- The term sits outside the square root',
                                              '- N-2: the certified NU input')),
       ('pk25/p2/kt_p2_v2_1.py', ('    R_e/t <= [',))]
TS = ['pk11/out/ts_N4_J170_D_S_z9sym_v1.json', 'pk11/out/ts_N3_S_z9sym_v1.json', 'pk11/out/vacres_K3_N4_sym_v1.json',
      'pk11/out/vacres_K3_N3_sym_v1.json', 'pk22/midrow/psixy/ts_N4_J170_D_S_z9symxy_v1.json', 'pk22/midrow/psixy/ts_N3_S_z9symxy_v1.json',
      'pk22/midrow/psixy/ts_N4_J170_D_S_z9symxyp_v1.json', 'pk22/midrow/psixy/ts_N3_S_z9symxyp_v1.json',
      'pk02/FAR_CRUDE_v1_N4.json', 'pk02/FAR_CRUDE_v1_N3.json']
FILES = [p for p, _ in SRC] + ['rv02/MANIFEST_REVIEW_KTCERT_RE_DEFINITION_rv02.sha256',
                               'rv02/MANIFEST_REVIEW_KTCERT_RE_DEFINITION_ADD1_rv02.sha256',
                               'rv02/MANIFEST_REVIEW_P2_V2_1_rv02.sha256'] + TS + \
        ['pk24/notes_src/NU_G_NOTE_body_v1.md', 'pk24/tools/assemble_nunote_v1.py', 'pk24/jobs/job239_nunote_v1.sh']


def h(p):
    s = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 20), b''):
            s.update(blk)
    return s.hexdigest()


assert not os.path.exists(NOTE) and not os.path.exists(MAN)
assert len(set(FILES)) == len(FILES), 'duplicate file entry'
for f in FILES:
    assert os.path.isfile(W18 + '/' + f), f
body = open(BODY).read()
for ph in ('{{DATE}}', '{{LINES}}', '{{FILES}}'):
    assert body.count(ph) == 1, ph
for m in re.finditer(r'\{\{SHA8:([^}]+)\}\}', body):
    assert m.group(1) in FILES, ('SHA8 path not in FILES', m.group(1))
date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
body = re.sub(r'\{\{SHA8:([^}]+)\}\}', lambda m: h(W18 + '/' + m.group(1))[:8], body)
ln_ = []
for path, pres in SRC:
    lines = open(W18 + '/' + path, encoding='utf-8').read().splitlines()
    ln_.append('%s (sha8 %s):' % (path, h(W18 + '/' + path)[:8]))
    for pre in pres:
        hit = 0
        for i, x in enumerate(lines, 1):
            if x.startswith(pre):
                ln_.append('  l.%d %s' % (i, x if len(x) <= 600 else x[:600] + ' ...'))
                hit += 1
        assert hit > 0, ('no line from', path, pre)
    ln_.append('')
fl = ['%s  %d  %s' % (h(W18 + '/' + f), os.path.getsize(W18 + '/' + f), f) for f in FILES]
note = body.replace('{{DATE}}', date).replace('{{LINES}}', '\n'.join(ln_).rstrip('\n')).replace('{{FILES}}', '\n'.join(fl))
assert '{{' not in note, 'unfilled placeholder'
with open(NOTE, 'x') as fh:
    fh.write(note)
print('NOTE %s %s (%d lines, %d tool lines, %d files)' % (h(NOTE), NOTE, note.count('\n'), len(ln_), len(fl)))
rels = FILES + [os.path.relpath(NOTE, W18)]
with open(MAN, 'x') as fh:
    fh.write(''.join('%s  %s\n' % (h(W18 + '/' + r), r) for r in rels))
ok = 0
for ln in open(MAN).read().splitlines():
    s, r = ln.split('  ', 1)
    good = h(W18 + '/' + r) == s
    ok += good
    if not good:
        print('FAILED %s' % r)
print('MANIFEST %s %s: %d of %d OK' % (h(MAN), MAN, ok, len(rels)))
