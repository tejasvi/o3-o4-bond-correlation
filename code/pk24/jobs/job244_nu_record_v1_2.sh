#!/bin/bash
# job244_nu_record_v1_2.sh (pk24; the row 4659 approval for row 4639 step (3)): builds pk24/nu/kt_nu_g_v1_2.py (tools/make_kt_nu_g_v1_2.py:
# C-TRI per the N-1, states psi, e1, e2, e3, pk25's record form), AST, a dry run (nu/dry/), and, only if the dry run is VALID, the
# record run writing pk24/nu/NU_G_RECORD_v1.kv; then the manifest pk24/nu/MANIFEST_NU_G_RECORD_v1.sha256 and its check.
O=/mnt/g2/release/root/code/pk24
CODEDIR=/mnt/g2/release/root/code
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
set -o noclobber
run() { python3 -I -B $G $O/guard/MIDROW_GUARD_$1.log $2 --run -- env OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B "${@:3}"; }
X=$O/mr_engine/out; NU=$O/nu
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
cmp $CODEDIR/pk02/arbeng_c2b_v2.py $NU/arbeng_c2b_v2.py && echo "ARBENG COPY IDENTICAL $(sha256sum $NU/arbeng_c2b_v2.py | cut -c1-8)" || { echo "ARBENG COPY DIFFERS"; exit 3; }
run j244_ast 0.03 $O/tools/astcheck_pk24_v1.py $O/tools/make_kt_nu_g_v1_2.py $NU/src/nu_head_v1_2.py $NU/src/nu_main_v1_2.py > $X/j244_ast.console 2>&1
rc=$?; echo "ast rc=$rc"; cat $X/j244_ast.console
if [ $rc -ne 0 ]; then exit 4; fi
run j244_mk 0.03 $O/tools/make_kt_nu_g_v1_2.py > $X/j244_mk.console 2>&1
rc=$?; echo "make rc=$rc"; cat $X/j244_mk.console
if [ $rc -ne 0 ]; then exit 5; fi
run j244_ast2 0.03 $O/tools/astcheck_pk24_v1.py $NU/kt_nu_g_v1_2.py > $X/j244_ast2.console 2>&1
rc=$?; echo "ast tool rc=$rc"; cat $X/j244_ast2.console
if [ $rc -ne 0 ]; then exit 6; fi
run j244_dry 0.05 $NU/kt_nu_g_v1_2.py dry $NU/dry/NU_G_RECORD_v1_dry3.kv > $NU/dry/kt_nu_g_v1_2_dry3.out 2>&1
rc=$?; echo "tool dry rc=$rc"; awk '/^C-HASH|^C-CORE|^C-TRI|^GATES|^RECORD|^RUN_VERDICT/' $NU/dry/kt_nu_g_v1_2_dry3.out | cut -c1-240
if [ $rc -ne 0 ]; then echo "STOP: the dry run is not VALID"; exit 7; fi
run j244_rec 0.05 $NU/kt_nu_g_v1_2.py record $NU/NU_G_RECORD_v1.kv > $NU/kt_nu_g_v1_2_record.out 2>&1
rc=$?; echo "tool record rc=$rc"; cut -c1-260 $NU/kt_nu_g_v1_2_record.out
if [ $rc -ne 0 ]; then exit 8; fi
cmp <(awk '!/^#|^CODE|^STATUS/' $NU/dry/NU_G_RECORD_v1_dry3.kv) <(awk '!/^#|^CODE|^STATUS/' $NU/NU_G_RECORD_v1.kv) && echo "DRY AND RECORD AGREE outside line 1, CODE and STATUS" || echo "DRY AND RECORD DIFFER"
env -C $CODEDIR sha256sum pk24/nu/kt_nu_g_v1_2.py pk24/tools/make_kt_nu_g_v1_2.py pk24/nu/src/nu_head_v1_2.py pk24/nu/src/nu_main_v1_2.py pk24/nu/arbeng_c2b_v2.py pk02/arbeng_c2b_v2.py pk02/kt_cert_v1_9.py pk11/out/ts_N4_J170_D_S_z9sym_v1.json pk11/out/ts_N3_S_z9sym_v1.json pk11/out/vacres_K3_N4_sym_v1.json pk11/out/vacres_K3_N3_sym_v1.json pk25/mr/v3/MR_LEMMAP.kv pk24/NU_G_NOTE_v1.md pk24/MANIFEST_NU_G_NOTE_v1.sha256 rv02/REVIEW_NU_G_NOTE_V1_rv02.md pk24/jobs/job244_nu_record_v1_2.sh pk24/nu/dry/NU_G_RECORD_v1_dry3.kv pk24/nu/dry/kt_nu_g_v1_2_dry3.out pk24/nu/kt_nu_g_v1_2_record.out pk24/nu/NU_G_RECORD_v1.kv > $NU/MANIFEST_NU_G_RECORD_v1.sha256
echo "manifest rc=$?"; env -C $CODEDIR sha256sum -c $NU/MANIFEST_NU_G_RECORD_v1.sha256 | awk '{c[$NF]++} END {for (k in c) print "MANIFEST CHECK", k, c[k]}'
sha256sum $NU/MANIFEST_NU_G_RECORD_v1.sha256 $NU/NU_G_RECORD_v1.kv $NU/kt_nu_g_v1_2.py | awk '{print substr($1,1,8), $2}'
echo "end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
