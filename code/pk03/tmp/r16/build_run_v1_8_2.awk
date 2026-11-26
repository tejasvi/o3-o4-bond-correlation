# build_run_v1_8_2.awk -- pk03. Writes m3_run_v1_8_2.py from m3_run_v1_8_1.py (32bed253): the N record on route B's scope (
# option 3). Lines 717-901 (walk_pieces and run_asm) are replaced by tmp/r16/asmN_block_v1_8_2.py; every other changed line is checked
# against a substring of the original first; a mismatch prints BUILD ERROR and exits 1.
# Usage: awk -v B=<block file> -f build_run_v1_8_2.awk m3_run_v1_8_1.py > m3_run_v1_8_2.py
function need(s) { if (index($0, s) == 0) { print "BUILD ERROR line " NR ": expected " s; bad = 1; exit 1 } }
NR == 2 {
    need("\"\"\"m3_run_v1_8_1.py -- pk03 (code/pk03/). REVISION of m3_run_v1_8.py (7d72fc7f) for option 5: one item,")
    print "\"\"\"m3_run_v1_8_2.py -- pk03 (code/pk03/). REVISION of m3_run_v1_8_1.py (32bed253) for option 3: one item, asmN.N,"
    print "the N record on route B's scope, assembled from the N pieces m3_run_v1_8 finished, while the rest of the family stays uncomputed."
    print "- ITEM_RE accepts asmN.4 and asmN.3 only (this script computes no entry and writes no hand-off). Every hand-off it reads is"
    print "  m3_run_v1_8's (V18_SHA; capped pieces must be clean CAP-STOPs of m3_run_v1_8), as in v1_8_1."
    print "- walk_done replaces walk_pieces: the VALID N pieces in order, each advancing (C-PIECES as before, capped pieces skipped), without"
    print "  the gate that they cover the family; the entry in progress at the last piece is not used (PIECES-DONE)."
    print "- The scope (pk11, from kt_s8_cert_v1_11 l.487-492 and s8core_v1_8_2 l.1120-1147): every T,a,b of S8_ENTRY_LIST_v3's N"
    print "  graph (55) and the TX,a,b with max(a, b) <= 3 (10). C-SCOPE-N: 65 keys, 55 + 10, all in the list and every one complete in a"
    print "  VALID piece (PLANT-SCOPE-N: the family's last entry added must not be complete). C-SCOPE: the record holds exactly them."
    print "- FILES = ('N',): write_records raises unless the key sets are exactly N (C-ONLY-N; PLANT-ONLY-N: a D record added must raise"
    print "  before any file is opened). C-REP-B and C-REP-AK run over the scope against m3ref_v1_10's V3N. The plants of v1_8 (C-FMT, the"
    print "  reader plants, C-BOUND-RT, PLANT-NOWRITE) run on the N text."
    print "- The record is m3_s8v3_N_N<N>_J300_v1_8_2.json (m3_record_v4, read through m3_reader_v4_4); eng names m3_run_v1_8_2 and, as"
    print "  entries_by, m3_run_v1_8 with its full sha256; the extras 'scope' (the narrowed scope in words, against list v3) and 'scope_keys'"
    print "  (the 65 keys) say it is not the full N family."
    print "Everything else is m3_run_v1_8_1's. Its docstring follows."
    sub(/^"""m3_run_v1_8_1.py -- pk03 \(code\/pk03\/\)\. /, "m3_run_v1_8_1: ")
    print
    next
}
NR == 42 { need("ITEM_RE = r'(asmP)\\.(4|3)'"); print "ITEM_RE = r'(asmN)\\.(4|3)'"; next }
NR == 44 { need("print('usage: m3_run_v1_8_1.py ITEM LIM"); print "    print('usage: m3_run_v1_8_2.py ITEM LIM   (ITEM = asmN.4 or asmN.3; LIM = RLIMIT_CPU soft limit in s, 5..540)')"; next }
NR == 196 { need("out('m3_run_v1_8_1 item %s LIM %d; script sha256 %s; python %s'"); sub(/out\('m3_run_v1_8_1 item/, "out('m3_run_v1_8_2 item"); print; next }
NR == 696 { need("FILES = ('D', 'E2', 'E3', 'FF')"); print "FILES = ('N',)   # asmN: the N record on route B's scope, nothing else"; next }
NR == 703 {
    need("raise ValueError('asmP writes exactly the records of %s and never an N record, not %s'")
    print "        raise ValueError('asmN writes exactly the record of %s (the N family on route B\\'s scope), not %s' % (FILES, sorted(set(texts) | set(paths))))"
    next
}
NR == 717 {
    need("def walk_pieces(graph, res):")
    while ((getline ln < B) > 0) print ln
    close(B)
    next
}
NR > 717 && NR <= 901 { next }
NR == 902 { if ($0 != "") { print "BUILD ERROR line 902: expected the blank line after run_asm"; bad = 1; exit 1 } print; next }
{ print }
END { if (bad) exit 1 }
