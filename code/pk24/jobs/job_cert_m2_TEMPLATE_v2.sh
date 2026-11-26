#!/bin/bash
# job_cert_m2_TEMPLATE_v2.sh (pk24; template v1 (d54714dd) with check_m2_cols_v2 for P4 v5 (vx_lo, vx_hi refreshed on the last h row); MIDROW_M2_PLAN_v1_3 sect. 1, G6 v1_7 sect. 5b and 6): M2's CERTIFIED factored run, to be copied to a numbered
# job with INS_PATH/INS_SHA8 (MR_INSERT v5, pk25's P4), EXA_PATH/EXA_SHA8 (MR_EXACT v1_10, pk22's item (4)), CRX_PATH/CRX_SHA8 (the factored
# MR_CRUDEX, pk25's P3) and TAG set, after G-M2F's final pass. Steps: stage the five certified records byte for byte (tools/stage_certset_v1.py;
# MR_SPECTRAL mr/v4 0e4d8177 and MR_JOINT 80bc8d81 as in M1); tools/check_m2_cols_v2.py (v5 is mr/v4b 54691bc1 and v1_10 is v1_9 98e4e01e outside
# the last piece's Way A fields, which carry floor 0 and a certified sign); the factored MR_CRUDEX's header (CRUDEX_FORM factored, D_MAX); the t
# gate on v5 (row 4520); engine v1_8_4 CERTIFIED, factored, NMAX 10, all pieces, TAIL 2:5; every gate line and the summary (FAIL, least H, the
# three lowest-H rows per N, TAIL_VERDICT with its parts, C-SIGN, TAIL SUP, RUN_VERDICT).
O=/mnt/g2/release/root/code/pk24
CODEDIR=/mnt/g2/release/root/code
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
set -o noclobber
INS_PATH=PENDING
INS_SHA8=PENDING
EXA_PATH=PENDING
EXA_SHA8=PENDING
CRX_PATH=PENDING
CRX_SHA8=PENDING
TAG=PENDING
for v in "$INS_PATH" "$INS_SHA8" "$EXA_PATH" "$EXA_SHA8" "$CRX_PATH" "$CRX_SHA8" "$TAG"; do if [ "$v" = PENDING ]; then echo "set the record paths, sha8s and TAG first"; exit 2; fi; done
run() { python3 -I -B $G $O/guard/MIDROW_GUARD_$1.log $2 --run -- env OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B "${@:3}"; }
E=$O/mr_engine; X=$E/out; R=$E/cert_m2_$TAG; ENG=$E/kt_mr_assembly_v1_8_4.py
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
run ${TAG}_stage 0.03 $O/tools/stage_certset_v1.py $R pk25/mr/v4/MR_SPECTRAL.kv:0e4d8177 $INS_PATH:$INS_SHA8 $EXA_PATH:$EXA_SHA8 $CRX_PATH:$CRX_SHA8 pk22/midrow/g4/mrc/out/cert/MR_JOINT_CERT_v1.kv:80bc8d81 > $E/cert_m2_$TAG.stage.console 2>&1
rc=$?; echo "stage rc=$rc"; cat $E/cert_m2_$TAG.stage.console
if [ $rc -ne 0 ]; then exit 5; fi
run ${TAG}_chk 0.03 $O/tools/check_m2_cols_v2.py $CODEDIR/pk25/mr/v4b/MR_INSERT.kv $R/MR_INSERT.kv $CODEDIR/pk22/midrow/g4/mrc/out/cert/MR_EXACT_CERT_v1_9_C.kv $R/MR_EXACT.kv > $X/${TAG}_chk.console 2>&1
rc=$?; echo "m2 cols rc=$rc"; cat $X/${TAG}_chk.console
if [ $rc -ne 0 ]; then echo "STOP before the engine: m2 cols rc $rc"; exit 7; fi
awk '/^CRUDEX_FORM = factored$/ { f = 1 } /^D_MAX = [1-9][0-9]*$/ { d = $3 } /^FIELDS = / { exit } END { if (f && d) { print "FACTORED MR_CRUDEX: CRUDEX_FORM factored, D_MAX " d } else { print "STOP: MR_CRUDEX is not a factored record with D_MAX"; exit 8 } }' $R/MR_CRUDEX.kv
if [ $? -ne 0 ]; then exit 8; fi
awk '/^FIELDS = / { for (i = 3; i <= NF; i++) c[$i] = i } /^N[34]_P[0-9]+_[ht] / { split($1, q, "_"); N = substr(q[1], 2); X = q[3]; v = $(c["Pev_hi"]) + 0; k = N SUBSEP X; if (!(k in hi) || v > hi[k]) { hi[k] = v; w[k] = $1 } } END { bad = 0; for (N = 4; N >= 3; N--) { printf "PEV MAX N=%d: h %.6g at %s, t %.6g at %s\n", N, hi[N, "h"], w[N, "h"], hi[N, "t"], w[N, "t"]; if (hi[N, "t"] > 0.48) bad = 1 } printf "PEV GATE (row 4520: t <= 0.48): %s\n", bad ? "EXCEEDED - stop" : "PASS"; exit bad }' $R/MR_INSERT.kv
if [ $? -ne 0 ]; then exit 6; fi
PS=$(sha256sum $R/PINS.txt | cut -d' ' -f1)
run ${TAG}_e 0.12 $ENG $R $PS CERTIFIED $E/MR_ASSEMBLY_cert_m2_${TAG}_2_5.kv none 10 all 2:5 > $E/kt_mr_v1_8_4_cert_m2_${TAG}_2_5.out 2>&1
rc=$?; echo "engine rc=$rc"
OUTF=$E/kt_mr_v1_8_4_cert_m2_${TAG}_2_5.out
awk '/^G-|^C-|^XMODE|^ROUTE V|^TAIL ARGUMENT|^TAIL N=|^TAIL REASONS|^TAIL_VERDICT|^RUN_VERDICT|^STOP|^MODE|^FACTORED SIGN/' $OUTF | cut -c1-240
F=$E/MR_ASSEMBLY_cert_m2_${TAG}_2_5.kv
[ -e $F ] && awk 'BEGIN{f=0; n=0} $1 ~ /^N[34]_n/ { n++; h = $NF + 0; N = substr($1, 2, 1); if ($10 == "FAIL") { f++; fl = fl " " $1 } d = $1 " (" $3 " d " $4 " dp " $6 " m " $7 " piece " $9 ", H " $NF ")"; for (j = 1; j <= 3; j++) if (!((N, j) in bh) || h < bh[N, j]) { for (k = 3; k > j; k--) if ((N, k - 1) in bh) { bh[N, k] = bh[N, k - 1]; bd[N, k] = bd[N, k - 1] } bh[N, j] = h; bd[N, j] = d; break } } END { printf "CERT M2 finite rows: %d, FAIL %d%s\n", n, f, (f ? "; FAIL rows:" fl : ""); for (N = 4; N >= 3; N--) for (j = 1; j <= 3; j++) if ((N, j) in bh) printf "  N%d lowest H #%d: %s\n", N, j, bd[N, j] }' $F
awk '/^TAIL SUP/' $OUTF | cut -c1-200
[ -e $F ] && awk '/^RUN_VERDICT|^MODE|^TAIL_VERDICT/' $F | cut -c1-160
echo "end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
