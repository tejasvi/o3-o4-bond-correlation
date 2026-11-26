#!/usr/bin/env python3
"""job139 (pk25, C12 step 1, MR_INSERT v4 producer v2_2; the P0_LOG row 4441): job135's splice with one source changed, so that the
engine differs from kt_s9h_ins_v2_1 (ae471223) by one change alone: asm/src/s9c_v1_8_blocks.py.txt in place of s9c_v1_7_blocks.py.txt
(L7's |h_00| bounds (C8)'s vacuum amplitude: + (2 W + W^2) N_H), output asm/src/kt_s9h_ins_v2_2s.py.in, and one docstring
sentence naming the change. Everything else is job135's: the C6b base template kt_s9h_ins_v1_1.py.in, the blocks s9c_v1_6_ins_blocks,
ins_v1_5_ta and ins_v2_1_blocks, the main ins_v2_1_main, the dry/cert argument check, LEMMAP on mr/v3 and the nine constants. Each replaced
span is found by scanning; the output is written with 'x' and parsed only after the maker fills it."""
import ast
import hashlib
import os
import sys

D = '/mnt/g2/release/root/code/pk25/asm/src/'
SRC, OUT = D + 'kt_s9h_ins_v1_1.py.in', D + 'kt_s9h_ins_v2_2s.py.in'
BLKS = [D + 's9c_v1_6_ins_blocks.py.txt', D + 'ins_v1_5_ta.py.txt', D + 's9c_v1_8_blocks.py.txt', D + 'ins_v2_1_blocks.py.txt']
MAIN = D + 'ins_v2_1_main.py.txt'
ARGV_OLD = ["if len(sys.argv) != 3 or sys.argv[1] != 'dry' or not re.fullmatch(r'[A-Za-z0-9_]{1,40}', sys.argv[2]):",
            "    print('usage: @@NAME@@ dry TAG')"]
ARGV_NEW = ["MODES = ('dry', 'cert')   # v2_1: cert only under the approval naming this file's sha8",
            "if len(sys.argv) != 3 or sys.argv[1] not in MODES or not re.fullmatch(r'[A-Za-z0-9_]{1,40}', sys.argv[2]):",
            "    print('usage: @@NAME@@ dry|cert TAG')"]
LEMMAP_OLD = "LEMMAP = OWN + '/mr/v2/MR_LEMMAP.kv'"
LEMMAP_NEW = "LEMMAP = OWN + '/mr/v3/MR_LEMMAP.kv'   # v2_1: the certified C6a v3 side table (the review 087868a8 CLEAR; the row 4401)"


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def span(lines, name):
    """the 0-based [start, end) line span of the one top-level def name, found by scanning (the template is not valid Python yet)."""
    starts = [i for i, ln in enumerate(lines) if ln.startswith('def %s(' % name)]
    if len(starts) != 1:
        raise SystemExit('STOP: def %s found %d times' % (name, len(starts)))
    i = starts[0]
    j = i + 1
    while j < len(lines) and not (lines[j] and not lines[j][0].isspace() and not lines[j].startswith('#')):
        j += 1
    while j > i + 1 and not lines[j - 1].strip():
        j -= 1
    return i, j


def one_line(lines, text):
    k = [n for n, ln in enumerate(lines) if ln == text]
    if len(k) != 1:
        raise SystemExit('STOP: the line %r found %d times' % (text[:60], len(k)))
    return k[0]


