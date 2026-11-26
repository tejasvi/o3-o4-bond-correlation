#!/bin/bash
D=/mnt/g2/release/root/code/pk21/p2/a
PY=python3
O=$D/out/a3_bulk_checks_v1.out
$PY -I -B -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" $D/a3_bulk_checks_v1.py >> $O 2>&1 || { echo "SYNTAX FAIL" >> $O; exit 4; }
$PY -I -B $D/a3_bulk_checks_v1.py $D/out >> $O 2>&1 || echo "FAILED a3" >> $O
