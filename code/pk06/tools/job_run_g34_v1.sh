#!/bin/bash
# job_run_g34_v1.sh NAME CAP MARGIN LIM WALL -- K ROWS COLS N J1 ORBS SIGS [CONTROLS [MEMSTOP]]
# pk06: one engine run (mode grid) under coreh_guard_v2 --run and the wrapper; writes runs/NAME.out, .err, .guard.log (noclobber)
P=/mnt/g2/release/root/code/pk06
E=$P/kt_lbu_g34_pk06_v1.py
G=/mnt/g2/guard/coreh_guard_v2.py
PYB=python3
NICE="nice -n 10"
name=$1; cap=$2; margin=$3; lim=$4; wall=$5; shift 5
[ "$1" = "--" ] && shift
case "$name" in ""|*[!A-Za-z0-9_]*) echo "bad name"; exit 2;; esac
O=$P/runs/$name
set -C
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=$P/tmp
ulimit -c 0
$NICE prlimit --as=8589934592 -- $PYB -I -B "$G" "$O.guard.log" "$cap" --margin "$margin" --run -- \
  timeout "$wall" $NICE prlimit --as=8589934592 --cpu=$((lim + 2)) -- $PYB -I -B "$E" grid "$lim" "$@" > "$O.out" 2> "$O.err"
echo "rc=$?"
