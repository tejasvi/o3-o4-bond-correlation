#!/bin/bash
# job233 (pk22, MR_EXACT v1_9 with H4TH's certified J-laws, main row 4485): ast.parse of the maker, the maker (writes
# midrow/g4/mrc/src/mrx_cert_v1_9.py and mrx_combine_v1_9.py, mode 'x'), ast.parse of both, the certified runs at N = 4 and 3 (outputs
# midrow/g4/mrc/out/mrx_cert_v1_9_cert_n<N>.out; parts out/cert/MR_EXACT_PART_v1_9_<U|C>_N<N>.kv), then the combine (output
# midrow/g4/mrc/out/mrx_combine_v1_9_a.out; record out/cert/MR_EXACT_CERT_v1_9_C.kv).
set -u
S=/mnt/g2/release/root/code/pk22
E=$S/midrow/g4/mrc
PY=python3
export TMPDIR=$E/tmp
M=$E/src/make_mrx_v1_9.py
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('AST OK', sys.argv[1])" $M || exit 4
echo "SRC $(/usr/bin/sha256sum $M | /usr/bin/cut -c1-8) make_mrx_v1_9.py"
$PY -I -B $M
echo "MAKER rc=$?"
for P in $E/src/mrx_cert_v1_9.py $E/src/mrx_combine_v1_9.py; do
  [ -f $P ] || exit 5
  $PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('AST OK', sys.argv[1])" $P || exit 6
  echo "SRC $(/usr/bin/sha256sum $P | /usr/bin/cut -c1-8) $P"
done
for N in 4 3; do
  O=$E/out/mrx_cert_v1_9_cert_n${N}.out
  if [ -e $O ]; then echo "STOP: $O exists"; exit 3; fi
  env MALLOC_ARENA_MAX=2 $PY -I -B $E/src/mrx_cert_v1_9.py cert $N > $O 2> ${O%.out}.err
  echo "RUN N=$N rc=$?"
  /usr/bin/cut -c1-400 $O | /usr/bin/awk '/-> FAIL|DOES NOT FIRE|^(C-LAWCERT|PLANT-LAWCERT|C-CERT-SAME|CERT-COUNT|C-H0|C-BULK|C-FACTX|C-FLOAT |JLOW C|XSIGN C|RECORD|VERDICT)/'
  /usr/bin/tail -n 12 ${O%.out}.err
done
O=$E/out/mrx_combine_v1_9_a.out
if [ -e $O ]; then echo "STOP: $O exists"; exit 3; fi
$PY -I -B $E/src/mrx_combine_v1_9.py > $O 2> ${O%.out}.err
echo "COMBINE rc=$?"
/usr/bin/cut -c1-300 $O
/usr/bin/tail -n 12 ${O%.out}.err
