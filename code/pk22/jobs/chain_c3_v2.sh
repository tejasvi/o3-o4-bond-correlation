#!/bin/bash
# chain_c3_v2.sh (pk22, phase (iii) steps A3-A5): chain_c3_v1.sh for runner c3_1 (m3/m3_run_v1_9_3_px22_c3_1.py; CS4 smoke parts CS4a1..CS4a4 are single items) in the order given, one guarded job
# per item (1 core, timeout 580, LIM 540, prlimit 8 GiB, guard cap 0.2 core-h, which leaves the 60 s margin), sequential. An argument is
#   <X>a.<N>, <X>r1.<N>, <X>r2.<N>, asm.<N>   one item;
#   <Y>p.<N>   the prep pieces <Y>p1.<N>, <Y>p2.<N>, ... until one prints 'PREP16 <Y> piece <k>: DONE;' (at most 19);
#   <X>k.<N>   the entry pieces <X>k1.<N>, ... until one prints C-PIECE with 'entries <s>..<m> of <n> done, next <n>' (at most 9).
# Bytes (each local job writes at most about 1 GB): before each item the root must have at least 935 GiB free, and after
# it the folder pk22/m3/out (records, memos, out/tab16c tables) must have grown by at most 1.0e9 bytes; the priced growth is a few MB
# per smoke or entry piece and tens of MB per prep piece of the 9- and 6-vertex graphs (no 12-vertex prep runs here: CS4 and H4T read the
# shared S4 and H preps).
# Stops (distinct exit codes) at the first item whose guard rc is not 0 or whose VERDICT lines are not exactly [VERDICT VALID] (4), at a
# piece limit (5), if an output exists (3), when STOP_chain_c3v2 exists (6), on the free-space floor (7) or on the per-item byte cap (8);
# PAUSE_chain_c3v2 holds it between items. Log: chain_c3_v2.log. Usage: chain_c3_v2.sh ARG...
set -u
B=/mnt/g2/release/root/code/pk22
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
SCR=$B/m3/m3_run_v1_9_3_px22_c3_1.py
OD=$B/m3/out
LOG=$B/jobs/chain_c3_v2.log
set -o noclobber
say() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> "$LOG"; }
run1() {   # run one item; sets V (verdict lines) and O (output path); returns 0 when the item ran clean
  local IT=$1
  if [ -e $B/jobs/STOP_chain_c3v2 ]; then say "STOP file seen before $IT"; exit 6; fi
  while [ -e $B/jobs/PAUSE_chain_c3v2 ]; do sleep 20; if [ -e $B/jobs/STOP_chain_c3v2 ]; then say "STOP while paused"; exit 6; fi; done
  local AV=$(df -B1 --output=avail / | awk 'NR == 2 {print $1}')
  if [ "$AV" -lt $((935 * 1024 * 1024 * 1024)) ]; then say "stop: root free $AV bytes below 935 GiB"; exit 7; fi
  O=$OD/m3_run_v1_9_3_$IT.out
  local E=$OD/m3_run_v1_9_3_$IT.err
  if [ -e "$O" ] || [ -e "$E" ]; then say "output exists: $O"; exit 3; fi
  local T0=$(du -sb $OD | cut -f1)
  say "start $IT"
  python3 -I -B $G $B/guard/W1_GUARD_c3v2_$IT.log 0.2 --run -- env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TMPDIR=$B/m3/tmp timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B $SCR $IT 540 > "$O" 2> "$E"
  local rc=$?
  local T1=$(du -sb $OD | cut -f1)
  V=$(awk '/^VERDICT/' "$O")
  say "end $IT rc $rc verdict [$V] cpu $(awk '/^STAGE-CPU total/ {print $3}' "$O") out +$((T1 - T0)) bytes guard $(awk '/guard exits/ {print $NF, $(NF-1)}' $B/guard/W1_GUARD_c3v2_$IT.log)"
  if [ $((T1 - T0)) -gt 1000000000 ]; then say "stop: $IT wrote $((T1 - T0)) bytes, above 1.0e9"; exit 8; fi
  if [ "$rc" != 0 ] || [ "$V" != "VERDICT VALID" ]; then say "stop: $IT rc $rc verdict [$V]"; exit 4; fi
}
say "chain start $* script sha256 $(sha256sum $SCR | cut -c1-16)"
for A in "$@"; do
  if [[ "$A" =~ ^(CE3|E2T)p\.([34])$ ]]; then
    Y=${BASH_REMATCH[1]}; NN=${BASH_REMATCH[2]}; k=1
    while :; do
      if [ "$k" -gt 19 ]; then say "prep piece limit passed for $Y N=$NN"; exit 5; fi
      run1 ${Y}p$k.$NN
      if awk -v k=$k -v y=$Y '$0 ~ "^PREP16 " y " piece " k ": DONE;" {f = 1} END {exit !f}' "$O"; then say "$Y prep N=$NN DONE at piece $k"; break; fi
      k=$((k + 1))
    done
  elif [[ "$A" =~ ^(CS4|CE3|H4T|E2T)k\.([34])$ ]]; then
    X=${BASH_REMATCH[1]}; NN=${BASH_REMATCH[2]}; k=1
    while :; do
      if [ "$k" -gt 9 ]; then say "entry piece limit passed for $X N=$NN"; exit 5; fi
      run1 ${X}k$k.$NN
      if awk '/^C-PIECE/ && match($0, /entries [0-9]+\.\.-?[0-9]+ of [0-9]+ done, next [0-9]+/) {s = substr($0, RSTART, RLENGTH); split(s, w, " "); if (w[4] == w[7]) f = 1} END {exit !f}' "$O"; then say "$X entries N=$NN all done at piece $k"; break; fi
      k=$((k + 1))
    done
  else
    run1 "$A"
  fi
done
say "chain end: all arguments done"
