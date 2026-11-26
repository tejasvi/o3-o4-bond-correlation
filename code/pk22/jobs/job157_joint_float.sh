#!/bin/bash
# job157 (pk22, G7): ast-check and run midrow/g4/mrx/src/joint_float_v1.py for N = 4 and 3 (float control of the c3j JTH entries).
set -u
S=/mnt/g2/release/root/code/pk22
PY=python3
T=$S/midrow/g4/mrx/src/joint_float_v1.py
$PY -I -B $S/tools/astcheck_v1.py $T || exit 4
for n in 4 3; do $PY -I -B $T $n > $S/midrow/g4/mrx/out/joint_float_v1_n$n.out 2>&1; echo "RUN N=$n rc=$?"; cat $S/midrow/g4/mrx/out/joint_float_v1_n$n.out; done
