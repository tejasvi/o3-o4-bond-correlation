#!/usr/bin/env python3
"""job137 (pk25, C12 step 2; the P0_LOG rows 4401, 4418): writes asm/src/kt_s9h_asm_v1_8.py.in from asm/src/kt_s9h_asm_v1_4b.py.in (the
template of the certified C6a v3 engine kt_s9h_asm_v1_7) by exact line edits, each line found once: the record folder mr/v4; the M1 engine pin
kt_mr_assembly_v1_8_4 with SPEC_V3 and LMP_V3 (the certified mr/v3 records); helpers engine_orient_rx, rec_rows and ochk_check before
check_grid; before the records are formed, C-ORIENT-LINE, C-V3-SAME (MR_SPECTRAL's and MR_LEMMAP's rows equal mr/v3's) and PLANT-COMBINE
; MR_SPECTRAL written as MR_INPUT_KV_v4 with the ORIENT_CHECK line, C-OCHK-READ and PLANT-OCHK; MR_LEMMAP checked
but not rewritten (mr/v3's stays the one side table, so LEMMAP_SHA256 keeps one value); the docstring's first line names v1_8. The output
is written with 'x' and parsed only after the maker fills it."""
import hashlib
import os
import sys

D = '/mnt/g2/release/root/code/pk25/asm/src/'
SRC, OUT = D + 'kt_s9h_asm_v1_4b.py.in', D + 'kt_s9h_asm_v1_8.py.in'
HELPERS = [
    "def engine_orient_rx():",
    "    \"\"\"v1_8: the M1 engine's ORIENT_CHECK pattern ORIENT_RX, read by ast from the pinned engine file.\"\"\"",
    "    tree = ast.parse(open(MR_ENGINE).read())",
    "    got = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)",
    "           and n.targets[0].id == 'ORIENT_RX']",
    "    if len(got) != 1:",
    "        raise Refused('C-ORIENT-LINE: the M1 engine defines ORIENT_RX %d times' % len(got))",
    "    return got[0]",
    "",
    "",
    "def rec_rows(path):",
    "    \"\"\"v1_8: a pinned record's rows (key, values) after its FIELDS line.\"\"\"",
    "    if PINS.get(path) is None or sha_file(path) != PINS[path]:",
    "        raise Refused('C-V3-SAME: %s does not match its pin' % os.path.basename(path))",
    "    rows, seen = [], False",
    "    for ln in lines_of(path):",
    "        if ln.startswith('FIELDS = '):",
    "            seen = True",
    "        elif seen and ln.strip() and not ln.startswith('#'):",
    "            k, v = [x.strip() for x in ln.split('=', 1)]",
    "            rows.append((k, v.split()))",
    "    return rows",
    "",
    "",
    "def ochk_check(text, cnt):",
    "    \"\"\"v1_8 C-OCHK-READ: the record text carries one ORIENT_CHECK line matching the M1 engine's ORIENT_RX with the record's piece counts.\"\"\"",
    "    v = [ln.split('=', 1)[1].strip() for ln in text.split('\\n') if ln.startswith('ORIENT_CHECK = ')]",
    "    mo = re.match(engine_orient_rx(), v[0]) if len(v) == 1 else None",
    "    if not mo or (int(mo.group(1)), int(mo.group(2))) != (cnt[4], cnt[3]):",
    "        raise Refused('C-OCHK-READ: ORIENT_CHECK missing or with other piece counts')",
    "    return True",
    "",
    ""]
BLOCK = [
    "    # v1_8 (C12 step 2): MR_SPECTRAL as MR_INPUT_KV_v4 with the ORIENT_CHECK line; its rows equal the certified mr/v3 record's, and MR_LEMMAP",
    "    # stays mr/v3's (rows checked equal, not rewritten), so LEMMAP_SHA256 keeps one value across the producers",
    "    cnt = dict((N, sum(1 for k, _v in ROWS['spec'] if k.startswith('N%d_' % N))) for N in (4, 3))",
    "    ochk = ('C-ORIENT PASS on every piece (N4 %d, N3 %d): u~_x has a positive coefficient on the canonical e1 and u~_y on the canonical e3; '",
    "            'plant PLANT-ORIENT fired' % (cnt[4], cnt[3]))",
    "    okl = (not any(g.startswith('C-PIECE') for g in fails) and 'PLANT-ORIENT' in EXEC and 'PLANT-ORIENT' not in nofire and",
    "           flag(engine_orient_rx) and re.match(engine_orient_rx(), ochk) is not None)",
    "    out('C-ORIENT-LINE: C-ORIENT passed on every piece (N4 %d, N3 %d), PLANT-ORIENT fired, the line matches the M1 engine\\'s ORIENT_RX -> %s' % (",
    "        cnt[4], cnt[3], gate(fails, 'C-ORIENT-LINE', okl)))",
    "    for nm, path, key in (('MR_SPECTRAL', SPEC_V3, 'spec'), ('MR_LEMMAP', LMP_V3, 'lmp')):",
    "        try:",
    "            ok = rec_rows(path) == [(k, list(v)) for k, v in ROWS[key]]",
    "        except Refused as e:",
    "            out('  refused: %s' % e)",
    "            ok = False",
    "        out('C-V3-SAME %s: every row equals the certified mr/v3 record\\'s (%s) -> %s' % (nm, PINS[path][:8], gate(fails, 'C-V3-SAME %s' % nm, ok)))",
    "",
    "    def combine_plant():",
    "        Dr = piece_compute(4, idx1, jlo1, jhi1, IN, None, 'rec')",
    "        Dl = piece_compute(4, idx1, jlo1, jhi1, IN, None, 'law')",
    "        sh = (abs(Dr['cx'].upper()) + abs(Dr['cx'].lower()) + abs(Dl['cx'].upper()) + abs(Dl['cx'].lower())) * 2 + 1",
    "        combine(Dr, dict(Dl, cx=Dl['cx'] + sh))",
    "    run_plant('PLANT-COMBINE', combine_plant)"]
