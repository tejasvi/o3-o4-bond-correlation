#!/bin/bash
# job229 (pk22, H4TH into the c3h lawcert fork, main row 4485): ast.parse of the maker, the maker (writes m3/m3_lawcert_c3h_v1_1.py,
# mode 'x'), ast.parse of it, the static item (output m3/out/m3_lawcert_c3h_v1_1_static.out), then items 4 and 3 (the certificates
# m3/out/m3_lawcert_c3h_v1_1_N<N>.json, mode 'x', after every gate and plant; outputs m3/out/m3_lawcert_c3h_v1_1_<N>.out). noclobber.
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
PY=python3
export TMPDIR=$S/m3/tmp
M=$S/m3/make_m3_lawcert_c3h_v1_1.py
P=$S/m3/m3_lawcert_c3h_v1_1.py
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('AST OK', sys.argv[1])" $M || exit 4
echo "SRC $(/usr/bin/sha256sum $M | /usr/bin/cut -c1-8) make_m3_lawcert_c3h_v1_1.py"
$PY -I -B $M
echo "MAKER rc=$?"
[ -f $P ] || exit 5
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('AST OK', sys.argv[1])" $P || exit 6
echo "SRC $(/usr/bin/sha256sum $P | /usr/bin/cut -c1-8) m3_lawcert_c3h_v1_1.py"
O=$S/m3/out/m3_lawcert_c3h_v1_1_static.out
$PY -I -B $P static 300 > $O 2> ${O%.out}.err
echo "RUN static rc=$?"
/usr/bin/awk '/-> FAIL|DOES NOT FIRE|^VERDICT|^C-PREP16|^C-HASH/' $O | /usr/bin/cut -c1-300
/usr/bin/tail -n 8 ${O%.out}.err
/usr/bin/awk '/^VERDICT VALID$/ {ok=1} END {exit !ok}' $O || exit 7
for N in 4 3; do
  O=$S/m3/out/m3_lawcert_c3h_v1_1_$N.out
  $PY -I -B $P $N 540 > $O 2> ${O%.out}.err
  echo "RUN N=$N rc=$?"
  /usr/bin/awk '/-> FAIL|DOES NOT FIRE|^VERDICT|^RECORD|^C-PINS|^C-BIND|^C-PRODUCER|^C-NO-RESUME|^C-LAWFIELDS|^C-MONO-FAR|^C-BAND|^C-LAWCERT-RT/' $O | /usr/bin/cut -c1-330
  /usr/bin/tail -n 8 ${O%.out}.err
done
