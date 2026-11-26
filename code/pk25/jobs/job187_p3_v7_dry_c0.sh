#!/bin/bash
# job187 (pk25; the rows 4768, 4770, 4772): E3 v2's freeze manifest verified; ast of the v7 maker; build asm/kt_s9h_p3_v7_1.py from the
# P3 v7 template (E3's certified R_xy per piece, C-SQ2, MODE cert, CW CERTIFIED only, C-MAIN-E4); dry run TAG c0 PART full on the real
# E3 rows (dry record asm/dry_c0/MR_CRUDEX.kv). The certified run is a separate job, after the P3b-2 review.
set -u
W=/mnt/g2/release/root/code
D=$W/pk25
PY=python3
EM=$W/pk22/midrow/e3/MANIFEST_E3_SQ2_v2.sha256
[ -f $EM ] || { echo "STOP: E3 v2 is not frozen ($EM)"; exit 6; }
/usr/bin/sha256sum -c --quiet $EM || { echo "STOP: E3's freeze manifest does not verify"; exit 6; }
echo "E3 manifest $(/usr/bin/sha256sum $EM | cut -c1-8) verified"
$PY -I -B -c 'import ast, sys; ast.parse(open(sys.argv[1]).read()); print("AST OK maker")' $D/asm/make_kt_s9h_p3_v7.py || { echo "STOP ast"; exit 6; }
$PY -I -B $D/asm/make_kt_s9h_p3_v7.py kt_s9h_p3_v7_1.py | awk '!/^PINS /' || { echo "STOP maker"; exit 6; }
[ -f $D/asm/kt_s9h_p3_v7_1.py ] || { echo "STOP no engine"; exit 6; }
$PY -I -B $D/asm/kt_s9h_p3_v7_1.py dry c0 full
echo "dry c0 full rc $?"