EDITS = [
    ("RECDIR = OWN + '/mr/v3' if MODE == 'cert' else os.path.join(ASM, 'dry_%s' % TAG)",
     ["RECDIR = OWN + '/mr/v4' if MODE == 'cert' else os.path.join(ASM, 'dry_%s' % TAG)   # v1_8: MR_SPECTRAL v4 to mr/v4"]),
    ("MR_ENGINE = CODEDIR + '/pk24/mr_engine/kt_mr_assembly_v1_6.py'",
     ["MR_ENGINE = CODEDIR + '/pk24/mr_engine/kt_mr_assembly_v1_8_4.py'   # v1_8: the M1 engine of G6 v1_6_2 (FIELDS, ORIENT, ORIENT_RX)",
      "SPEC_V3 = OWN + '/mr/v3/MR_SPECTRAL.kv'   # v1_8: the certified v3 records the v4 rows must equal",
      "LMP_V3 = OWN + '/mr/v3/MR_LEMMAP.kv'"]),
    ("def check_grid(P):", HELPERS + ["def check_grid(P):"]),
    ("    texts = {}", BLOCK + ["    texts = {}"]),
    ("            ('MR_SPECTRAL', 'MR_INPUT_KV_v3', SPEC_FIELDS, ROWS['spec'], []),",
     ["            ('MR_SPECTRAL', 'MR_INPUT_KV_v4', SPEC_FIELDS, ROWS['spec'], ['ORIENT_CHECK = %s' % ochk]),"]),
    ("    run_plant('PLANT-WRITE', lambda: readback(texts['MR_SPECTRAL'][0], 'MR_INPUT_KV_v3', 'MR_SPECTRAL', SPEC_FIELDS, ROWS['spec'], tamper=True))",
     ["    run_plant('PLANT-WRITE', lambda: readback(texts['MR_SPECTRAL'][0], 'MR_INPUT_KV_v4', 'MR_SPECTRAL', SPEC_FIELDS, ROWS['spec'], tamper=True))",
      "    out('C-OCHK-READ: MR_SPECTRAL\\'s text carries the ORIENT_CHECK line with N4 %d, N3 %d -> %s' % (",
      "        cnt[4], cnt[3], gate(fails, 'C-OCHK-READ', flag(lambda: ochk_check(texts['MR_SPECTRAL'][0], cnt)))))",
      "    run_plant('PLANT-OCHK', lambda: ochk_check('\\n'.join(ln for ln in texts['MR_SPECTRAL'][0].split('\\n') if not ln.startswith('ORIENT_CHECK = ')), cnt))"]),
    ("    if not os.path.isdir(RECDIR) or os.path.realpath(RECDIR) not in (os.path.realpath(OWN + '/mr/v3'), os.path.realpath(os.path.join(ASM, 'dry_%s' % TAG))):",
     ["    if not os.path.isdir(RECDIR) or os.path.realpath(RECDIR) not in (os.path.realpath(OWN + '/mr/v4'), os.path.realpath(os.path.join(ASM, 'dry_%s' % TAG))):"]),
    ("    for rec in ('MR_SPECTRAL', 'MR_LEMMAP'):", ["    for rec in ('MR_SPECTRAL',):   # v1_8: MR_LEMMAP stays mr/v3's"]),
    ("               'PLANT-S0', 'PLANT-CXSWAP', 'PLANT-F2', 'PLANT-WRITE', 'PLANT-CX0-SIGN', 'PLANT-ALIAS', 'PLANT-LAW-PIN')",
     ["               'PLANT-S0', 'PLANT-CXSWAP', 'PLANT-F2', 'PLANT-WRITE', 'PLANT-CX0-SIGN', 'PLANT-ALIAS', 'PLANT-LAW-PIN', 'PLANT-COMBINE', 'PLANT-OCHK')"]),
    ('"""@@NAME@@ (pk25, code/pk25/asm/; G5 item C6a): the record MR_SPECTRAL (MR_INPUT_KV_v3) and the Lemma P side table MR_LEMMAP',
     ['"""@@NAME@@ (pk25, code/pk25/asm/; G5 C6a, v1_8 for C12 step 2: MR_SPECTRAL written as MR_INPUT_KV_v4 with the ORIENT_CHECK line to mr/v4,',
      'its rows equal to the certified mr/v3 record\'s (C-V3-SAME), MR_LEMMAP checked equal to mr/v3\'s and not rewritten, PLANT-COMBINE and PLANT-OCHK',
      'added; the v3 text follows): the record MR_SPECTRAL (MR_INPUT_KV_v3) and the Lemma P side table MR_LEMMAP'])]


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    if os.path.exists(OUT):
        print('STOP: %s exists' % OUT)
        return 6
    lines = open(SRC).read().split('\n')
    for old, new in EDITS:
        k = [n for n, ln in enumerate(lines) if ln == old]
        if len(k) != 1:
            print('STOP: the line %r found %d times' % (old[:70], len(k)))
            return 6
        lines = lines[:k[0]] + new + lines[k[0] + 1:]
    txt = '\n'.join(lines)
    with open(OUT, 'x') as fh:
        fh.write(txt)
    print('SPLICE %s sha256 %s lines %d (from %s %s, %d line edits)' % (os.path.basename(OUT), sha(OUT), txt.count('\n'), os.path.basename(SRC),
                                                                       sha(SRC)[:8], len(EDITS)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
