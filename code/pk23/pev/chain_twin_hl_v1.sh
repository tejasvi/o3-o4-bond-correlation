#!/bin/bash
# chain_twin_hl_v1.sh (pk23, option B Pev entries): the float twin's P16L prep pieces at one N, p1, p2, ... until a piece prints
# "P16-DONE piece <k> of P16L N=<N>" (at most 9 pieces). One guarded job per piece (cap 0.2 core-h, LIM 540 s, timeout 600 s, prlimit
# 16 GiB, one thread), run inside pk23/pev (a subshell cd), TRIAL z9sym; outputs pk23/pev/out/m3ref_hl_v1_P16L.<N>.p<k>_z9sym.out
# and .err (noclobber). Stops (distinct exit codes) when an output exists (3), a piece's guard rc is not 0 or its last VERDICT line is
# not VERDICT VALID (4), after 9 pieces (5), when pk23/pev/STOP_twin exists (6), when root free space is below 1000 GiB (7), or when a
# piece grows pk23/pev/out by more than 4 GB (8). Log: pk23/pev/chain_twin_hl_v1_N<N>.log. Usage: chain_twin_hl_v1.sh 4|3
set -u
NN=${1:-}
case "$NN" in 3|4) ;; *) echo "usage: chain_twin_hl_v1.sh 4|3"; exit 2 ;; esac
H=/mnt/g2/release/root/code/pk23
P=$H/pev
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
SCR=$P/m3ref_hl_v1.py
LOG=$P/chain_twin_hl_v1_N$NN.log
say() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> "$LOG"; }
say "chain start N=$NN script sha256 $(sha256sum "$SCR" | cut -c1-16)"
for k in 1 2 3 4 5 6 7 8 9; do
  [ -e "$P/STOP_twin" ] && { say "STOP file seen before piece $k"; exit 6; }
  AV=$(df -B1 --output=avail / | awk 'NR == 2 {print $1}')
  [ "$AV" -ge $((1000 * 1024 * 1024 * 1024)) ] || { say "stop: root free $AV bytes below 1000 GiB"; exit 7; }
  IT=P16L.$NN.p$k
  O=$P/out/m3ref_hl_v1_${IT}_z9sym.out; E=${O%.out}.err
  { [ -e "$O" ] || [ -e "$E" ]; } && { say "output exists: $O"; exit 3; }
  T0=$(du -sb "$P/out" | cut -f1)
  say "start $IT"
  python3 -I -B "$G" "$H/guard/PK23_GUARD_pev_twin_$IT.log" 0.2 --run -- env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    TMPDIR=$P/out timeout 600 nice -n 10 prlimit --as=17179869184 -- \
    bash -c "cd $P && set -o noclobber && $PY -I -B $SCR $IT 540 z9sym > $O 2> $E"
  rc=$?
  T1=$(du -sb "$P/out" | cut -f1)
  V=$(awk '/^VERDICT/ {v = $0} END {print v}' "$O")
  say "end $IT rc $rc [$V] $(awk '/^STAGE-CPU total/ {print $0}' "$O") out +$((T1 - T0)) bytes guard $(awk '/guard exits|after kill/ {print $NF, $(NF-1)}' "$H/guard/PK23_GUARD_pev_twin_$IT.log")"
  [ $((T1 - T0)) -gt 4000000000 ] && { say "stop: $IT grew out by $((T1 - T0)) bytes"; exit 8; }
  { [ "$rc" = 0 ] && [ "$V" = "VERDICT VALID" ]; } || { say "stop: $IT rc $rc [$V]"; exit 4; }
  if awk -v k=$k -v n=$NN '$0 ~ "^P16-DONE piece " k " of P16L N=" n "$" {f = 1} END {exit !f}' "$O"; then say "P16L N=$NN DONE at piece $k"; exit 0; fi
done
say "stop: 9 pieces without P16-DONE"
exit 5
