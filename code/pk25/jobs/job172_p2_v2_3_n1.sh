#!/bin/bash
# job172 (pk25; P2 rerun for the N1, the row 4691): ast of the v2_3 maker; build p2/kt_p2_v2_3.py with pk24's NU record and
# producer; dry run TAG d4 and its rows against the cited cert record p2/MR_LEMMAP_V3F.kv (0cd95286); if VALID, make p2/v3f2 and run the
# cert TAG c1 to p2/v3f2/MR_LEMMAP_V3F.kv, then its rows against d4's.
set -u
W=/mnt/g2/release/root/code
D=$W/pk25
PY=python3
$PY -I -B -c 'import ast, sys
for f in sys.argv[1:]:
    ast.parse(open(f).read(), f)
print("AST OK %d files" % (len(sys.argv) - 1))' $D/p2/make_kt_p2_v2_3.py || { echo "STOP ast"; exit 6; }
[ ! -e $D/p2/v3f2 ] || { echo "STOP p2/v3f2 exists"; exit 6; }
$PY -I -B $D/p2/make_kt_p2_v2_3.py kt_p2_v2_3.py pk24/nu/NU_G_RECORD_v1.kv pk24/nu/MANIFEST_NU_G_RECORD_v1.sha256 pk24/nu/kt_nu_g_v1_2.py | awk '!/^PINS /' || { echo "STOP maker"; exit 6; }
[ -f $D/p2/kt_p2_v2_3.py ] || { echo "STOP no engine"; exit 6; }
$PY -I -B $D/p2/kt_p2_v2_3.py dry d4
rc=$?
echo "d4 dry rc $rc"
cmp_rows() {
  awk -F' = ' 'FNR == 1 {f++} /^N[34]_P[0-9]+ = / {if (f == 1) {o[$1] = $2; n1++} else {n2++; if (!($1 in o)) miss++; else if (o[$1] != $2) {d++; split(o[$1], a, " "); split($2, b, " "); for (i = 1; i <= length(a); i++) if (a[i] != b[i]) {nf++; if (a[i] + 0 > b[i] + 0) down++}; if (last == "" && $1 ~ /P0903/) last = $1}}} END {printf "ROWS %d vs %d, missing %d, rows differing %d, fields differing %d (of which smaller in the second file %d)\n", n1, n2, miss, d, nf, down}' "$1" "$2"
  awk -F' = ' 'FNR == 1 {f++} $1 ~ /^N[34]_P0903$/ {if (f == 1) o[$1] = $2; else print "LAST " $1 ": " (o[$1] == $2 ? "equal" : "DIFFERENT")}' "$1" "$2"
}
if [ $rc -eq 0 ] && [ -f $D/p2/dry_d4/MR_LEMMAP_V3F.kv ]; then
  cmp_rows $D/p2/MR_LEMMAP_V3F.kv $D/p2/dry_d4/MR_LEMMAP_V3F.kv
  mkdir $D/p2/v3f2 || { echo "STOP mkdir"; exit 6; }
  $PY -I -B $D/p2/kt_p2_v2_3.py cert c1
  echo "cert c1 rc $?"
  [ -f $D/p2/v3f2/MR_LEMMAP_V3F.kv ] && cmp_rows $D/p2/dry_d4/MR_LEMMAP_V3F.kv $D/p2/v3f2/MR_LEMMAP_V3F.kv
fi
exit 0