def main():
    if os.path.exists(OUT):
        print('STOP: %s exists' % OUT)
        return 6
    lines = open(SRC).read().split('\n')
    blk = '\n\n\n'.join(open(p).read().rstrip('\n') for p in BLKS).split('\n')
    mn = open(MAIN).read().rstrip('\n').split('\n')
    ast.parse('\n'.join(blk))
    ast.parse('\n'.join(mn))
    i, j = span(lines, 'main')
    lines = lines[:i] + mn + lines[j:]
    i, j = span(lines, 'h_piece')
    lines = lines[:i] + blk + lines[j:]
    a = one_line(lines, ARGV_OLD[0])
    if lines[a + 1] != ARGV_OLD[1]:
        print('STOP: the usage line does not follow the argument check')
        return 6
    lines = lines[:a] + ARGV_NEW + lines[a + 2:]
    b = one_line(lines, LEMMAP_OLD)
    lines[b] = LEMMAP_NEW
    k = [n for n, ln in enumerate(lines) if ln.startswith("M4H_READER_PATH = ")]
    if len(k) != 1:
        print('STOP: M4H_READER_PATH line found %d times' % len(k))
        return 6
    lines = lines[:k[0] + 1] + ["MU = OWN + '/mu/kt_mu_hw_v1_1.py'   # the mu tool v1_1 (the row 4386 N4)",
                                "CI_MARGIN = '0.01'   # the margin around c~_h's hull for the mu tool's interval (C-CH-HULL checks c_h inside)",
                                "MEANS = CODEDIR + '/pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37_1.kv'   # R4's certified means export (c_t, c_b)",
                                "DJREC = dict((N, (CODEDIR + '/pk22/m3/out/m3_c3j_DJ_N%d_J300_c3j.json' % N, CODEDIR + '/pk22/m3/out/m3_run_v1_9_3_asm.%d_c3j.out' % N)) for N in (4, 3))   # pk22's c3j DJ records (DHT)",
                                "LAM9C = 60   # the S9(c) Lam-split level (pk02/S9C_PLAN_v2_ADD1.md sect. 1; the row 4328)",
                                "BAD_TOL = '1e-10'   # C-BAD-SMALL and C-BAD-W (S9C_BADPART_LEMMA_v1 sect. 4)",
                                "ENGA = dict((N, CODEDIR + '/pk01/out_kt_c_v2_3_e1n%d.out' % N) for N in (4, 3))   # engine A's EXPLICIT lines (m_bg, INFO)",
                                "M1ENG = CODEDIR + '/pk24/mr_engine/kt_mr_assembly_v1_8_4.py'   # the M1 engine: MR_INSERT v4 FIELDS, X_POWER, X_DEFINITION, ORIENT_RX",
                                "SPEC_V3 = OWN + '/mr/v3/MR_SPECTRAL.kv'   # the certified MR_SPECTRAL: TRIAL_SET is copied from it (the row 4321)"] + lines[k[0] + 1:]
    old = '"""@@NAME@@ (pk25, code/pk25/asm/; G5 item C6b, exploration stage): h\'s bulk amplitudes per piece of R4\'s grid (S9(b)-h), DRY ONLY.'
    new = ('"""@@NAME@@ (pk25, code/pk25/asm/; G5 C12 step 1, the rows 4380, 4401, 4407, 4418): the MR_INSERT v4 producer, MODE dry or\n'
           'cert (cert only under the approval naming this file\'s sha8; the record to mr/v4/MR_INSERT.kv, a dry run\'s to asm/dry_<TAG>/). h rows:\n'
           'S9(c)-h (the code of the S9C engine kt_s9c_h_v1_7, pk25/S9C_LINES_v1.md with S9C_LINES_v1_1.md), xc enclosing v_x/t by the centred\n'
           'form of M_R^c/t with the lines and Lemma A over t_lo, vx joined with t xc at both ends, way B on the last piece (xc = [g_lo, g_hi],\n'
           'xf = f); t and a rows as kt_s9h_ins_v1_5 (power 0: xc = vx, xf = 0); Pev = C for h and t (the row 4376); the header of\n'
           'pk24/MIDROW_G6_SPEC_v1_6_2.md sect. 6 with FIELDS, X_POWER, X_DEFINITION and the ORIENT_CHECK pattern read by ast from the\n'
           'pinned M1 engine, TRIAL_SET copied from mr/v3 MR_SPECTRAL, LEMMAP_SHA256 of mr/v3 MR_LEMMAP; gates C-SIGN-S9C, C-BAD-W, C-ANCHOR,\n'
           'C-FACTX, C-FLOOR, C-ORIENT-LINE, C-WRITE; the C8 notes N1 (c_t ends by exact comparison), N2 (PLANT-MU-T, PLANT-MU-C), N4\n'
           '(mu tool v1_1). v2_2: L7\'s |h_00| bounds (C8)\'s vacuum amplitude, + (2 W + W^2) N_H (the row 4441).\n'
           'The C6b base template text follows. C6b base: h\'s bulk amplitudes per piece of R4\'s grid (S9(b)-h).')
    txt = '\n'.join(lines)
    if txt.count(old) != 1:
        print('STOP: the docstring line found %d times' % txt.count(old))
        return 6
    txt = txt.replace(old, new)
    with open(OUT, 'x') as fh:
        fh.write(txt)
    print('SPLICE %s sha256 %s lines %d (from %s %s; %s; %s %s)' % (os.path.basename(OUT), sha(OUT), txt.count('\n'), os.path.basename(SRC), sha(SRC)[:8],
                                                               ', '.join('%s %s' % (os.path.basename(p), sha(p)[:8]) for p in BLKS), os.path.basename(MAIN),
                                                               sha(MAIN)[:8]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
