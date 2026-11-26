#!/bin/bash
# chain_float_c3_v2.sh (pk22, phase (iii) step A2): chain_float_c3_v1.sh for the float twin m3ref_px22_v1_5.py, with FAMILY:N items on the command
# line (each from piece 1, in the order given) instead of families run at N = 4 then N = 3; STOP/PAUSE files and the log carry v2.
# staged pieces, one guarded job per piece (1 core, timeout 580, prlimit 8 GiB, guard cap 0.2 core-h, which leaves the 60 s margin above
# the piece's 540 s), sequential: per family N = 4 from piece 1 until a piece prints P16-DONE, then N = 3 likewise.
# Bytes (each local job writes at most about 1 GB): before each piece the root must have at least 935 GiB free (the
# part stops sit at 930/920 GiB), and after it the P16 cache pk22/m3/out/tab16 must have grown by at most 1.0e9 bytes; the priced
# growth is 0 for tables adopted under their keys and about 0.64e9 for a 12-vertex graph's D16 + D14 vertex tables at a new N.
# Stops (distinct exit codes) at the first piece whose guard rc is not 0 (4), whose VERDICT lines are not exactly [VERDICT VALID] (4),
# that prints neither P16-DONE nor PREP-PARTIAL (4), at piece 9 (5), if an output exists (3), when STOP_chain_float_c3v2 exists (6), on
# the free-space floor (7) or on the per-piece byte cap (8); PAUSE_chain_float_c3v2 holds it between pieces. Log: chain_float_c3_v2.log.
# Usage: chain_float_c3_v2.sh FAMILY:N...
set -u
B=/mnt/g2/release/root/code/pk22
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
SCR=$B/m3/m3ref_px22_v1_5.py
TAB=$B/m3/out/tab16
LOG=$B/jobs/chain_float_c3_v2.log
set -o noclobber
say() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> "$LOG"; }
say "chain start families $* script sha256 $(sha256sum $SCR | cut -c1-16)"
for FN in "$@"; do
  F=${FN%%:*}; NN=${FN##*:}
  for ONCE in 1; do
    P=1
    while :; do
      if [ -e $B/jobs/STOP_chain_float_c3v2 ]; then say "STOP file seen before $F.$NN.p$P"; exit 6; fi
      while [ -e $B/jobs/PAUSE_chain_float_c3v2 ]; do sleep 20; if [ -e $B/jobs/STOP_chain_float_c3v2 ]; then say "STOP while paused"; exit 6; fi; done
      if [ "$P" -gt 9 ]; then say "piece limit passed at $F N=$NN"; exit 5; fi
      AV=$(df -B1 --output=avail / | awk 'NR == 2 {print $1}')
      if [ "$AV" -lt $((935 * 1024 * 1024 * 1024)) ]; then say "stop: root free $AV bytes below 935 GiB"; exit 7; fi
      IT=$F.$NN.p$P
      O=$B/m3/out/m3ref_px22_v1_5_${IT}_z9sym.out
      E=$B/m3/out/m3ref_px22_v1_5_${IT}_z9sym.err
      if [ -e "$O" ] || [ -e "$E" ]; then say "output exists: $O"; exit 3; fi
      T0=$(du -sb $TAB | cut -f1)
      say "start $IT (tab16 $T0 bytes, root free $AV bytes)"
      python3 -I -B $G $B/guard/W1_GUARD_chainc3v2_$IT.log 0.2 --run -- env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TMPDIR=$B/m3/tmp timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B $SCR $IT 540 z9sym > "$O" 2> "$E"
      rc=$?
      T1=$(du -sb $TAB | cut -f1)
      V=$(awk '/^VERDICT/' "$O")
      D=$(awk '/^P16-DONE/ {d=1} /^PREP-PARTIAL/ {p=1} END {if (d) print "DONE"; else if (p) print "PARTIAL"; else print "OTHER"}' "$O")
      C=$(awk '/^STAGE-CPU total/ {print $3}' "$O")
      say "end $IT rc $rc verdict [$V] prep [$D] cpu $C tab16 +$((T1 - T0)) bytes guard $(awk '/guard exits/ {print $NF, $(NF-1)}' $B/guard/W1_GUARD_chainc3v2_$IT.log)"
      if [ $((T1 - T0)) -gt 1000000000 ]; then say "stop: piece wrote $((T1 - T0)) bytes into tab16, above 1.0e9"; exit 8; fi
      if [ "$rc" != 0 ]; then say "stop: rc $rc"; exit 4; fi
      if [ "$V" != "VERDICT VALID" ]; then say "stop: verdict"; exit 4; fi
      if [ "$D" = DONE ]; then say "$F N=$NN DONE at piece $P"; break; fi
      if [ "$D" != PARTIAL ]; then say "stop: piece end [$D]"; exit 4; fi
      P=$((P + 1))
    done
  done
done
say "chain end: all families done"
