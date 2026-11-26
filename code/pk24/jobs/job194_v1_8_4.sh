#!/bin/bash
# job194_v1_8_4.sh (pk24; the rows 4320, 4325, 4335, 4340, 4359, 4376; the tail-check request): AST, makers and AST for engine v1_8_4 (v1_8_3 with the C-TAILMONO OK and TAIL SUP lines); template diffs v1_8_3 -> v1_8_4 and v1_7_1 -> v1_8_4; on job192's upgraded sets (folder v36): regressions against v1_7_1's rows, the tail rows of v1_8_1 (now with the two new lines), the 28 plants, the negatives, route (v) against the diagnostic engine and on the v4 stand-ins, and the Way B floor test through the tail. Folder v38.
O=/mnt/g2/release/root/code/pk24
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
set -o noclobber
run() { python3 -I -B $G $O/guard/MIDROW_GUARD_$1.log $2 --run -- env OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B "${@:3}"; }
E=$O/mr_engine; X=$E/out; V=$E/v38; U=$E/v36; S17=$E/v17; V20=$E/v20; V22=$E/v22; V27=$E/v27; V30=$E/v30; V35=$E/v35
rowcmp() { awk -v t="$1" 'NR==FNR { if ($1 ~ /^N[34]_n/) a[$1] = $0; next } $1 ~ /^N[34]_n/ { n++; if (!($1 in a) || a[$1] != $0) x++ } END { printf "REGRESSION %s: rows %d, rows differing %d\n", t, n, x }' "$2" "$3"; }
tailcmp() { awk -v t="$1" 'NR==FNR { if ($1 ~ /^N[34]_P/) a[$1] = $0; next } $1 ~ /^N[34]_P/ { n++; if (!($1 in a) || a[$1] != $0) x++ } END { printf "TAIL REGRESSION %s: rows %d, rows differing %d\n", t, n, x }' "$2" "$3"; }
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
run j194_ast1 0.03 $O/tools/astcheck_pk24_v1.py $O/tools/make_mrtemplates_v1_8_4.py $O/tools/make_mrengine_v1_8_4.py > $X/j194_ast1.console 2>&1
rc=$?; echo "ast1 rc=$rc"; cat $X/j194_ast1.console
if [ $rc -ne 0 ]; then exit 4; fi
run j194_tmpl 0.03 $O/tools/make_mrtemplates_v1_8_4.py > $X/j194_tmpl.console 2>&1
rc=$?; echo "templates rc=$rc"; cat $X/j194_tmpl.console
if [ $rc -ne 0 ]; then exit 5; fi
run j194_make 0.03 $O/tools/make_mrengine_v1_8_4.py > $X/j194_make.console 2>&1
rc=$?; echo "engine make rc=$rc"; cat $X/j194_make.console
if [ $rc -ne 0 ]; then exit 6; fi
run j194_ast2 0.03 $O/tools/astcheck_pk24_v1.py $E/src/kt_mr_assembly_v1_8_4.py.in $E/src/mr_merge_v1_8_4.py.in $E/kt_mr_assembly_v1_8_4.py $E/mr_merge_v1_8_4.py > $X/j194_ast2.console 2>&1
rc=$?; echo "ast2 rc=$rc"; cat $X/j194_ast2.console
if [ $rc -ne 0 ]; then exit 7; fi
run j194_d1 0.03 $O/tools/udiff_v1.py $E/src/kt_mr_assembly_v1_8_3.py.in $E/src/kt_mr_assembly_v1_8_4.py.in $X/udiff_engine_tmpl_v1_8_3_v1_8_4.txt > $X/j194_udiff.console 2>&1
run j194_d2 0.03 $O/tools/udiff_v1.py $E/src/mr_merge_v1_8_3.py.in $E/src/mr_merge_v1_8_4.py.in $X/udiff_merge_tmpl_v1_8_3_v1_8_4.txt >> $X/j194_udiff.console 2>&1
run j194_d3 0.03 $O/tools/udiff_v1.py $E/src/kt_mr_assembly_v1_7_1.py.in $E/src/kt_mr_assembly_v1_8_4.py.in $X/udiff_engine_tmpl_v1_7_1_v1_8_4.txt >> $X/j194_udiff.console 2>&1
run j194_d4 0.03 $O/tools/udiff_v1.py $E/src/mr_merge_v1_7_1.py.in $E/src/mr_merge_v1_8_4.py.in $X/udiff_merge_tmpl_v1_7_1_v1_8_4.txt >> $X/j194_udiff.console 2>&1
echo "udiff rc=$?"; awk '/^UDIFF OUT/' $X/j194_udiff.console
ENG=$E/kt_mr_assembly_v1_8_4.py
mkdir $V
for B in "v3f:default" "v3s:default" "v4s:default" "v4f:20" "a0:default"; do
  T=${B%%:*}; NM=${B#*:}; D=$U/up_$T; PB=$(sha256sum $D/PINS.txt | cut -d' ' -f1)
  run j194_r_$T 0.06 $ENG $D $PB STANDIN $V/MR_ASSEMBLY_$T.kv none $NM > $V/kt_mr_v1_8_4_$T.out 2>&1
  echo "regression run $T rc=$?"; awk '/^RUN_VERDICT|^STOP/' $V/kt_mr_v1_8_4_$T.out | cut -c1-220
  rowcmp "v1_8_4 $T against v1_7_1" $V22/MR_ASSEMBLY_$T.kv $V/MR_ASSEMBLY_$T.kv
done
D=$U/up_cwa0e; PB=$(sha256sum $D/PINS.txt | cut -d' ' -f1)
for DM in 3:3:10:$V27/MR_ASSEMBLY_base_D3_M3.kv 2:5:10:$V30/MR_ASSEMBLY_base_D2_M5.kv; do
  D0=$(echo $DM | cut -d: -f1); M0=$(echo $DM | cut -d: -f2); NX=$(echo $DM | cut -d: -f3); REF=$(echo $DM | cut -d: -f4)
  run j194_t_${D0}_${M0} 0.06 $ENG $D $PB STANDIN $V/MR_ASSEMBLY_tail_D${D0}_M${M0}.kv none $NX all $D0:$M0 > $V/kt_mr_v1_8_4_tail_D${D0}_M${M0}.out 2>&1
  echo "tail run $D0:$M0 rc=$?"; awk '/^C-TAILMONO|^TAIL SUP|^TAIL N=|^TAIL_VERDICT|^RUN_VERDICT|^STOP/' $V/kt_mr_v1_8_4_tail_D${D0}_M${M0}.out | cut -c1-420
  rowcmp "v1_8_4 tail run $D0:$M0 rows against v1_8_1" $REF $V/MR_ASSEMBLY_tail_D${D0}_M${M0}.kv
  tailcmp "v1_8_4 $D0:$M0 against v1_8_1" $REF.tail $V/MR_ASSEMBLY_tail_D${D0}_M${M0}.kv.tail
done
D=$U/up_v4f; PS=$(sha256sum $D/PINS.txt | cut -d' ' -f1)
for P in OPN TAU2 SIGN T2 DELTA PIN COUNT UNIF DUPKEY PROD PRODOK XSIGN ENVR FACTX CSTAT ORIENT XORIENT YORIENT IORIENT OCHK XDEF FLOOR; do
  run j194_p_$P 0.05 $ENG $D $PS STANDIN $V/MR_ASSEMBLY_${P}.kv $P > $V/kt_mr_v1_8_4_plant_$P.out 2>&1
  echo "plant $P rc=$?"; awk '/^PLANT/' $V/kt_mr_v1_8_4_plant_$P.out | cut -c1-200
done
for P in TAILQ TAILSIGN TAILENV; do
  run j194_p_$P 0.05 $ENG $D $PS STANDIN $V/MR_ASSEMBLY_${P}.kv $P 10 all 3:3 > $V/kt_mr_v1_8_4_plant_$P.out 2>&1
  echo "plant $P rc=$?"; awk '/^PLANT/' $V/kt_mr_v1_8_4_plant_$P.out | cut -c1-200
done
PO=$(sha256sum $V20/standin_NOF1_L3_CRX30_V4/PINS.txt | cut -d' ' -f1)
run j194_n1 0.03 $ENG $V20/standin_NOF1_L3_CRX30_V4 $PO STANDIN $V/MR_ASSEMBLY_NEG1.kv > $V/kt_mr_v1_8_4_neg1.out 2>&1
echo "negative 1 (a v4 set in v1_8_1's layout) rc=$? (8 expected)"; awk '/^STOP/' $V/kt_mr_v1_8_4_neg1.out | cut -c1-200
PO=$(sha256sum $S17/standin_NOF1_L3_SPLIT/PINS.txt | cut -d' ' -f1)
run j194_n2 0.03 $ENG $S17/standin_NOF1_L3_SPLIT $PO STANDIN $V/MR_ASSEMBLY_NEG2.kv > $V/kt_mr_v1_8_4_neg2.out 2>&1
echo "negative 2 (a v3 set without ORIENT_CHECK) rc=$? (8 expected)"; awk '/^STOP/' $V/kt_mr_v1_8_4_neg2.out | cut -c1-200
D=$U/up_v3s; PB=$(sha256sum $D/PINS.txt | cut -d' ' -f1)
run j194_n3 0.03 $ENG $D $PB STANDIN $V/MR_ASSEMBLY_NEG3.kv none 10 all 3:3 > $V/kt_mr_v1_8_4_neg3.out 2>&1
echo "negative 3 (TAIL on a split set) rc=$? (8 expected)"; awk '/^STOP/' $V/kt_mr_v1_8_4_neg3.out | cut -c1-200
D=$U/up_v4f; PB=$(sha256sum $D/PINS.txt | cut -d' ' -f1)
run j194_n4 0.03 $ENG $D $PB STANDIN $V/MR_ASSEMBLY_NEG4.kv none 8 all 3:3 > $V/kt_mr_v1_8_4_neg4.out 2>&1
echo "negative 4 (NMAX 8 below n0 10) rc=$? (8 expected)"; awk '/^STOP/' $V/kt_mr_v1_8_4_neg4.out | cut -c1-200
D=$U/up_routev; PB=$(sha256sum $D/PINS.txt | cut -d' ' -f1)
run j194_rv 0.12 $ENG $D $PB STANDIN $V/MR_ASSEMBLY_routev.kv > $V/kt_mr_v1_8_4_routev.out 2>&1
echo "route (v) run rc=$?"; awk '/^ROUTE V|^RUN_VERDICT|^STOP/' $V/kt_mr_v1_8_4_routev.out | cut -c1-140
rowcmp "v1_8_4 route (v) against the diagnostic engine" $V35/MR_ASSEMBLY_REAL_V3REC_E7_SIGNMBALL_SIGNM1_PEX4_PEV1.kv $V/MR_ASSEMBLY_routev.kv
D=$U/up_v4f_pex4; PB=$(sha256sum $D/PINS.txt | cut -d' ' -f1)
run j194_v4p 0.06 $ENG $D $PB STANDIN $V/MR_ASSEMBLY_v4f_pex4.kv none 20 > $V/kt_mr_v1_8_4_v4f_pex4.out 2>&1
echo "v4f with Pe_hi rc=$?"; awk '/^RUN_VERDICT|^STOP/' $V/kt_mr_v1_8_4_v4f_pex4.out | cut -c1-140
awk 'NR==FNR { if ($1 ~ /^N[34]_n/) { h[$1] = $NF; m[$1] = $7 } ; next } $1 ~ /^N[34]_n/ { n++; if (h[$1] != $NF) { c++; if (m[$1] == 1) c1++ } ; if ($NF + 0 < h[$1] - 1e-9) w++ } END { printf "ROUTE V ON THE V4 STAND-INS: rows %d, H changed on %d (m = 1: %d), H lower on %d\n", n, c, c1, w }' $V/MR_ASSEMBLY_v4f.kv $V/MR_ASSEMBLY_v4f_pex4.kv
FD=$U/floor_v4f; PF=$(sha256sum $FD/PINS.txt | cut -d' ' -f1)
run j194_fl 0.06 $ENG $FD $PF STANDIN $V/MR_ASSEMBLY_floor.kv none 10 all 2:5 > $V/kt_mr_v1_8_4_floor.out 2>&1
echo "floor run rc=$? (tail FAIL on the floor pieces expected, rc 9)"; awk '/^G-FACTX|^FACTORED SIGN|^TAIL N=|^TAIL_VERDICT|^RUN_VERDICT|^STOP/' $V/kt_mr_v1_8_4_floor.out | cut -c1-330
awk '$1 ~ /^N[34]_P0005$/ {print "FLOOR TAIL ROW", $1, "sign", $14, "envfail", $6, "verdict", $NF}' $V/MR_ASSEMBLY_floor.kv.tail
rowcmp "floor set rows against the zero-floor rows of up_v4f (n <= 10)" $V/MR_ASSEMBLY_v4f.kv $V/MR_ASSEMBLY_floor.kv
echo "end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
