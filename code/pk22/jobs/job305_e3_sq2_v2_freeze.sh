#!/bin/bash
# job305 (pk22; item (3) part (6)): freeze the certified e3_sq2 v2 (job304): template, maker, the generated e3_sq2_v2.py, the records, run
# outputs and the job files become read-only and are listed in midrow/e3/MANIFEST_E3_SQ2_v2.sha256 (verified). Runs only if both runs end
# VERDICT VALID.
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
E=$S/midrow/e3
J=$S/jobs
for N in 4 3; do
  [ "$(/usr/bin/awk '/^VERDICT/' $E/out/e3_sq2_v2_n$N.out)" = "VERDICT VALID" ] || { echo "STOP: N=$N not VALID"; exit 3; }
done
M=$E/MANIFEST_E3_SQ2_v2.sha256
[ -e $M ] && { echo "STOP: $M exists"; exit 3; }
F="$E/src/e3_sq2_v2.tmpl.py $E/src/make_e3_sq2_v2.py $E/src/e3_sq2_v2.py $E/out/e3_sq2_v2_N4.json $E/out/e3_sq2_v2_N3.json $E/out/e3_sq2_v2_n4.out $E/out/e3_sq2_v2_n4.err $E/out/e3_sq2_v2_n3.out $E/out/e3_sq2_v2_n3.err $J/job304_e3_sq2_v2_cert.sh $J/job304_e3_sq2_v2_cert.console $J/job305_e3_sq2_v2_freeze.sh"
for f in $F; do [ -f $f ] || { echo "STOP: missing $f"; exit 3; }; done
chmod a-w $F
/usr/bin/sha256sum $F > $M
chmod a-w $M
echo "MANIFEST $(/usr/bin/sha256sum $M | /usr/bin/cut -c1-16) entries $(/usr/bin/awk 'END{print NR}' $M)"
/usr/bin/sha256sum -c --quiet $M && echo "VERIFY OK"
/usr/bin/awk '{n=split($2, a, "/"); print "SHA8", substr($1, 1, 8), a[n]}' $M
