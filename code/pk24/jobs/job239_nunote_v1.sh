#!/bin/bash
# job239_nunote_v1.sh (pk24; the rows 4635, 4639, 4641): NU_G_NOTE_v1 (the analytic nu_g in engine A's own identification): the input
# pins as cited; AST of the assembler; the assembler (tools/assemble_nunote_v1.py); the note and its manifest.
O=/mnt/g2/release/root/code/pk24
CODEDIR=/mnt/g2/release/root/code
G=/mnt/g2/guard/coreh_guard_v2.py
PY=python3
set -o noclobber
run() { python3 -I -B $G $O/guard/MIDROW_GUARD_$1.log $2 --run -- env OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- $PY -I -B "${@:3}"; }
X=$O/mr_engine/out
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
ok=1
for p in "pk02/kt_cert_v1_9.py 86bcb6c7" "pk02/arbeng_c2b_v2.py fb8cd1b5" "rv02/REVIEW_KTCERT_RE_DEFINITION_rv02.md fba486b2" "rv02/REVIEW_KTCERT_RE_DEFINITION_ADD1_rv02.md 1b04a668" "rv02/REVIEW_P2_V2_1_rv02.md 6abd3d0d" "pk11/out/ts_N4_J170_D_S_z9sym_v1.json ea9d6c1b" "pk11/out/vacres_K3_N4_sym_v1.json b40859de"; do
  set -- $p; s=$(sha256sum $CODEDIR/$1 | cut -c1-8)
  if [ "$s" = "$2" ]; then echo "PIN OK $2 $1"; else echo "PIN DIFFERS $s (cited $2) $1"; ok=0; fi
done
if [ $ok -ne 1 ]; then exit 3; fi
run j239_ast 0.03 $O/tools/astcheck_pk24_v1.py $O/tools/assemble_nunote_v1.py > $X/j239_ast.console 2>&1
rc=$?; echo "ast rc=$rc"; cat $X/j239_ast.console
if [ $rc -ne 0 ]; then exit 4; fi
run j239_note 0.03 $O/tools/assemble_nunote_v1.py > $X/j239_note.console 2>&1
rc=$?; echo "note rc=$rc"; cat $X/j239_note.console
echo "end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
