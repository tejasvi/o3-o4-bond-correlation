#!/bin/bash
# job237 (pk22, MR_JOINT, main row 4506): freeze (a-w) the MR_JOINT build (template, maker, writer, job236 with its console, the run's
# output and err, the certified record MR_JOINT_CERT_v1.kv, this script) and write midrow/g4/mrc/MANIFEST_MRJ_CERT_v1.sha256 (verified).
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
E=$S/midrow/g4/mrc
F="$E/src/mrj_cert_v1.tmpl.py $E/src/make_mrj_v1.py $E/src/mrj_cert_v1.py $S/jobs/job236_mrj_v1.sh $S/jobs/job236_mrj_v1.console"
F="$F $E/out/mrj_cert_v1_cert.out $E/out/mrj_cert_v1_cert.err $E/out/cert/MR_JOINT_CERT_v1.kv $S/jobs/job237_mrj_v1_freeze.sh"
for f in $F; do [ -f "$f" ] || { echo "STOP: missing $f"; exit 3; }; done
chmod a-w $F
MAN=$E/MANIFEST_MRJ_CERT_v1.sha256
/usr/bin/sha256sum $F > $MAN
chmod a-w $MAN
echo "MANIFEST $(/usr/bin/sha256sum $MAN) entries $(/usr/bin/awk 'END{print NR}' $MAN)"
/usr/bin/sha256sum -c --quiet $MAN && echo "VERIFY OK"
/usr/bin/awk '{print "SHA8", substr($1, 1, 8), $2}' $MAN
