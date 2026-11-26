#!/bin/bash
# job236 (pk22, MR_JOINT, main rows 4489-4494): ast.parse of the template and the maker, the maker (writes
# midrow/g4/mrc/src/mrj_cert_v1.py, mode 'x'), ast.parse of it, then the certified run (output midrow/g4/mrc/out/mrj_cert_v1_cert.out;
# record out/cert/MR_JOINT_CERT_v1.kv).
set -u
S=/mnt/g2/release/root/code/pk22
E=$S/midrow/g4/mrc
PY=python3
export TMPDIR=$E/tmp
for P in $E/src/mrj_cert_v1.tmpl.py $E/src/make_mrj_v1.py; do
  $PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('AST OK', sys.argv[1])" $P || exit 4
  echo "SRC $(/usr/bin/sha256sum $P | /usr/bin/cut -c1-8) $P"
done
$PY -I -B $E/src/make_mrj_v1.py
echo "MAKER rc=$?"
P=$E/src/mrj_cert_v1.py
[ -f $P ] || exit 5
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('AST OK', sys.argv[1])" $P || exit 6
echo "SRC $(/usr/bin/sha256sum $P | /usr/bin/cut -c1-8) $P"
O=$E/out/mrj_cert_v1_cert.out
if [ -e $O ]; then echo "STOP: $O exists"; exit 3; fi
env MALLOC_ARENA_MAX=2 $PY -I -B $P cert > $O 2> ${O%.out}.err
echo "RUN rc=$?"
/usr/bin/cut -c1-600 $O
/usr/bin/tail -n 15 ${O%.out}.err
