#!/bin/bash
# job234 (pk22, MR_EXACT v1_9 with H4TH's certified J-laws, main row 4485): the diff midrow/g4/mrc/src/diff_mrx_cert_v1_8_to_v1_9.txt
# (unified, noclobber), then freeze (a-w) the v1_9 build (maker, writer, combine, the diff, job233 with its console, both runs' outputs and
# errs, the combine's output and err, the four parts, the certified record MR_EXACT_CERT_v1_9_C.kv, this script) and write
# midrow/g4/mrc/MANIFEST_MRX_CERT_v1_9.sha256 (verified).
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
E=$S/midrow/g4/mrc
DF=$E/src/diff_mrx_cert_v1_8_to_v1_9.txt
/usr/bin/diff -u $E/src/mrx_cert_v1_8.py $E/src/mrx_cert_v1_9.py > $DF
echo "DIFF rc=$? lines $(/usr/bin/awk 'END{print NR}' $DF)"
F="$E/src/make_mrx_v1_9.py $E/src/mrx_cert_v1_9.py $E/src/mrx_combine_v1_9.py $DF $S/jobs/job233_mrx_v1_9.sh $S/jobs/job233_mrx_v1_9.console"
for N in 4 3; do F="$F $E/out/mrx_cert_v1_9_cert_n$N.out $E/out/mrx_cert_v1_9_cert_n$N.err"; done
F="$F $E/out/mrx_combine_v1_9_a.out $E/out/mrx_combine_v1_9_a.err"
for V in U C; do for N in 4 3; do F="$F $E/out/cert/MR_EXACT_PART_v1_9_${V}_N$N.kv"; done; done
F="$F $E/out/cert/MR_EXACT_CERT_v1_9_C.kv $S/jobs/job234_mrx_v1_9_freeze.sh"
for f in $F; do [ -f "$f" ] || { echo "STOP: missing $f"; exit 3; }; done
chmod a-w $F
MAN=$E/MANIFEST_MRX_CERT_v1_9.sha256
/usr/bin/sha256sum $F > $MAN
chmod a-w $MAN
echo "MANIFEST $(/usr/bin/sha256sum $MAN) entries $(/usr/bin/awk 'END{print NR}' $MAN)"
/usr/bin/sha256sum -c --quiet $MAN && echo "VERIFY OK"
/usr/bin/awk '$2 ~ /(MR_EXACT_CERT_v1_9_C\.kv|mrx_cert_v1_9\.py|mrx_combine_v1_9\.py|make_mrx_v1_9\.py|cert_n[34]\.out|combine_v1_9_a\.out|diff_mrx_cert_v1_8_to_v1_9\.txt)$/ {print "SHA8", substr($1, 1, 8), $2}' $MAN
