#!/bin/bash
# job240_m2cols_v2_test.sh (pk24; pk25's P4 ask): tests tools/check_m2_cols_v2.py before M2's certified run. From the M2 rehearsal set
# (mr_engine/m2_rehearsal_v1), tools/make_vx_refresh_standin_v1.py writes test stand-ins (vxref: P4's floor-free vx hull on the last h rows;
# plant_other: vx changed on a non-last h row; plant_low: vx_hi below the hull). Expected: v2 on the rehearsal set rc 0; v2 on vxref rc 0 with
# vx_lo, vx_hi among the allowed changes; v1 on vxref rc 9 (the reason for v2); v2 on plant_other rc 9; v2 on plant_low rc 0 with the VXHULL
# INFO line 'misses on the high side'.
O=/mnt/g2/release/root/code/pk24
CODEDIR=/mnt/g2/release/root/code
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
set -o noclobber
run() { python3 -I -B $G $O/guard/MIDROW_GUARD_$1.log $2 --run -- env OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B "${@:3}"; }
E=$O/mr_engine; X=$E/out; T=$E/vxref_test_v1
V4B=$CODEDIR/pk25/mr/v4b/MR_INSERT.kv; E19=$CODEDIR/pk22/midrow/g4/mrc/out/cert/MR_EXACT_CERT_v1_9_C.kv; RE=$E/m2_rehearsal_v1
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
run j240_ast 0.03 $O/tools/astcheck_pk24_v1.py $O/tools/check_m2_cols_v2.py $O/tools/make_vx_refresh_standin_v1.py > $X/j240_ast.console 2>&1
rc=$?; echo "ast rc=$rc"; cat $X/j240_ast.console
if [ $rc -ne 0 ]; then exit 4; fi
run j240_mk 0.03 $O/tools/make_vx_refresh_standin_v1.py $RE/MR_INSERT.kv $T > $X/j240_mk.console 2>&1
rc=$?; echo "stand-ins rc=$rc"; cat $X/j240_mk.console
if [ $rc -ne 0 ]; then exit 5; fi
for c in "reh v2 $RE/MR_INSERT.kv 0" "vxref v2 $T/vxref/MR_INSERT.kv 0" "vxref v1 $T/vxref/MR_INSERT.kv 9" "plant_other v2 $T/plant_other/MR_INSERT.kv 9" "plant_low v2 $T/plant_low/MR_INSERT.kv 0"; do
  set -- $c
  run j240_$1_$2 0.03 $O/tools/check_m2_cols_$2.py $V4B $3 $E19 $RE/MR_EXACT.kv > $X/j240_$1_$2.console 2>&1
  rc=$?; if [ "$rc" = "$4" ]; then v=AS-EXPECTED; else v=UNEXPECTED; fi
  echo "CASE $1 check_m2_cols_$2: rc $rc (expected $4) -> $v"
  awk '/^M2COLS (INSERT|EXACT): |VXHULL|CHANGED N[34]_P0903_h vx|^M2COLS OK|^M2COLS STOP/' $X/j240_$1_$2.console | cut -c1-260
done
echo "end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
