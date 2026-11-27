#!/bin/bash
D=/mnt/g2/release/root/code/pk21/p2/s4c
PY=python3
$PY -I -B -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" $D/kt_s9h_tau4_pk21_v1.py > $D/out/job22_stdout.txt 2>&1 || { echo "SYNTAX FAIL" >> $D/out/job22_stdout.txt; exit 4; }
$PY -I -B $D/kt_s9h_tau4_pk21_v1.py vsweep 300 >> $D/out/job22_stdout.txt 2>&1
echo "exit $?" >> $D/out/job22_stdout.txt
