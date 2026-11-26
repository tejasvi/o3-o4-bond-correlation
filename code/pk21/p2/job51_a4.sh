#!/bin/bash
D=/mnt/g2/release/root/code/pk21/p2/a
PY=python3
O=$D/out/a4_units_crosscheck_v1.out
set -o noclobber
: > $O || exit 3
$PY -I -B -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" $D/a4_units_crosscheck_v1.py >> $O 2>&1 || { echo "SYNTAX FAIL" >> $O; exit 4; }
timeout 300 $PY -I -B $D/a4_units_crosscheck_v1.py >> $O 2>&1 || echo "FAILED a4" >> $O
