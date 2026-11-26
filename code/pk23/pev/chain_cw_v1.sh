#!/bin/bash
# chain_cw_v1.sh (pk23, C_w variant B): chain_hl_v1_1.sh (38407fbf) for pk23's C_w runner pk23/pev/m3_run_v1_9_3_cw_v1.py (family
# LC, reading the certified L prep of m3_run_v1_9_3_hl_v1), in the order given, one guarded job per item (1 core, guard cap 0.2 core-h, or
# CAPV if set; LIM from LIMV (default 540), timeout LIM + 40, prlimit from ASV in GiB (default 32)), sequential. An argument is
#   LCa.<N>, LCr1.<N>, LCr2.<N>, asmc.<N>   one item;
#   LCk.<N>[@k]  the entry pieces LCk<k>.<N>, ... until one prints C-PIECE with 'entries <s>..<m> of <n> done, next <n>' (at most 9).
# Outputs pk23/pev/out/m3_run_v1_9_3_<item>.out and .err (noclobber). Before each item the root must have at least 1000 GiB free; the
# per-item byte cap is 12.0e9 (growth of pk23/pev/out). Stops (distinct exit codes) at the first item whose guard rc is not 0 or whose
# VERDICT lines are not exactly [VERDICT VALID] (4), at the piece limit (5), if an output exists (3), when pk23/pev/STOP_chain_cw exists
# (6), on the free-space floor (7) or on the byte cap (8); pk23/pev/PAUSE_chain_cw holds it between items. Log pk23/pev/chain_cw_v1.log.
# Usage: [LIMV=<s>] [ASV=<GiB>] [CAPV=<core-h>] chain_cw_v1.sh ARG...
set -u
H=/mnt/g2/release/root/code/pk23
B=$H/pev
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
SCR=$B/m3_run_v1_9_3_cw_v1.py
OD=$B/out
LOG=$B/chain_cw_v1.log
LIM=${LIMV:-540}
AS=$(( ${ASV:-32} * 1024 * 1024 * 1024 ))
CAP=${CAPV:-0.2}
set -o noclobber
say() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> "$LOG"; }
run1() {
  local IT=$1
  if [ -e $B/STOP_chain_cw ]; then say "STOP file seen before $IT"; exit 6; fi
  while [ -e $B/PAUSE_chain_cw ]; do sleep 20; if [ -e $B/STOP_chain_cw ]; then say "STOP while paused"; exit 6; fi; done
  local AV=$(df -B1 --output=avail / | awk 'NR == 2 {print $1}')
  if [ "$AV" -lt $((1000 * 1024 * 1024 * 1024)) ]; then say "stop: root free $AV bytes below 1000 GiB"; exit 7; fi
  O=$OD/m3_run_v1_9_3_$IT.out
  local E=${O%.out}.err
  if [ -e "$O" ] || [ -e "$E" ]; then say "output exists: $O"; exit 3; fi
  local T0=$(du -sb $OD | cut -f1)
  say "start $IT LIM $LIM AS $AS CAP $CAP"
  python3 -I -B $G $H/guard/PK23_GUARD_cw_$IT.log $CAP --run -- env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TMPDIR=$OD \
    timeout $((LIM + 40)) nice -n 10 prlimit --as=$AS -- bash -c "cd $B && $PY -I -B $SCR $IT $LIM > $O 2> $E"
  local rc=$?
  local T1=$(du -sb $OD | cut -f1)
  V=$(awk '/^VERDICT/' "$O")
  say "end $IT rc $rc verdict [$V] cpu $(awk '/^STAGE-CPU total/ {print $3}' "$O") out +$((T1 - T0)) bytes guard $(awk '/guard exits|after kill/ {print $NF, $(NF-1)}' $H/guard/PK23_GUARD_cw_$IT.log)"
  if [ $((T1 - T0)) -gt 12000000000 ]; then say "stop: $IT wrote $((T1 - T0)) bytes, above 12.0e9"; exit 8; fi
  if [ "$rc" != 0 ] || [ "$V" != "VERDICT VALID" ]; then say "stop: $IT rc $rc verdict [$V]"; exit 4; fi
}
say "chain start $* script sha256 $(sha256sum $SCR | cut -c1-16) chain sha256 $(sha256sum $0 | cut -c1-16)"
for A in "$@"; do
  if [[ "$A" =~ ^LCk\.([34])(@([0-9]+))?$ ]]; then
    NN=${BASH_REMATCH[1]}; k=${BASH_REMATCH[3]:-1}
    while :; do
      if [ "$k" -gt 9 ]; then say "entry piece limit passed for LC N=$NN"; exit 5; fi
      run1 LCk$k.$NN
      if awk '/^C-PIECE/ && match($0, /entries [0-9]+\.\.-?[0-9]+ of [0-9]+ done, next [0-9]+/) {s = substr($0, RSTART, RLENGTH); split(s, w, " "); if (w[4] == w[7]) f = 1} END {exit !f}' "$O"; then say "LC entries N=$NN done at piece $k"; break; fi
      k=$((k + 1))
    done
  elif [[ "$A" =~ ^(LCa|LCr1|LCr2|asmc)\.([34])$ ]]; then
    run1 "$A"
  else
    say "unknown argument $A"; exit 2
  fi
done
say "chain end: all arguments done"
