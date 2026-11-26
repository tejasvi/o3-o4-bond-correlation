#!/bin/bash
# job296 (pk22; item (4)): freeze the MR_EXACT v1_10 code before the certified runs: try 1's maker (never cited) moves aside to a
# SCRATCH_try1_ name; the makers, generated scripts, diffs and the build and dry-test jobs (job292, job294, job295) become read-only and are
# listed in midrow/g4/mrc/MANIFEST_MRX_CODE_v1_10.sha256 (verified). The SCRATCH dry copies and their outputs stay unlisted (never cited).
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
C=$S/midrow/g4/mrc
J=$S/jobs
if [ -e $C/src/make_mrx_v1_10.py ]; then
  mv -n $C/src/make_mrx_v1_10.py $C/src/SCRATCH_try1_make_mrx_v1_10.py
  [ -e $C/src/make_mrx_v1_10.py ] && { echo "STOP: try 1 maker still in place"; exit 3; }
  echo "MOVED try 1 maker to SCRATCH_try1_make_mrx_v1_10.py"
fi
M=$C/MANIFEST_MRX_CODE_v1_10.sha256
[ -e $M ] && { echo "STOP: $M exists"; exit 3; }
F="$C/src/make_mrx_v1_10_r2.py $C/src/mrx_cert_v1_10.py $C/src/diff_mrx_cert_v1_9_to_v1_10.txt $C/src/make_mrx_combine_v1_10.py $C/src/mrx_combine_v1_10.py $C/src/diff_mrx_combine_v1_9_to_v1_10.txt $J/job292_make_mrx_v1_10_r2.sh $J/job292_make_mrx_v1_10_r2.console $J/job294_dry_mrx_v1_10.sh $J/job294_dry_mrx_v1_10.console $J/job295_make_combine_v1_10.sh $J/job295_make_combine_v1_10.console $J/job296_freeze_mrx_code_v1_10.sh"
for f in $F; do [ -f $f ] || { echo "STOP: missing $f"; exit 3; }; done
chmod a-w $F
/usr/bin/sha256sum $F > $M
chmod a-w $M
echo "MANIFEST $(/usr/bin/sha256sum $M | /usr/bin/cut -c1-16) entries $(/usr/bin/awk 'END{print NR}' $M)"
/usr/bin/sha256sum -c --quiet $M && echo "VERIFY OK"
/usr/bin/awk '{n=split($2, a, "/"); print "SHA8", substr($1, 1, 8), a[n]}' $M
