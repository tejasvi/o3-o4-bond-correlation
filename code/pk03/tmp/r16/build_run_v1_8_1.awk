# build_run_v1_8_1.awk -- pk03. Writes m3_run_v1_8_1.py from m3_run_v1_8.py (7d72fc7f): the partial asm (option 5). Every changed
# line is checked against a substring of the original before it is changed; any mismatch prints BUILD ERROR and exits 1.
# Usage: awk -f build_run_v1_8_1.awk m3_run_v1_8.py > m3_run_v1_8_1.py
function need(s) { if (index($0, s) == 0) { print "BUILD ERROR line " NR ": expected " s; bad = 1; exit 1 } }
NR == 2 {
    need("\"\"\"m3_run_v1_8.py -- pk03 (code/pk03/). The CERTIFIED entries")
    print "\"\"\"m3_run_v1_8_1.py -- pk03 (code/pk03/). REVISION of m3_run_v1_8.py (7d72fc7f) for option 5: one item,"
    print "asmP.N, the partial assembly of the families that are done (D, E2, FF and E3) while the N family's pieces still run. What changes:"
    print "- ITEM_RE accepts asmP.4 and asmP.3 only, so this script computes no entry and writes no hand-off."
    print "- Every hand-off it reads is m3_run_v1_8's: read_handoff binds each to m3_run_v1_8's full sha256 (V18_SHA, put in OWNMOD so C-HASH"
    print "  checks the file), and walk_pieces' piece_state accepts a capped piece only as a clean CAP-STOP of m3_run_v1_8. Entries come only"
    print "  from VALID hand-offs, as in m3_run_v1_8's asm."
    print "- FILES = (D, E2, E3, FF): the asm does not walk the N pieces, and write_records raises on any other key set, so no N record can be"
    print "  written (C-NO-N; PLANT-NO-N: an added N record must raise before any file is opened). C-SCOPE, C-REP-B and C-REP-AK run over the"
    print "  four families against m3ref_v1_10, as before."
    print "- The records are m3_s8v3_<D|E2|E3|FF>_N<N>_J300_v1_8_1.json (m3_record_v4, read through m3_reader_v4_4 as before); eng names"
    print "  m3_run_v1_8_1 and, as entries_by, m3_run_v1_8 with its full sha256; the extra 'partial' says the N family is not assembled."
    print "Everything else is m3_run_v1_8's. Its docstring follows."
    sub(/^"""m3_run_v1_8.py -- pk03 \(code\/pk03\/\)\. /, "m3_run_v1_8: ")
    print
    next
}
NR == 30 { need("ITEM_RE = r'(D|E2|FF|E3u"); print "ITEM_RE = r'(asmP)\\.(4|3)'"; next }
NR == 32 { need("print('usage: m3_run_v1_8.py ITEM LIM"); print "    print('usage: m3_run_v1_8_1.py ITEM LIM   (ITEM = asmP.4 or asmP.3; LIM = RLIMIT_CPU soft limit in s, 5..540)')"; next }
NR == 105 {
    if ($0 != "}") { print "BUILD ERROR line 105: expected the end of OWNMOD"; bad = 1; exit 1 }
    print
    print "V18_SHA = 'be0c1be3eadabf2f14f40d84f7a2482f2b75aada522b0e267146008cd700da3b'   # m3_run_v1_8.py, the producer of every hand-off asmP reads"
    print "OWNMOD['m3_run_v1_8.py'] = V18_SHA"
    next
}
NR == 182 { need("out('m3_run_v1_8 item %s LIM %d; script sha256 %s; python %s'"); sub(/out\('m3_run_v1_8 item/, "out('m3_run_v1_8_1 item"); print; next }
NR == 525 { need("{'script': SELF_SHA, 'item': item, 'N': NN, 'family': fam}"); sub(/'script': SELF_SHA/, "'script': V18_SHA"); print; next }
NR == 627 { need("m.group(3) == SELF_SHA and HO.verdict_ok(lines, CAPPED)"); sub(/m\.group\(3\) == SELF_SHA/, "m.group(3) == V18_SHA"); print; next }
NR == 682 { need("FILES = ('D', 'N', 'E2', 'E3', 'FF')"); print "FILES = ('D', 'E2', 'E3', 'FF')   # asmP: the N family is not assembled"; next }
NR == 687 {
    need("plant so far has fired and the TAG is certified; returns [(file key, path)] written, or [] when it refuses.")
    print
    print "    if set(texts) != set(FILES) or set(paths) != set(FILES):"
    print "        raise ValueError('asmP writes exactly the records of %s and never an N record, not %s' % (FILES, sorted(set(texts) | set(paths))))"
    next
}
NR == 733 { need("walk_pieces('N', res)"); print "    # asmP: the N pieces are not walked (option 5)"; next }
NR == 735 { need("for graph in REFOUT:"); print "    for graph in [g_ for g_ in REFOUT if g_ != 'N']:"; next }
NR == 746 || NR == 757 { need("for e in V3:"); print "    for e in [x for x in V3 if x['graph'] != 'N']:"; next }
NR == 753 { need("(the five files hold exactly"); sub(/the five files/, "the four files"); print; next }
NR == 778 { need("eng = {'m3_run_v1_8': SELF_SHA, 'modules': dict(OWNMOD)}"); print "    eng = {'m3_run_v1_8_1': SELF_SHA, 'entries_by': 'm3_run_v1_8.py:' + V18_SHA, 'modules': dict(OWNMOD)}"; next }
NR == 782 { need("for gr in ('D', 'N', 'mix', 'E3', 'free2')}"); sub(/\('D', 'N', 'mix', 'E3', 'free2'\)/, "('D', 'mix', 'E3', 'free2')"); print; next }
NR == 785 {
    need("'graph': f, 'graph_m3': GMAP[f]}")
    sub(/'graph_m3': GMAP\[f\]\}/, "'graph_m3': GMAP[f],")
    print
    print "                 'partial': 'asmP of m3_run_v1_8_1: the D, E2, E3 and FF records only; the N family is not assembled'}"
    next
}
NR == 788 { need("'m3_s8v3_%s_N%d_J300%s_v1_8.json'"); sub(/_v1_8\.json'/, "_v1_8_1.json'"); print; next }
NR == 871 {
    need("refused, len(opened)))")
    print
    print "    gate('C-NO-N', set(texts) == set(FILES) == {'D', 'E2', 'E3', 'FF'} and not any(os.path.basename(p).startswith('m3_s8v3_N_') for p in paths.values()),"
    print "         '(asmP writes the D, E2, E3 and FF records only: %s)' % ', '.join(os.path.basename(paths[f]) for f in FILES))"
    print "    try:"
    print "        write_records(dict(texts, N=texts['D']), dict(paths, N=os.path.join(OUTD, 'm3_s8v3_N_N%d_J300_v1_8_1.json' % NN)), [], [], '', opener=no_open)"
    print "        plant('PLANT-NO-N', False, '(write_records with an N record added must raise before opening any file)')"
    print "    except ValueError:"
    print "        plant('PLANT-NO-N', not opened, '(write_records with an N record added raises before opening any file)')"
    next
}
{ print }
END { if (bad) exit 1 }
