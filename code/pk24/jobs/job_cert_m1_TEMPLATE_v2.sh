#!/bin/bash
# job_cert_m1_TEMPLATE_v2.sh (pk24; the rows 4446, 4505, 4520, 4523, 4526, 4534, 4536): M1's CERTIFIED run, to be copied to a numbered job
# with INS_PATH, INS_SHA8 and TAG set once pk25's option B MR_INSERT (mr/v4b) lands. Steps: stage the five certified records byte for byte
# (tools/stage_certset_v1.py, pins checked); the v4b check against mr/v4 21e88843 (tools/check_v4b_cols_v1.py: FIELDS and row keys; C11's
# h-row columns, row 4526, stop 8; C_hi on h and t rows, row 4534, stop 10; every field but Pev_hi and vp_hi, row 4536, stop 9); the row
# 4520 gate: every t row's Pev_hi at or below 0.48 at both N, else stop; the Pev levels report (h and t per N, least and largest, with the
# piece); engine v1_8_4 CERTIFIED at NMAX 11, and at NMAX 10 only if 11 fails (row 4505); every gate line; the summary (FAIL, the three
# lowest-H rows per N, same-bond H_J, RUN_VERDICT). v1 of this template (jobs/job_cert_m1_TEMPLATE.sh) had the C11 check alone, in awk.
O=/mnt/g2/release/root/code/pk24
CODEDIR=/mnt/g2/release/root/code
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
set -o noclobber
INS_PATH=PENDING
INS_SHA8=PENDING
TAG=PENDING
if [ "$INS_PATH" = PENDING ] || [ "$INS_SHA8" = PENDING ] || [ "$TAG" = PENDING ]; then echo "set INS_PATH, INS_SHA8 and TAG first"; exit 2; fi
run() { python3 -I -B $G $O/guard/MIDROW_GUARD_$1.log $2 --run -- env OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B "${@:3}"; }
E=$O/mr_engine; X=$E/out; R=$E/cert_m1_$TAG; ENG=$E/kt_mr_assembly_v1_8_4.py
V4=$CODEDIR/pk25/mr/v4/MR_INSERT.kv
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
run ${TAG}_stage 0.03 $O/tools/stage_certset_v1.py $R pk25/mr/v4/MR_SPECTRAL.kv:0e4d8177 $INS_PATH:$INS_SHA8 pk22/midrow/g4/mrc/out/cert/MR_EXACT_CERT_v1_9_C.kv:98e4e01e pk25/mr/v4/MR_CRUDEX.kv:eb4d7511 pk22/midrow/g4/mrc/out/cert/MR_JOINT_CERT_v1.kv:80bc8d81 > $E/cert_m1_$TAG.stage.console 2>&1
rc=$?; echo "stage rc=$rc"; cat $E/cert_m1_$TAG.stage.console
if [ $rc -ne 0 ]; then exit 5; fi
run ${TAG}_chk 0.03 $O/tools/check_v4b_cols_v1.py $V4 $R/MR_INSERT.kv > $X/${TAG}_chk.console 2>&1
rc=$?; echo "v4b check rc=$rc"; cat $X/${TAG}_chk.console
if [ $rc -ne 0 ]; then echo "STOP before the engine: v4b check rc $rc (8 C11 reruns first; 10 MR_JOINT reruns first; 9 other fields or structure)"; exit 7; fi
awk '/^FIELDS = / { for (i = 3; i <= NF; i++) c[$i] = i } /^N[34]_P[0-9]+_[ht] / { split($1, q, "_"); N = substr(q[1], 2); X = q[3]; v = $(c["Pev_hi"]) + 0; k = N SUBSEP X; if (!(k in lo) || v < lo[k]) { lo[k] = v; wl[k] = $1 } if (!(k in hi) || v > hi[k]) { hi[k] = v; w[k] = $1 } } END { bad = 0; for (N = 4; N >= 3; N--) { printf "PEV LEVELS N=%d: h Pev_hi [%.6g at %s, %.6g at %s], t Pev_hi [%.6g at %s, %.6g at %s]\n", N, lo[N, "h"], wl[N, "h"], hi[N, "h"], w[N, "h"], lo[N, "t"], wl[N, "t"], hi[N, "t"], w[N, "t"]; if (hi[N, "t"] > 0.48) bad = 1 } printf "PEV GATE (main row 4520: t <= 0.48 on every piece): %s\n", bad ? "EXCEEDED - stop; the subtraction step and a G6 revision are needed" : "PASS"; exit bad }' $R/MR_INSERT.kv
if [ $? -ne 0 ]; then exit 6; fi
PS=$(sha256sum $R/PINS.txt | cut -d' ' -f1)
for NM in 11 10; do
  run ${TAG}_e_$NM 0.12 $ENG $R $PS CERTIFIED $E/MR_ASSEMBLY_cert_m1_${TAG}_n$NM.kv none $NM > $E/kt_mr_v1_8_4_cert_m1_${TAG}_n$NM.out 2>&1
  rc=$?; echo "engine NMAX $NM rc=$rc"
  awk '/^G-|^C-|^XMODE|^ROUTE V|^RUN_VERDICT|^STOP|^MODE/' $E/kt_mr_v1_8_4_cert_m1_${TAG}_n$NM.out | cut -c1-220
  F=$E/MR_ASSEMBLY_cert_m1_${TAG}_n$NM.kv
  [ -e $F ] && awk -v nm=$NM 'BEGIN{f=0; n=0} $1 ~ /^N[34]_n/ { n++; h = $NF + 0; N = substr($1, 2, 1); if ($10 == "FAIL") { f++; fl = fl " " $1 } d = $1 " (" $3 " d " $4 " dp " $6 " m " $7 " piece " $9 ", H " $NF ")"; for (j = 1; j <= 3; j++) if (!((N, j) in bh) || h < bh[N, j]) { for (k = 3; k > j; k--) if ((N, k - 1) in bh) { bh[N, k] = bh[N, k - 1]; bd[N, k] = bd[N, k - 1] } bh[N, j] = h; bd[N, j] = d; break } } END { printf "CERT M1 NMAX %s: rows %d, FAIL %d%s\n", nm, n, f, (f ? "; FAIL rows:" fl : ""); for (N = 4; N >= 3; N--) for (j = 1; j <= 3; j++) if ((N, j) in bh) printf "  N%d lowest H #%d: %s\n", N, j, bd[N, j] }' $F
  awk '/^SUMMARY/ { split($0, a, "same-bond orbits "); print "  " $2 " " $3 " same-bond: " substr(a[2], 1, 40) }' $E/kt_mr_v1_8_4_cert_m1_${TAG}_n$NM.out | awk 'NR <= 12'
  [ -e $F ] && awk '/^RUN_VERDICT|^MODE/' $F | cut -c1-160
  if [ $rc -eq 0 ]; then echo "NMAX_M1 = $NM (row 4505)"; break; fi
done
echo "end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
