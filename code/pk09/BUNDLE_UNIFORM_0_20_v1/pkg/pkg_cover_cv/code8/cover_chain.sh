#!/bin/bash
# Wave 18, [3, 20] cover with certint6 (vec truncation, frob lambda_5; UNIF 9.24-9.27).  Sequential jobs on one core,
# each under 580 s (certint6 stops its adaptive loop at 520 s).  The cover resumes from the ledger: the covered reach a
# is the end of the chain of CERT intervals starting at JA; the next job covers [a, min(floor(a) + 1, JB)] with
# L = ceil(sqrt(44 J_end)) (>= the RV11_25 minimum ceil(sqrt(41 J))) and I = 6, starting at h = 0.045 (q0 = 0.045/a,
# qmax = 0.065/a).  frob lambda_5 bound (9.26) everywhere, vec truncation (9.24, 9.25, 9.27).
# Stops: reach >= JB; two jobs in a row without progress; a new job would push the job wall time past GUARD (cap 1.5 core-h).
# usage: cover_chain.sh plan|run [GUARD_SECONDS]
S=/mnt/g2/release/root/data/e17/unif/scratch
MODE=$1
GUARD=${2:-5400}
JA=3.0; JB=20.0
LEDGER=${COVER_LEDGER:-$S/out/cover6_cv.ledger}          # overridable for script tests only
TIMES=${COVER_TIMES:-$S/out/cover6_cv.times}
STATUS=${COVER_STATUS:-$S/out/cover6_cv.status}
W="env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=$S/tmp timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B"
cd $S || exit 1
case "$MODE" in plan|run) ;; *) echo "usage: cover_chain.sh plan|run [GUARD_SECONDS]"; exit 2 ;; esac
reach() {       # end of the chain of CERT intervals [J0 - h, J0 + h] that starts at JA
    if [ ! -s "$LEDGER" ]; then echo "$JA"; return; fi
    awk -v a="$JA" 'BEGIN { n = 0 } $5 == "CERT" { lo[n] = $1 - $2; hi[n] = $1 + $2; n++ }
        END { ch = 1; while (ch) { ch = 0; for (i = 0; i < n; i++) if (lo[i] <= a && hi[i] > a) { a = hi[i]; ch = 1 } } printf "%.17g\n", a }' "$LEDGER"
}
used() { if [ -s "$TIMES" ]; then awk '{ s += $2 } END { printf "%d\n", s }' "$TIMES"; else echo 0; fi; }
CODESHA=$(cd $S && sha256sum code8/certint6.py code8/mfops.py code8/mfstruct2.py code8/mfstruct.py code8/lam5frob.py code4/certlib3.py code4/tm2.py | sha256sum | cut -c1-16)
echo "$(date -u +%H:%M:%SZ) start ($MODE), code hash $CODESHA, guard $GUARD s" >> "$STATUS"
nojob=0
while true; do
    a=$(reach)
    done_=$(awk -v a="$a" -v b="$JB" 'BEGIN { print (a >= b) ? 1 : 0 }')
    if [ "$done_" = 1 ]; then echo "cover reached $a >= $JB" | tee -a "$STATUS"; break; fi
    u=$(used)
    if [ $((u + 600)) -gt "$GUARD" ]; then echo "GUARD: job wall time $u s + 600 s > $GUARD s at reach $a; stop and re-price" | tee -a "$STATUS"; break; fi
    read JE L Q0 QM < <(awk -v a="$a" -v b="$JB" 'BEGIN { je = int(a) + 1; if (je > b) je = b; l = int(sqrt(44 * je)); if (l * l < 44 * je) l++;
        printf "%.17g %d %.6g %.6g\n", je, l, 0.045 / a, 0.065 / a }')
    k=$(ls $S/out/ | awk '/^certint6_cv_[0-9]+\.txt$/ { n++ } END { print n + 1 }')
    TAG=$(printf "cv_%03d" "$k")
    CMD="code8/certint6.py $TAG $L 6 adapt:$a:$JE:$Q0:$QM vec frob"
    if [ "$MODE" = plan ]; then echo "plan: reach $a, used $u s; next: $CMD"; break; fi
    now=$(cd $S && sha256sum code8/certint6.py code8/mfops.py code8/mfstruct2.py code8/mfstruct.py code8/lam5frob.py code4/certlib3.py code4/tm2.py | sha256sum | cut -c1-16)
    if [ "$now" != "$CODESHA" ]; then echo "STOP: certifier code changed during the cover ($now != $CODESHA)" | tee -a "$STATUS"; break; fi
    t0=$(date +%s)
    $W $CMD > $S/tmp/$TAG.log 2>&1
    rc=$?
    t1=$(date +%s)
    echo "$TAG $((t1 - t0)) rc=$rc L=$L from=$a to=$JE" >> "$TIMES"
    a2=$(reach)
    prog=$(awk -v a="$a" -v b="$a2" 'BEGIN { print (b > a) ? 1 : 0 }')
    if [ "$prog" = 1 ]; then nojob=0; else nojob=$((nojob + 1)); fi
    echo "$(date -u +%H:%M:%SZ) $TAG rc=$rc $((t1 - t0)) s, reach $a -> $a2" >> "$STATUS"
    if [ "$nojob" -ge 2 ]; then echo "STOP: two jobs without progress at reach $a2" | tee -a "$STATUS"; break; fi
done
