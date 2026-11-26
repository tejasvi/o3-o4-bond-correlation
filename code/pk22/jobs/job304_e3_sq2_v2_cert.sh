#!/bin/bash
# job304 (pk22; item (3) part (6), after pk23's certified M4XY v1_1): build e3_sq2_v2.py (make_e3_sq2_v2.py --cert M4KV ASMOUT M4MAN V18MAN,
# V18MAN the x records' run manifest pk22/midrow/e3/kt/MANIFEST_V1_8_XY_2_X_v1.sha256), its static check, and its runs at N = 4 and 3
# (records midrow/e3/out/e3_sq2_v2_N<N>.json, mode 'x'). Usage: job304_e3_sq2_v2_cert.sh M4KV ASMOUT M4MAN (paths under code, pk23's).
set -u
set -o noclobber
[ $# -eq 3 ] || { echo "usage: job304_e3_sq2_v2_cert.sh M4KV ASMOUT M4MAN"; exit 2; }
W=/mnt/g2/release/root/code
S=$W/pk22
D=$S/midrow/e3/src
O=$S/midrow/e3/out
PY=python3
export TMPDIR=$S/midrow/e3/tmp
for p in "$1" "$2" "$3"; do [ -f "$W/$p" ] || { echo "STOP: missing $W/$p"; exit 3; }; done
/usr/bin/sha256sum -c --quiet $S/midrow/e3/kt/MANIFEST_V1_8_XY_2_X_v1.sha256 || { echo "STOP: x records manifest"; exit 3; }
echo "TEMPLATE $(/usr/bin/sha256sum $D/e3_sq2_v2.tmpl.py | /usr/bin/cut -c1-8), MAKER $(/usr/bin/sha256sum $D/make_e3_sq2_v2.py | /usr/bin/cut -c1-8)"
[ -e $D/e3_sq2_v2.py ] && { echo "STOP: e3_sq2_v2.py exists"; exit 3; }
$PY -I -B $D/make_e3_sq2_v2.py --cert "$1" "$2" "$3" pk22/midrow/e3/kt/MANIFEST_V1_8_XY_2_X_v1.sha256 || { echo "STOP: maker"; exit 3; }
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('STATIC ast.parse OK', sys.argv[1])" $D/e3_sq2_v2.py || { echo "STOP: static"; exit 3; }
for N in 4 3; do
  o=$O/e3_sq2_v2_n$N.out
  [ -e $o ] && { echo "STOP: $o exists"; exit 3; }
  $PY -I -B $D/e3_sq2_v2.py $N > $o 2> ${o%.out}.err
  echo "RUN N=$N rc=$?"
  /usr/bin/awk '/-> FAIL|DOES NOT FIRE|^(C-MANIFEST|C-LOAD|C-LEMMA|C-JMIN-GRID|C-MONO-J|C-LIMIT|C-ROUND|ROWS|RECORD|VERDICT)/{print substr($0, 1, 420)}' $o
  /usr/bin/tail -n 6 ${o%.out}.err
done
