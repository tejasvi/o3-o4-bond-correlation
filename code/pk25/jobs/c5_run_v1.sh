#!/bin/bash
# c5_run_v1.sh (pk25): C5's cert run (only after the approval naming m4h_asm_v1.py 65e872b0): m4h_asm_v1 cert (writes pk25/m4h/M4H_KV_v1.txt
# when every check passes), then, if it ends VALID, m4h_reader_v1's script mode on the record; outputs in pk25/m4h/out (new files only).
W=/mnt/g2/release/root/code
PY=python3
D=$W/pk25/m4h
cd $W || exit 2
set -o noclobber
case "$(sha256sum $D/m4h_asm_v1.py | cut -c1-8)" in 65e872b0) ;; *) echo "STOP the asm is not the file named for the approval"; exit 7;; esac
for o in $D/out/out_m4h_asm_v1.out $D/out/out_m4h_asm_v1.err $D/out/out_m4h_reader_v1.out $D/out/out_m4h_reader_v1.err; do [ ! -e "$o" ] || { echo "STOP exists $o"; exit 6; }; done
OMP_NUM_THREADS=1 TMPDIR=$W/pk25/tmp timeout 580 $PY -I -B $D/m4h_asm_v1.py cert > $D/out/out_m4h_asm_v1.out 2> $D/out/out_m4h_asm_v1.err
echo "asm exit $?"
awk '{print substr($0, 1, 300)}' $D/out/out_m4h_asm_v1.out | tail -n 60
echo "--- asm err tail"; tail -n 8 $D/out/out_m4h_asm_v1.err
if [ "$(awk '/^VERDICT/' $D/out/out_m4h_asm_v1.out)" = "VERDICT VALID" ]; then
  OMP_NUM_THREADS=1 TMPDIR=$W/pk25/tmp timeout 300 $PY -I -B $D/m4h_reader_v1.py $D/M4H_KV_v1.txt $D/out/out_m4h_asm_v1.out > $D/out/out_m4h_reader_v1.out 2> $D/out/out_m4h_reader_v1.err
  echo "reader exit $?"
  awk '{print substr($0, 1, 300)}' $D/out/out_m4h_reader_v1.out
  echo "--- reader err tail"; tail -n 8 $D/out/out_m4h_reader_v1.err
fi
