#!/bin/bash
# job297 (pk22; item (4), MR_EXACT v1_10, certified runs on the word): mrx_cert_v1_10 (MANIFEST_MRX_CODE_v1_10) at N = 4 and 3 (outputs
# midrow/g4/mrc/out/mrx_cert_v1_10_cert_n<N>.out; parts out/cert/MR_EXACT_PART_v1_10_<U|C>_N<N>.kv), then mrx_combine_v1_10 (output
# out/mrx_combine_v1_10_a.out; record out/cert/MR_EXACT_CERT_v1_10_C.kv).
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
E=$S/midrow/g4/mrc
PY=python3
export TMPDIR=$E/tmp
/usr/bin/sha256sum -c --quiet $E/MANIFEST_MRX_CODE_v1_10.sha256 || { echo "STOP: code manifest"; exit 3; }
echo "CODE MANIFEST $(/usr/bin/sha256sum $E/MANIFEST_MRX_CODE_v1_10.sha256 | /usr/bin/cut -c1-8) verified"
for N in 4 3; do
  O=$E/out/mrx_cert_v1_10_cert_n${N}.out
  if [ -e $O ]; then echo "STOP: $O exists"; exit 3; fi
  env MALLOC_ARENA_MAX=2 $PY -I -B $E/src/mrx_cert_v1_10.py cert $N > $O 2> ${O%.out}.err
  echo "RUN N=$N rc=$?"
  /usr/bin/cut -c1-600 $O | /usr/bin/awk '/-> FAIL|DOES NOT FIRE|^(C-WAYA|PLANT-WAYA|RECORD|VERDICT)/'
  /usr/bin/tail -n 12 ${O%.out}.err
done
O=$E/out/mrx_combine_v1_10_a.out
if [ -e $O ]; then echo "STOP: $O exists"; exit 3; fi
$PY -I -B $E/src/mrx_combine_v1_10.py > $O 2> ${O%.out}.err
echo "COMBINE rc=$?"
/usr/bin/cut -c1-600 $O
/usr/bin/tail -n 12 ${O%.out}.err
