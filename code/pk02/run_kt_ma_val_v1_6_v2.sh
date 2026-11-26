#!/bin/bash
# run_kt_ma_val_v1_6_v2.sh -- pk02 (code/pk02/). The validation of record of arbeng_ma_v1_4 (2c0a7338): kt_ma_val_v1_6.py (e182d503)
# on the approval for item (iii) (compute cap 0.8 core-h for item (iii); 726.8 s went to hand tests, so this run gets 2150 s), bundle MANIFEST_ARBENG_MA_v1_4.sha256 (whose own sha256 must start 8d1a2fcf;
# every entry by sha256sum -c --strict). ONE JOB AT A TIME, in this order: v3, v4, v1, v2 (v1_5's pieces on v1_4), cmp (C-V15SAME), v5, v6,
# v7s, then v7u0, v7u1, ... (at most 6) until level 16 of the D16 table is assembled, then v7f. Address space: v1 12 GiB, the others 8 GiB;
# every piece LIM 540. A piece starts only if the CPU of this run's outputs so far (user + system from /usr/bin/time -v) + 546 <= 2150.
# Stops at the first piece whose VERDICT lines are not exactly ["VERDICT VALID"] (or whose output path exists), and if root free space is
# below 886 GiB or MemAvailable below 24 GiB. One line per step in out/run_kt_ma_val_v1_6_v2.log; outputs out/out_kt_ma_val_v1_6_<piece>.out
# and .err (444); the D16 state in out/val16_state (about 3.5 GB).
D=/mnt/g2/release/root/code/pk02
L=$D/out/run_kt_ma_val_v1_6_v2.log
M=$D/MANIFEST_ARBENG_MA_v1_4.sha256
F=$D/kt_ma_val_v1_6.py
CAP=2150
shopt -s nullglob
stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
M8=$(sha256sum "$M" < /dev/null | cut -c1-8)
if [ "$M8" != 8d1a2fcf ]; then echo "SHA MISMATCH manifest $M8 $(stamp)" >> "$L"; exit 3; fi
if ! sha256sum -c --quiet --strict "$M" < /dev/null > /dev/null 2>&1; then echo "SHA MISMATCH: a file in the manifest differs $(stamp)" >> "$L"; exit 3; fi
for s in kt_ma_val_v1_6.py arbeng_ma_v1_4.py; do
  pin=$(awk -v p="$D/$s" '$2 == p {print $1}' "$M")
  if [ -z "$pin" ] || [ "$pin" != "$(sha256sum "$D/$s" < /dev/null | cut -c1-64)" ]; then echo "SHA MISMATCH $s $(stamp)" >> "$L"; exit 3; fi
done
echo "SHA OK manifest $M8 (every entry, --strict; kt_ma_val_v1_6, arbeng_ma_v1_4 in it) $(stamp)" >> "$L"
cpuof() { awk -F': ' '/User time \(seconds\)|System time \(seconds\)/ {s += $2} END {printf "%.1f", s + 0}' "$@" /dev/null; }
used() { local errs; errs=("$D"/out/out_kt_ma_val_v1_6_*.err); cpuof "${errs[@]}"; }
rootok() { df -B1 --output=avail / | awk 'NR == 2 {ok = ($1 >= 886 * 1073741824)} END {exit !ok}'; }
memok() { awk '/^MemAvailable:/ {ok = ($2 >= 24 * 1048576)} END {exit !ok}' /proc/meminfo; }
piece() {
  local p=$1 as=$2 o e u rc
  o=$D/out/out_kt_ma_val_v1_6_$p.out; e=${o%.out}.err
  for f in "$o" "$e"; do if [ -e "$f" ]; then echo "EXISTS ${f##*/} $(stamp)" >> "$L"; exit 4; fi; done
  u=$(used)
  if ! awk -v u="$u" -v c="$CAP" 'BEGIN {exit !(u + 546 <= c)}'; then echo "CAP-GUARD: used $u s before $p, cap $CAP s $(stamp)" >> "$L"; exit 6; fi
  if ! rootok; then echo "DISK-GUARD before $p $(stamp)" >> "$L"; exit 7; fi
  if ! memok; then echo "MEM-GUARD before $p $(stamp)" >> "$L"; exit 7; fi
  echo "launch $p AS $as $(stamp); used $u s" >> "$L"
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 OMP_NUM_THREADS=1 timeout 580 nice -n 10 /usr/bin/time -v prlimit --as="$as" -- \
    python3 -I -B "$F" "$p" 540 > "$o" 2> "$e"
  rc=$?
  chmod 444 "$o" "$e"
  echo "$p rc $rc cpu $(cpuof "$e") s peak RSS $(awk -F': ' '/Maximum resident set size \(kbytes\)/ {printf "%.0f", $2 / 1024}' "$e") MiB, bytes $(($(stat -c %s "$o") + $(stat -c %s "$e"))) $(stamp)" >> "$L"
  awk '/^(C-|PLANT-|QC|V7 |ERROR)/ && !/^C-TREE|^C-HASH/ {print "  " substr($0, 1, 230)}' "$o" >> "$L"
  if [ "$(awk '/^VERDICT/' "$o")" != "VERDICT VALID" ]; then echo "STOP: $p not VALID ($(awk '/^VERDICT/' "$o" | head -c 200)) $(stamp)" >> "$L"; exit 5; fi
  echo "$p VALID $(stamp); used $(used) s of $CAP" >> "$L"
}
echo "start $(stamp); used $(used) s" >> "$L"
piece v3 8589934592
piece v4 8589934592
piece v1 12884901888
piece v2 8589934592
piece cmp 8589934592
piece v5 8589934592
piece v6 8589934592
piece v7s 8589934592
for i in 0 1 2 3 4 5; do
  [ -e "$D/out/val16_state/handoff_level_k16.json" ] && break
  piece "v7u$i" 8589934592
done
if [ ! -e "$D/out/val16_state/handoff_level_k16.json" ]; then echo "STOP: level 16 not assembled after the v7u jobs $(stamp)" >> "$L"; exit 5; fi
piece v7f 8589934592
echo "DONE $(stamp); used $(used) s of $CAP" >> "$L"
