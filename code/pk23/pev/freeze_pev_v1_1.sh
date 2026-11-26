#!/bin/bash
# freeze_pev_v1_1.sh (pk23, option B Pev entries): freeze_pev_v1.sh for the v1_1 manifest. Runs sha256sum -c on the manifest first
# (stops unless every row is OK), then chmod a-w on every path in out/MANIFEST_PEV_L_RECORDS_v1_1.frozen.txt and on the manifest and that
# list themselves; then counts the frozen paths still writable by anyone (must be 0). The writable rows (logs) stay writable. Run it with
# its guard log outside the manifest's globs (pk23/guard/PK23_GUARD_freeze_pev11.log). Usage: bash freeze_pev_v1_1.sh
set -u
B=/mnt/g2/release/root/code/pk23/pev
M=$B/MANIFEST_PEV_L_RECORDS_v1_1.sha256
F=$B/out/MANIFEST_PEV_L_RECORDS_v1_1.frozen.txt
cd $B || exit 2
bad=$(sha256sum -c $M 2>&1 | awk '!/: OK$/ {b++} END {print b+0}')
if [ "$bad" != 0 ]; then echo "manifest check: $bad rows not OK; nothing frozen"; exit 4; fi
mapfile -t fz < $F
chmod a-w "${fz[@]}" $M $F
left=$(find "${fz[@]}" $M $F -perm /222 | awk 'END{print NR}')
echo "FROZEN $(( ${#fz[@]} + 2 )) paths; still writable: $left; manifest check before the freeze: all $(awk 'END{print NR}' $M) rows OK"
