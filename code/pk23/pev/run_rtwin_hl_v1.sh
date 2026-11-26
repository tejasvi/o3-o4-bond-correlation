#!/bin/bash
# run_rtwin_hl_v1.sh (pk23, option B Pev entries): one guarded run of pk23/pev/rtwin_hl_v1.py per argument, in the order given.
# Usage: run_rtwin_hl_v1.sh LIM ASGIB CAP ITEM...   (ITEM = L|LH|LT|LB.<N>; LIM = the script's RLIMIT_CPU in s, timeout LIM + 60;
# prlimit --as ASGIB GiB; guard cap CAP core-h). The script writes pk23/pev/out/rtwin_hl_v1_<ITEM>_z9sym.out itself (mode x); stdout
# and stderr go to pk23/pev/out/rtwin_hl_v1_<ITEM>.log (noclobber). Stops at the first item whose guard rc is not 0 or whose VERDICT
# lines are not exactly [VERDICT VALID] (exit 4), or if an output exists (exit 3). Log: pk23/pev/rtwin_hl_v1.log.
set -u
H=/mnt/g2/release/root/code/pk23
B=$H/pev
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
LOG=$B/rtwin_hl_v1.log
LIM=$1; AS=$(( $2 * 1024 * 1024 * 1024 )); CAP=$3; shift 3
set -o noclobber
say() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> "$LOG"; }
say "run start LIM $LIM AS $AS CAP $CAP items $* script sha256 $(sha256sum $B/rtwin_hl_v1.py | cut -c1-16)"
for IT in "$@"; do
  O=$B/out/rtwin_hl_v1_${IT}_z9sym.out
  E=$B/out/rtwin_hl_v1_${IT}.log
  if [ -e "$O" ] || [ -e "$E" ]; then say "output exists: $O"; exit 3; fi
  say "start $IT"
  python3 -I -B $G $B/PK23_GUARD_pev_rtwin_$IT.log $CAP --run -- env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TMPDIR=$B/out \
    timeout $((LIM + 60)) nice -n 10 prlimit --as=$AS -- bash -c "cd $B && $PY -I -B $B/rtwin_hl_v1.py $IT $LIM > $E 2>&1"
  rc=$?
  V=$(awk '/^VERDICT/' "$O")
  say "end $IT rc $rc verdict [$V] $(awk '/^ITEM/' "$O") guard $(awk '/guard exits|after kill/ {print $NF, $(NF-1)}' $B/PK23_GUARD_pev_rtwin_$IT.log)"
  if [ "$rc" != 0 ] || [ "$V" != "VERDICT VALID" ]; then say "stop: $IT rc $rc verdict [$V]"; exit 4; fi
done
say "run end: all items done"
