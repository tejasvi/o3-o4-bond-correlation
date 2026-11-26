#!/bin/bash
# make_cw_comb_manifest_v2_2.sh (pk23, C_w; the P0_LOG rows 4684, 4711): the release manifest of the certified CW_X11 record of
# cw_comb_v2_2 on pk25's P2 table 47cef0dd, on the pattern of pk23/it3/make_far_crude_xy_manifest_v1_1.sh. Run it, and
# freeze_cw_comb_v2_2.sh after it, with guard logs named outside the listed globs (pk23/guard/PK23_GUARD_manifest_cw22.log,
# PK23_GUARD_freeze_cw22.log). Writes pk23/cw/MANIFEST_CW_COMB_V2_2_v1.sha256 (noclobber), the sha256sum list (paths relative to
# pk23; check with: env -C pk23 sha256sum -c cw/MANIFEST_CW_COMB_V2_2_v1.sha256) of
#   FROZEN (a-w by freeze_cw_comb_v2_2.sh): the record cw/out/CW_X11_v2_2.kv, its run output, the producer cw_comb_v2_2 with its parent
#   cw_comb_v2_0, its maker make_cw_comb_v2_x4 (and x3, which x4 extends), the maker output, diff and syntax check; the P2 manifest check;
#   the token check and row compares (cmp_cw_x11_v1.awk and its output); the t-ball check and the arb division test with their outputs; the
#   syntax-check tool; the reader fork m3_reader_cw_v1_1 (pinned by the comb) with its maker, diff, maker output, check script and check
#   output; this script and the freeze script;
#   WRITABLE (listed only): the guard logs of pk23/cw, the SCRATCH selftests, the DRY versions v2_0 and v2_1 (records, outputs, v2_1's
#   code, diff and maker output), the refused first launch of v2_2 (an empty output and its assert), the unused makers x, x1, x2 and the
#   lineage tests (the x1 replacement test, the selftest shim, the static maker test, the arb union test).
# Every listing is a bash glob or a literal name (no ls, find or sort pipe); each listed path must be a file. Prints the manifest's
# sha256 and row counts. Usage: bash make_cw_comb_manifest_v2_2.sh
set -u
B=/mnt/g2/release/root/code/pk23
M=$B/cw/MANIFEST_CW_COMB_V2_2_v1.sha256
F=$B/cw/out/MANIFEST_CW_COMB_V2_2_v1.frozen.txt
set -o noclobber
cd $B || exit 2
if [ -e $M ] || [ -e $F ]; then echo "exists: $M or $F"; exit 3; fi
frozen=( cw/out/CW_X11_v2_2.kv cw/out/cw_comb_v2_2_a.out cw/out/cw_comb_v2_2_a.err cw/cw_comb_v2_2.py cw/cw_comb_v2_0.py
  cw/make_cw_comb_v2_x4.py cw/make_cw_comb_v2_x3.py cw/out/make_cw_comb_v2_2.out cw/out/make_cw_comb_v2_2.err cw/diff_cw_comb_v2_0_to_v2_2.txt
  cw/out/astcheck_cw_comb_v2_2.out cw/out/p2_v2_3_cert_check_v2_2.out cw/cmp_cw_x11_v1.awk cw/out/cmp_cw_x11_v2_2.out
  tools/test_tball_v2_2_v1.py cw/out/test_tball_v2_2_v1.out cw/out/test_tball_v2_2_v1.err cw/out/astcheck_test_tball_v2_2_v1.out
  tools/test_arb_div0_v1.py cw/out/test_arb_div0_v1.out cw/out/test_arb_div0_v1.err tools/astcheck_v1.py
  pev/m3_reader_cw_v1_1.py pev/make_m3_reader_cw_v1_1.py pev/diff_m3_reader_cw_v1_to_v1_1.txt pev/out/make_m3_reader_cw_v1_1.out
  pev/m3_reader_cw11_check_v1.py pev/out/m3_reader_cw11_check_v1.out cw/make_cw_comb_manifest_v2_2.sh cw/freeze_cw_comb_v2_2.sh )
writable=( cw/PK23_GUARD_* cw/out/SCRATCH_* cw/out/CW_X11_DRY_v2_0_a.kv cw/out/CW_X11_DRY_v2_1_a.kv cw/out/cw_comb_v2_0_dry_a.out
  cw/out/cw_comb_v2_1_dry_a.out cw/cw_comb_v2_1.py cw/diff_cw_comb_v2_0_to_v2_1.txt cw/out/make_cw_comb_v2_1.out cw/out/cw_comb_v2_2.out
  cw/out/cw_comb_v2_2.err cw/make_cw_comb_v2_x.py cw/make_cw_comb_v2_x1.py cw/make_cw_comb_v2_x2.py cw/test_make_v2x1_repl_v1.py
  cw/test_selftest_v2_shim_v1.py tools/test_maker_repl_v1.py tools/test_arb_union_v1.py )
for p in "${frozen[@]}" "${writable[@]}"; do [ -f "$p" ] || { echo "not a file: $p"; exit 5; }; done
r=$(awk '$1 == "RECORD" && $2 == "CW_X11_v2_2.kv" {print $3}' cw/out/cw_comb_v2_2_a.out)
[ "$r" = "$(sha256sum cw/out/CW_X11_v2_2.kv | cut -d' ' -f1)" ] || { echo "the record is not its run output's RECORD line"; exit 6; }
[ "$(awk '/^VERDICT|^STATUS/' cw/out/cw_comb_v2_2_a.out | tr '\n' '|')" = "VERDICT VALID|STATUS CERTIFIED (DRY inputs: none)|" ] || {
  echo "the run output's VERDICT and STATUS lines are not VALID and CERTIFIED"; exit 7; }
printf '%s\n' "${frozen[@]}" > $F
sha256sum "${frozen[@]}" "${writable[@]}" > $M
echo "MANIFEST $(sha256sum $M | cut -d' ' -f1) $M rows $(awk 'END{print NR}' $M) (frozen $(awk 'END{print NR}' $F), writable ${#writable[@]})"
echo "CHECK $(sha256sum -c $M 2>&1 | awk '/: OK$/ {o++} !/: OK$/ {b++} END {print o+0 " OK, " b+0 " not OK"}')"
