#!/bin/bash
# run_o5_v1.sh (pk23): O5's whole-graph route, memory probes on the local machine; one guarded job per step in the form (1 core, timeout 580,
# prlimit 8 GiB, sequential). Batches:
#   make     AST check of o5/make_g36_v1.py, the maker (writes o5/kt_lbu_g36_pk23_v1.py once, never over), AST check of the copy;
#   control  the copy at n = 4, N = 4, K = 3, J1 = 350, orbit G02, sigma 1/4, MEMSTOP 7800: must reproduce pk06/runs/full_n4_G02_s14_v1.out;
#   probes   n = 5, 6, 7 at N = 4, K = 3, J1 = 350, orbit far, sigma 1/4, MEMSTOP 7800: the T1 build stops at the engine's own memory
#            predictor (GuardStop) before it would pass 7800 MB; the MOMDEG lines give terms, RSS and the predicted peak per degree.
# Guard caps: 0.03 core-h for ast/make, 0.10 (kill at 300 s CPU) for the control, 0.17 (kill at 552 s) for each probe (engine LIM 520).
# Outputs pk23/out/o5_<step>.out (noclobber). Usage: run_o5_v1.sh make|control|probes
H=/mnt/g2/release/root/code/pk23
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
E=$H/o5/kt_lbu_g36_pk23_v1.py
set -o noclobber
run() { python3 -I -B $G $H/guard/PK23_GUARD_$1.log $2 --run -- env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B "${@:3}"; }
step() { local name=$1 cap=$2; shift 2; echo "step $name start $(date -u +%Y-%m-%dT%H:%M:%SZ)"; run o5_$name $cap "$@" > $H/out/o5_$name.out 2>&1; local rc=$?; echo "step $name rc=$rc end $(date -u +%Y-%m-%dT%H:%M:%SZ) $(awk '/total/{t=$0} END {print t}' $H/guard/PK23_GUARD_o5_$name.log)"; return $rc; }
case "$1" in
  make)
    step ast_maker 0.03 $H/tools/astcheck_v1.py $H/o5/make_g36_v1.py || exit 4
    step make_g36 0.03 $H/o5/make_g36_v1.py || exit 4
    step ast_g36 0.03 $H/tools/astcheck_v1.py $E || exit 4 ;;
  control) step control_n4_G02 0.10 $E grid 280 3 3 4 4 350 G02 1/4 none 7800 ;;
  probes)
    step probe_n5 0.17 $E grid 520 3 3 5 4 350 far 1/4 none 7800
    step probe_n6 0.17 $E grid 520 3 3 6 4 350 far 1/4 none 7800
    step probe_n7 0.17 $E grid 520 3 3 7 4 350 far 1/4 none 7800 ;;
  *) echo "usage: run_o5_v1.sh make|control|probes"; exit 2 ;;
esac
