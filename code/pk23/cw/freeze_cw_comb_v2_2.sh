#!/bin/bash
# freeze_cw_comb_v2_2.sh (pk23, C_w): freeze_far_crude_xy_v1_1.sh's form for MANIFEST_CW_COMB_V2_2_v1. Runs sha256sum -c on the manifest
# first (stops unless every row is OK), then chmod a-w on every path in cw/out/MANIFEST_CW_COMB_V2_2_v1.frozen.txt and on the manifest and
# that list; then counts the frozen paths still writable by anyone (must be 0). The writable rows (guard logs, SCRATCH, DRY and lineage
# files) stay as they are. Run it with its guard log outside the manifest's globs (pk23/guard/PK23_GUARD_freeze_cw22.log).
# Usage: bash freeze_cw_comb_v2_2.sh
set -u
B=/mnt/g2/release/root/code/pk23
M=$B/cw/MANIFEST_CW_COMB_V2_2_v1.sha256
F=$B/cw/out/MANIFEST_CW_COMB_V2_2_v1.frozen.txt
cd $B || exit 2
bad=$(sha256sum -c $M 2>&1 | awk '!/: OK$/ {b++} END {print b+0}')
if [ "$bad" != 0 ]; then echo "manifest check: $bad rows not OK; nothing frozen"; exit 4; fi
mapfile -t fz < $F
[ "${#fz[@]}" -gt 0 ] || { echo "the frozen list is empty; nothing frozen"; exit 5; }
chmod a-w "${fz[@]}" $M $F
left=$(find "${fz[@]}" $M $F -perm /222 | awk 'END{print NR}')
echo "FROZEN $(( ${#fz[@]} + 2 )) paths; still writable: $left; manifest check before the freeze: all $(awk 'END{print NR}' $M) rows OK"
