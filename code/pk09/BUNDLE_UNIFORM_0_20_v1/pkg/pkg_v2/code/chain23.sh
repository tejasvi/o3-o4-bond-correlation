#!/bin/bash
# Production cover with the frozen certint3: segments run as sequential jobs (each <= 580 s, one core), every job
# resuming from the reach printed by the previous one.  A segment that stalls (q too small) hands its reach to the next
# segment, which then starts there.  usage: chain22.sh PREFIX "L I start end q0 qmax maxjobs" ...
cd /mnt/g2/release/root/data/e17/unif/scratch || exit 1
PFX=$1; shift
run() {
    env TMPDIR=/mnt/g2/release/root/data/e17/unif/scratch/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 \
        timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B code4/certint4.py "$@"
}
seg=0
reach=""
for spec in "$@"; do
    seg=$((seg + 1))
    set -- $spec
    L=$1; I=$2; a=$3; e=$4; q=$5; qm=$6; nj=$7
    if [ -n "$reach" ]; then
        a=$(awk -v a="$a" -v r="$reach" 'BEGIN {print (r < a) ? r : a}')
    fi
    k=1
    while [ "$k" -le "$nj" ]; do
        tag=${PFX}${seg}_${k}
        log=out/cover4_${tag}.log
        [ -e "$log" ] && { echo "log $log exists; stop" >> out/chain23_${PFX}.log; exit 1; }
        run "$tag" "$L" "$I" "adapt:$a:$e:$q:$qm" > "$log" 2>&1
        rc=$?
        line=$(awk '/adaptive cover: reached a =/' "$log")
        printf '%s seg %d job %d (L=%s I=%s) rc=%s: %s\n' "$(date -u +%FT%TZ)" "$seg" "$k" "$L" "$I" "$rc" "$line" >> out/chain23_${PFX}.log
        [ -n "$line" ] || exit 1
        a=$(echo "$line" | awk '{print $6}')
        q=$(echo "$line" | awk '{print $NF}')
        reach=$a
        awk '/q too small/ {f=1} END {exit !f}' "$log" && { echo "segment $seg stalled at $a" >> out/chain23_${PFX}.log; break; }
        awk -v a="$a" -v e="$e" 'BEGIN {exit !(a >= e)}' && break
        k=$((k + 1))
    done
done
echo "$(date -u +%FT%TZ) chain done, reach $reach" >> out/chain23_${PFX}.log
