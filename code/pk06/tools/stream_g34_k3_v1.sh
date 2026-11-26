#!/bin/bash
# stream_g34_k3_v1.sh N J1 FIRST ATTEMPT -- pk06, P2-13 full run (the approval, option (1)): engine kt_lbu_g34_pk06_v1.py (8b7aff00)
# unchanged, K = 3, P3 x P4, one N: orbits G<FIRST>..G19 in order, one guarded job each (tools/job_run_g34_v1.sh: cap 0.08 core-h,
# LIM 250 s, wall 540 s), sigma 1/4; an orbit not certified at 1/4 is rerun once at 1/3. Before each job: the engine sha8, a new
# output name, and the inbox (one file: stat, then jq length; a pending message pauses the stream). Stops with
# runs/STOP_n<N>_a<ATTEMPT>.txt at the first job whose VERDICT is not VALID, an orbit certified at neither sigma, or a check above.
P=/mnt/g2/release/root/code/pk06
INB=/mnt/g2/release/root/data/pause_pk06.json
N=$1; J1=$2; FIRST=$3; A=$4
case "$N:$J1" in 3:300|4:350) ;; *) echo "bad N J1"; exit 2;; esac
case "$FIRST" in [1-9]|1[0-9]) ;; *) echo "bad FIRST"; exit 2;; esac
case "$A" in [1-9]) ;; *) echo "bad ATTEMPT"; exit 2;; esac
LOG=$P/runs/stream_n${N}_a${A}.log
STOP=$P/runs/STOP_n${N}_a${A}.txt
set -C
stop() { printf '%s STOP %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" >> "$LOG"; printf '%s STOP %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" > "$STOP"; exit "$2"; }
for i in $(seq "$FIRST" 19); do
  o=$(printf 'G%02d' "$i")
  ok=0
  for sg in 1/4 1/3; do
    name=full_n${N}_${o}_s${sg/\//}_v1
    out=$P/runs/$name.out
    [ "$(sha256sum $P/kt_lbu_g34_pk06_v1.py | cut -c1-8)" = "7c437dd0" ] || stop "engine sha8 changed before $name" 6
    [ -e "$out" ] && stop "output $name exists" 7
    if [ -f "$INB" ] && nm=$(jq length "$INB"); then :; else nm=unreadable; fi
    [ "$nm" = "0" ] || stop "before $name: inbox holds $nm message(s) (pause, not a failure)" 5
    rc=$(bash $P/tools/job_run_g34_v1.sh "$name" 0.08 20 250 540 -- 3 3 4 "$N" "$J1" "$o" "$sg" none 6500)
    v=$(awk '$1 == "SUMMARY" && match($0, /VERDICT [A-Z]+/) {print substr($0, RSTART + 8, RLENGTH - 8)}' "$out")
    c=$(awk '$1 == "R-CERT" && match($0, /certified [A-Za-z]+/) {print substr($0, RSTART + 10, RLENGTH - 10)}' "$out")
    printf '%s %s %s verdict=%s certified=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$name" "$rc" "$v" "$c" >> "$LOG"
    [ "$v" = "VALID" ] || stop "$name: VERDICT ${v:-none} ($rc)" 3
    if [ "$c" = "True" ]; then ok=1; break; fi
  done
  [ "$ok" = 1 ] || stop "$o: certified at neither sigma" 4
done
printf '%s STREAM n%s a%s DONE\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$N" "$A" >> "$LOG"
