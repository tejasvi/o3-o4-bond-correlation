#!/bin/bash
# job189 (pk25; P3's certified run under the row 4768 pre-authorisation: (i) pk22's E3 v2 frozen (MANIFEST_E3_SQ2_v2) and read by the
# engine): E3's freeze manifest verified; the same engine as the dry c0
# (asm/kt_s9h_p3_v7_1.py, no rebuild); MODE cert TAG c1 PART full (record pk25/mr/v6/MR_CRUDEX.kv); its rows against the dry c0 record.
set -u
W=/mnt/g2/release/root/code
D=$W/pk25
PY=python3
EM=$W/pk22/midrow/e3/MANIFEST_E3_SQ2_v2.sha256
[ -f $EM ] || { echo "STOP: E3 v2 is not frozen"; exit 6; }
/usr/bin/sha256sum -c --quiet $EM || { echo "STOP: E3's freeze manifest does not verify"; exit 6; }
[ -f $D/asm/kt_s9h_p3_v7_1.py ] || { echo "STOP: no engine"; exit 6; }
[ ! -e $D/mr/v6 ] || { echo "STOP: mr/v6 exists"; exit 6; }
[ "$(awk '/^VERDICT/' $D/asm/out/out_kt_s9h_p3_v7_1_dry_c0_full.out)" = "VERDICT VALID (PART full; dry record)" ] || { echo "STOP: the dry c0 is not VALID"; exit 6; }
echo "ENGINE $(/usr/bin/sha256sum $D/asm/kt_s9h_p3_v7_1.py | cut -c1-8), E3 manifest $(/usr/bin/sha256sum $EM | cut -c1-8)"
$PY -I -B $D/asm/kt_s9h_p3_v7_1.py cert c1 full
echo "cert c1 full rc $?"
awk '/^VERDICT|^CERTIFIED RECORD|^C-E3-READ|^C-SQ2|^C-MAIN-E4|^C-JS N|^PLANTS/{print substr($0, 1, 300)}' $D/asm/out/out_kt_s9h_p3_v7_1_cert_c1_full.out
if [ -f $D/mr/v6/MR_CRUDEX.kv ]; then
  echo "ROWS cert $(awk '/^N[34]_P/' $D/mr/v6/MR_CRUDEX.kv | sha256sum | cut -c1-8) dry c0 $(awk '/^N[34]_P/' $D/asm/dry_c0/MR_CRUDEX.kv | sha256sum | cut -c1-8)"
  diff <(awk '!/^N[34]_P/' $D/asm/dry_c0/MR_CRUDEX.kv) <(awk '!/^N[34]_P/' $D/mr/v6/MR_CRUDEX.kv) | cut -c1-200
fi
exit 0
