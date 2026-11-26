#!/bin/bash
# job190 (pk25): freeze P3's certified record (job189): mr/v6/MR_CRUDEX.kv with the engine, template, maker, the cert and dry c0 run outputs,
# the dry c0 record, the jobs and guard logs, listed in mr/MANIFEST_MR_V6_CRUDEX_CERT_c1.sha256 (paths relative to pk25/; verified); the record,
# outputs, engine, template, maker and jobs become read-only (a certified release); guard logs stay writable. Runs only if the cert run ended VALID.
set -u
set -o noclobber
D=/mnt/g2/release/root/code/pk25
O=$D/asm/out/out_kt_s9h_p3_v7_1_cert_c1_full.out
[ "$(awk '/^VERDICT/' $O)" = "VERDICT VALID (PART full; certified record)" ] || { echo "STOP: the cert run is not VALID"; exit 3; }
M=$D/mr/MANIFEST_MR_V6_CRUDEX_CERT_c1.sha256
[ -e $M ] && { echo "STOP: $M exists"; exit 3; }
F="mr/v6/MR_CRUDEX.kv asm/out/out_kt_s9h_p3_v7_1_cert_c1_full.out asm/out/out_kt_s9h_p3_v7_1_dry_c0_full.out asm/dry_c0/MR_CRUDEX.kv asm/kt_s9h_p3_v7_1.py asm/src/kt_s9h_p3_v7.py.in asm/make_kt_s9h_p3_v7.py jobs/job187_p3_v7_dry_c0.sh jobs/job189_p3_v7_cert.sh jobs/job190_p3_v7_freeze.sh guard/job187.log guard/job187_bashn.log guard/job189.log guard/job189_bashn.log"
for f in $F; do [ -f $D/$f ] || { echo "STOP: missing $f"; exit 3; }; done
( cd $D && /usr/bin/sha256sum $F ) > $M
for f in $F; do case $f in guard/*) ;; *) chmod a-w $D/$f ;; esac; done
chmod a-w $M
echo "MANIFEST $(/usr/bin/sha256sum $M | /usr/bin/cut -c1-8) entries $(/usr/bin/awk 'END{print NR}' $M)"
env -C $D /usr/bin/sha256sum -c --quiet $M && echo "VERIFY OK"
/usr/bin/awk '{print "SHA8", substr($1, 1, 8), $2}' $M
