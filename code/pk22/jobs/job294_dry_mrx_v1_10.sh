#!/bin/bash
# job294 (pk22; item (4), try 3 rerun): the SCRATCH dry copy of mrx_cert_v1_10 at N = 4 and 3, after try 2's dry parts were moved
# aside (out/SCRATCH_dry_v1_10/SCRATCH_try2_*); try 3's first outputs (rc 1, FileExistsError at the part write) are kept as SCRATCH_try3a_*.
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
C=$S/midrow/g4/mrc
O=$C/out
PY=python3
export TMPDIR=$C/tmp
echo "SRC $(/usr/bin/sha256sum $C/src/SCRATCH_dry_mrx_cert_v1_10.py | /usr/bin/cut -c1-8) SCRATCH_dry_mrx_cert_v1_10.py; $(/usr/bin/sha256sum $C/src/mrx_cert_v1_10.py | /usr/bin/cut -c1-8) mrx_cert_v1_10.py"
for N in 4 3; do
  for x in out err; do
    f=$O/SCRATCH_dry_mrx_cert_v1_10_n$N.$x
    if [ -e $f ]; then mv -n $f $O/SCRATCH_try3a_dry_mrx_cert_v1_10_n$N.$x; fi
    if [ -e $f ]; then echo "STOP: $f still there"; exit 3; fi
  done
  for V in U C; do
    p=$O/SCRATCH_dry_v1_10/MR_EXACT_PART_v1_10_${V}_N$N.kv
    if [ -e $p ]; then echo "STOP: $p exists"; exit 3; fi
  done
done
for N in 4 3; do
  o=$O/SCRATCH_dry_mrx_cert_v1_10_n$N.out
  env MALLOC_ARENA_MAX=2 $PY -I -B $C/src/SCRATCH_dry_mrx_cert_v1_10.py cert $N > $o 2> ${o%.out}.err
  echo "RUN N=$N rc=$?"
  /usr/bin/cut -c1-700 $o | /usr/bin/awk '/-> FAIL|DOES NOT FIRE|^(C-WAYA|PLANT-WAYA|RECORD|VERDICT)/'
  /usr/bin/tail -n 6 ${o%.out}.err
done
