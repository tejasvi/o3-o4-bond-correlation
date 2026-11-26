#!/bin/bash
# job298 (pk22; item (4)): freeze the certified MR_EXACT v1_10 run (job297): outputs, parts, record and job files become read-only and
# are listed with the code manifest in midrow/g4/mrc/MANIFEST_MRX_CERT_v1_10.sha256 (verified). Runs only if both runs and the combine end
# VERDICT VALID.
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
E=$S/midrow/g4/mrc
J=$S/jobs
O=$E/out
for f in $O/mrx_cert_v1_10_cert_n4.out $O/mrx_cert_v1_10_cert_n3.out $O/mrx_combine_v1_10_a.out; do
  [ "$(/usr/bin/awk '/^VERDICT/{v=$0} END{print v}' $f)" = "VERDICT VALID" ] || { echo "STOP: $f not VALID"; exit 3; }
done
/usr/bin/sha256sum -c --quiet $E/MANIFEST_MRX_CODE_v1_10.sha256 || { echo "STOP: code manifest"; exit 3; }
M=$E/MANIFEST_MRX_CERT_v1_10.sha256
[ -e $M ] && { echo "STOP: $M exists"; exit 3; }
F="$E/MANIFEST_MRX_CODE_v1_10.sha256 $J/job297_mrx_v1_10_cert.sh $J/job297_mrx_v1_10_cert.console $O/mrx_cert_v1_10_cert_n4.out $O/mrx_cert_v1_10_cert_n4.err $O/mrx_cert_v1_10_cert_n3.out $O/mrx_cert_v1_10_cert_n3.err $O/mrx_combine_v1_10_a.out $O/mrx_combine_v1_10_a.err $O/cert/MR_EXACT_PART_v1_10_U_N4.kv $O/cert/MR_EXACT_PART_v1_10_U_N3.kv $O/cert/MR_EXACT_PART_v1_10_C_N4.kv $O/cert/MR_EXACT_PART_v1_10_C_N3.kv $O/cert/MR_EXACT_CERT_v1_10_C.kv $J/job298_mrx_v1_10_freeze.sh"
for f in $F; do [ -f $f ] || { echo "STOP: missing $f"; exit 3; }; done
chmod a-w $F
/usr/bin/sha256sum $F > $M
chmod a-w $M
echo "MANIFEST $(/usr/bin/sha256sum $M | /usr/bin/cut -c1-16) entries $(/usr/bin/awk 'END{print NR}' $M)"
/usr/bin/sha256sum -c --quiet $M && echo "VERIFY OK"
/usr/bin/awk '{n=split($2, a, "/"); print "SHA8", substr($1, 1, 8), a[n]}' $M
