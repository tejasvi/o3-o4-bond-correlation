#!/bin/bash
# N = 3 engine validation: m-basis brute force (Lb = 2, 3) against code5/o3sparse.py, then the exact quadruple table
# against the float engine (o3check.py) at L = 6, 10, 12.  Sequential jobs < 10 min, one core.
cd /mnt/g2/release/root/data/e17/unif/scratch || exit 1
LOG=out/val_o3.log
run() {
    env TMPDIR=/mnt/g2/release/root/data/e17/unif/scratch/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 \
        timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B "$@"
}
[ -e $LOG ] && { echo "$LOG exists"; exit 1; }
run code5/o3brute.py 2 0.5,1.3 2,3,4 >> $LOG 2>&1; echo "$(date -u +%FT%TZ) o3brute Lb=2 rc=$?" >> $LOG
run code5/o3brute.py 3 0.7,2.0 2,3,5 >> $LOG 2>&1; echo "$(date -u +%FT%TZ) o3brute Lb=3 rc=$?" >> $LOG
run code5/o3check.py 6 1.3 >> $LOG 2>&1; echo "$(date -u +%FT%TZ) o3check L=6 rc=$?" >> $LOG
run code5/o3check2.py 6 1.3 >> $LOG 2>&1; echo "$(date -u +%FT%TZ) o3check2 L=6 rc=$?" >> $LOG
run code5/o3check2.py 8 2.5 >> $LOG 2>&1; echo "$(date -u +%FT%TZ) o3check2 L=8 rc=$?" >> $LOG
run code5/o3check.py 10 0.5 >> $LOG 2>&1; echo "$(date -u +%FT%TZ) o3check L=10 rc=$?" >> $LOG
run code5/o3check.py 12 2.0 >> $LOG 2>&1; echo "$(date -u +%FT%TZ) o3check L=12 rc=$?" >> $LOG
echo "$(date -u +%FT%TZ) validation done" >> $LOG
