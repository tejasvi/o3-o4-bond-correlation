#!/bin/bash
# chain_rcc_v6.sh (pk22, phase (iii), NE's certified RC engine v1_5): chain_rcc_v5.sh (33db2536) for
# w1/rc_cert/kt_s8h_rcc_v1_5.py: runs its items in the order given, one guarded job per item (1 core, timeout 580, LIM 540, prlimit 8 GiB,
# guard cap 0.2 core-h, which leaves the 60 s margin), sequential. An argument is MODE:smoke:N, MODE:chunk:N:a:b, MODE:final:N or
# MODE:record (MODE dev or cert). Bytes: before each item the root must have at least 935 GiB free, and the item's output folder
# (w1/rc_cert/out) must grow by at most 1.0e9 bytes; a single output file is capped at 10 MiB by the S8 module copy's RLIMIT_FSIZE, so
# chunks hold at most about 80 pieces at N = 4 (v1_5 prints the class-level balls). Stops (distinct exit codes) at the first item whose guard rc is not 0 or whose VERDICT lines are
# not exactly [VERDICT VALID] (4), if its output exists (3), when STOP_chain_rcc exists (6), on the free-space floor (7) or on the byte
# cap (8); PAUSE_chain_rcc holds it between items. Log: chain_rcc_v6.log. Usage: chain_rcc_v6.sh ARG...
set -u
B=/mnt/g2/release/root/code/pk22
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
SCR=$B/w1/rc_cert/kt_s8h_rcc_v1_5.py
OD=$B/w1/rc_cert/out
LOG=$B/jobs/chain_rcc_v6.log
set -o noclobber
say() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> "$LOG"; }
say "chain start $* script sha256 $(sha256sum $SCR | cut -c1-16)"
for A in "$@"; do
  IFS=: read -r MD IT P1 P2 P3 <<< "$A"
  case "$IT" in
    smoke|final) ARGS="$MD $IT 540 $P1"; SFX="${IT}_n$P1" ;;
    chunk) ARGS="$MD chunk 540 $P1 $P2 $P3"; SFX=$(printf 'c%d_%04d_%04d' "$P1" "$P2" "$P3") ;;
    record) ARGS="$MD record 540"; SFX="record" ;;
    *) say "bad argument $A"; exit 5 ;;
  esac
  if [ -e $B/jobs/STOP_chain_rcc ]; then say "STOP file seen before $A"; exit 6; fi
  while [ -e $B/jobs/PAUSE_chain_rcc ]; do sleep 20; if [ -e $B/jobs/STOP_chain_rcc ]; then say "STOP while paused"; exit 6; fi; done
  AV=$(df -B1 --output=avail / | awk 'NR == 2 {print $1}')
  if [ "$AV" -lt $((935 * 1024 * 1024 * 1024)) ]; then say "stop: root free $AV bytes below 935 GiB"; exit 7; fi
  O=$OD/out_kt_s8h_rcc_v1_5_${MD}_${SFX}.out
  if [ -e "$O" ]; then say "output exists: $O"; exit 3; fi
  T0=$(du -sb $OD | cut -f1)
  say "start $A"
  python3 -I -B $G $B/guard/W1_GUARD_rcc15_${MD}_${SFX}.log 0.2 --run -- env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B $SCR $ARGS > $OD/console15_${MD}_${SFX}.txt 2>&1
  rc=$?
  T1=$(du -sb $OD | cut -f1)
  V=$(awk '/^VERDICT/' "$O" 2>/dev/null)
  say "end $A rc $rc verdict [$V] $(awk '/^ITEM /{print $4, $5, $6, $7}' "$O" 2>/dev/null) out +$((T1 - T0)) bytes guard $(awk '/guard exits/ {print $NF, $(NF-1)}' $B/guard/W1_GUARD_rcc15_${MD}_${SFX}.log)"
  if [ $((T1 - T0)) -gt 1000000000 ]; then say "stop: $A wrote $((T1 - T0)) bytes, above 1.0e9"; exit 8; fi
  if [ "$rc" != 0 ] || [ "$V" != "VERDICT VALID" ]; then say "stop: $A rc $rc verdict [$V]"; exit 4; fi
done
say "chain end: all arguments done"
