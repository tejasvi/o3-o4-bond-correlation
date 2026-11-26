#!/bin/bash
# job262 (pk22; the rows 4578, 4582: the laws of the E4 rerun on 10'): ast.parse of the maker, the maker with SIDE8 = the run manifest's
# sha8 read here by tool (writes m3/m3_lawcert_c3k_v2.py, mode 'x'), its diff from v1 (noclobber), ast.parse of it, the static item (output
# m3/out/m3_lawcert_c3k_v2_static.out), then items 4 and 3 (certificates m3/out/m3_lawcert_c3k_v2_N<N>.json, mode 'x', after every gate and
# plant; outputs m3/out/m3_lawcert_c3k_v2_<N>.out). noclobber.
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
PY=python3
export TMPDIR=$S/m3/tmp
M=$S/m3/make_m3_lawcert_c3k_v2.py
P=$S/m3/m3_lawcert_c3k_v2.py
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('AST OK', sys.argv[1])" $M || exit 4
echo "SRC $(/usr/bin/sha256sum $M | /usr/bin/cut -c1-8) make_m3_lawcert_c3k_v2.py"
SIDE8=$(/usr/bin/sha256sum $S/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 | /usr/bin/cut -c1-8)
echo "SIDE8 $SIDE8 (MANIFEST_E4_C3K2_v1.sha256, read by tool)"
env SIDE8=$SIDE8 $PY -I -B $M
echo "MAKER rc=$?"
[ -f $P ] || exit 5
/usr/bin/diff -u $S/m3/m3_lawcert_c3k_v1.py $P > $S/m3/diff_m3_lawcert_c3k_v1_to_v2.txt
echo "DIFF rc=$? lines $(/usr/bin/awk 'END{print NR}' $S/m3/diff_m3_lawcert_c3k_v1_to_v2.txt)"
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('AST OK', sys.argv[1])" $P || exit 6
echo "SRC $(/usr/bin/sha256sum $P | /usr/bin/cut -c1-8) m3_lawcert_c3k_v2.py"
O=$S/m3/out/m3_lawcert_c3k_v2_static.out
$PY -I -B $P static 300 > $O 2> ${O%.out}.err
echo "RUN static rc=$?"
/usr/bin/awk '/-> FAIL|DOES NOT FIRE|^VERDICT|^C-HASH|^C-PREP16|^C-LAW-SHAPE|^C-LAW-REM|^C-PREP-BAR/' $O | /usr/bin/cut -c1-400
/usr/bin/tail -n 12 ${O%.out}.err
/usr/bin/awk '/^VERDICT VALID$/ {ok=1} END {exit !ok}' $O || exit 7
for N in 4 3; do
  O=$S/m3/out/m3_lawcert_c3k_v2_$N.out
  $PY -I -B $P $N 540 > $O 2> ${O%.out}.err
  echo "RUN N=$N rc=$?"
  /usr/bin/awk '/-> FAIL|DOES NOT FIRE|^VERDICT|^RECORD|^C-PINS|^C-BIND|^C-PRODUCER|^C-NO-RESUME|^PLANT-NO-RESUME|^C-LAWFIELDS|^C-MONO-FAR|^C-BAND|^C-LAWCERT-RT/' $O | /usr/bin/cut -c1-520
  /usr/bin/tail -n 12 ${O%.out}.err
done
