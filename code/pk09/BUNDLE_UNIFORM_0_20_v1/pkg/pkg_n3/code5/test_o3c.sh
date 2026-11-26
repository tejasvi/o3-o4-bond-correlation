#!/bin/bash
# First N = 3 certifier tests on single intervals (one per planned segment), sequential jobs < 10 min, one core.
cd /mnt/g2/release/root/data/e17/unif/scratch || exit 1
LOG=out/test_o3c.log
run() {
    env TMPDIR=/mnt/g2/release/root/data/e17/unif/scratch/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 \
        timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B code5/o3cert.py "$@"
}
for spec in "o3t1 10 3 0.01:0.0001" "o3t2 12 4 1:0.02" "o3t3 14 6 2.5:0.012" "o3t4 16 6 2.95:0.012"; do
    set -- $spec
    [ -e out/o3cert_$1.txt ] && { echo "out/o3cert_$1.txt exists" >> $LOG; exit 1; }
    run "$@" > out/o3cert_$1.stdout 2>&1
    rc=$?
    echo "$(date -u +%FT%TZ) $1 (L=$2 I=$3 $4) rc=$rc: $(awk '/==>|not certified|too large|exception|Error/' out/o3cert_$1.stdout | tail -n 1)" >> $LOG
    [ $rc -eq 0 ] || exit 1
done
echo "$(date -u +%FT%TZ) tests done" >> $LOG
