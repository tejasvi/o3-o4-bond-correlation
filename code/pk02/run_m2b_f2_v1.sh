#!/bin/bash
# run_m2b_f2_v1.sh -- pk02 (code/pk02/). The certified M2(b) rerun for the two trade fixes as authorized (after
# the CHECK 849eeb24 and ADD1 6a4fb7e3 and the d1c1ca7c): MANIFEST_M2B_F2_FIX_v2.sha256 (whose own sha256 must start c9a7d1ed),
# ONE JOB AT A TIME:
#   m2b_floatref_v2.py at N = 4 and 3 (the C-REP twin; estimate 280 s each, its own RLIMIT 540);
#   m2b_cert_v1_4.py pieces, per N = 4 then 3: tA (estimate 15 s, LIM 30, AS 8 GiB), r0 (90 s, LIM 180, AS 8 GiB), d5 (330 s, LIM 540,
#   AS 16 GiB), dwt and dwl (500 s each, LIM 560, timeout 590, AS 16 GiB; EARLY_CPU 320 as v1_2); no dw (nothing reads it);
#   m2b_rep_v1_5.py at N = 4 and 3 (C-REP; seconds).
# Cap 1.5 core-h = 5400 s over the CPU of this rerun's records (user + system from /usr/bin/time -v): a job starts only if that CPU + its LIM
# + 6 <= 5400. Stops at the first record whose VERDICT lines are not exactly ["VERDICT VALID"] (EARLY-STOP and CAP-STOP included), on an
# MAFallback, on a job above twice its estimate, on a missing or mismatched hand-off, if a record or hand-off already exists, if root free
# space is below 886 GiB or MemAvailable below 24 GiB, and (the gap) on a d5, dwt or dwl record without C-RADV and C-TMONO PASS lines.
# One line per step in out/run_m2b_f2_v1.log with CPU, peak RSS, bytes written and the piece's STAGE-CPU, MAJFIX and gate lines.
D=/mnt/g2/release/root/code/pk02
L=$D/out/run_m2b_f2_v1.log
M=$D/MANIFEST_M2B_F2_FIX_v2.sha256
CAP=5400
TMPD=$D/tmp_m2b_c11
shopt -s nullglob
stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
M8=$(sha256sum "$M" < /dev/null | cut -c1-8)
if [ "$M8" != c9a7d1ed ]; then echo "SHA MISMATCH manifest $M8 $(stamp)" >> "$L"; exit 3; fi
if ! sha256sum -c --quiet "$M" < /dev/null > /dev/null 2>&1; then echo "SHA MISMATCH: a file in the manifest differs $(stamp)" >> "$L"; exit 3; fi
for s in m2b_cert_v1_4.py m2b_floatref_v2.py m2b_rep_v1_5.py majfix_v1_1.py; do
  pin=$(awk -v p="$D/$s" '$2 == p {print $1}' "$M")
  got=$(sha256sum "$D/$s" < /dev/null | cut -c1-64)
  if [ -z "$pin" ] || [ "$pin" != "$got" ]; then echo "SHA MISMATCH $s $(stamp)" >> "$L"; exit 3; fi
done
echo "SHA OK manifest $M8 (every entry; m2b_cert_v1_4, m2b_floatref_v2, m2b_rep_v1_5, majfix_v1_1 in it) $(stamp)" >> "$L"
mkdir -p "$TMPD" || exit 3
cpuof() { awk -F': ' '/User time \(seconds\)|System time \(seconds\)/ {s += $2} END {printf "%.1f", s + 0}' "$@" /dev/null; }
used() { local errs; errs=("$D"/out/out_m2b_floatref_v2_*.err "$D"/out_m2b_cert_v1_4_*.err "$D"/out/out_m2b_rep_v1_5_*.err); cpuof "${errs[@]}"; }
rssof() { awk -F': ' '/Maximum resident set size \(kbytes\)/ {m = $2} END {printf "%.0f", m / 1024}' "$1"; }
sz() { if [ -e "$1" ]; then stat -c %s "$1"; else echo 0; fi; }
rootok() { df -B1 --output=avail / | awk 'NR == 2 {ok = ($1 >= 886 * 1073741824)} END {exit !ok}'; }
memok() { awk '/^MemAvailable:/ {ok = ($2 >= 24 * 1048576)} END {exit !ok}' /proc/meminfo; }
guards() {
  local u
  u=$(used)
  if ! awk -v u="$u" -v l="$2" -v c="$CAP" 'BEGIN {exit !(u + l + 6 <= c)}'; then
    echo "CAP-GUARD: used $u s, $1 could need $(($2 + 6)) s, cap $CAP s $(stamp)" >> "$L"; exit 6
  fi
  if ! rootok; then echo "DISK-GUARD: root free below 886 GiB before $1 $(stamp)" >> "$L"; exit 7; fi
  if ! memok; then echo "MEM-GUARD: MemAvailable below 24 GiB before $1 $(stamp)" >> "$L"; exit 7; fi
}
twox() { if ! awk -v c="$2" -v x="$3" 'BEGIN {exit !(c <= 2 * x)}'; then echo "STOP-2X: $1 cpu $2 s above twice its estimate $3 s $(stamp)" >> "$L"; exit 5; fi; }
valid() { if [ "$(awk '/^VERDICT/' "$2")" != "VERDICT VALID" ]; then echo "STOP: $1 not VALID ($(awk '/^VERDICT/' "$2" | head -c 300)) $(stamp)" >> "$L"; exit 5; fi; }
float_job() {
  local n o e rc c
  n=$1; o=$D/out/out_m2b_floatref_v2_n$n.out; e=${o%.out}.err
  for f in "$o" "$e"; do if [ -e "$f" ]; then echo "EXISTS ${f##*/} $(stamp)" >> "$L"; exit 4; fi; done
  guards "floatref_v2 n$n" 540
  echo "launch floatref_v2 n$n (estimate 280 s; its RLIMIT 540) $(stamp); used $(used) s" >> "$L"
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=$TMPD OMP_NUM_THREADS=1 timeout 580 nice -n 10 /usr/bin/time -v \
    prlimit --as=8589934592 -- python3 -I -B "$D/m2b_floatref_v2.py" "$n" > "$o" 2> "$e"
  rc=$?
  chmod 444 "$o" "$e"
  c=$(cpuof "$e")
  echo "floatref_v2 n$n rc $rc cpu $c s peak RSS $(rssof "$e") MiB, bytes written $(($(sz "$o") + $(sz "$e"))) $(stamp)" >> "$L"
  awk '/^(FIX|FREF|C-HASH|C-VERBATIM)/ {print "  " substr($0, 1, 200)}' "$o" >> "$L"
  valid "floatref_v2 n$n" "$o"
  twox "floatref_v2 n$n" "$c" 280
  echo "floatref_v2 n$n VALID $(stamp); used $(used) s of $CAP" >> "$L"
}
cert_job() {
  local i est lim as to o e h rc c bo be bh k hn hs p
  i=$1; est=$2; lim=$3; as=$4; to=$5; p=${i%%.*}
  o=$D/out_m2b_cert_v1_4_$i.out; e=${o%.out}.err; h=$D/hand_m2b_cert_v1_4_$i.txt
  for f in "$o" "$e" "$h"; do if [ -e "$f" ]; then echo "EXISTS ${f##*/} $(stamp)" >> "$L"; exit 4; fi; done
  guards "$i" "$lim"
  echo "launch $i LIM $lim AS $as (estimate $est s) $(stamp); used $(used) s" >> "$L"
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=$TMPD OMP_NUM_THREADS=1 timeout "$to" nice -n 10 /usr/bin/time -v \
    prlimit --as="$as" -- python3 -I -B "$D/m2b_cert_v1_4.py" "$i" "$lim" > "$o" 2> "$e"
  rc=$?
  chmod 444 "$o" "$e"
  c=$(cpuof "$e"); bo=$(sz "$o"); be=$(sz "$e"); bh=$(sz "$h")
  echo "$i rc $rc cpu $c s (estimate $est, LIM $lim) peak RSS $(rssof "$e") MiB, bytes written $((bo + be + bh)) (record $bo, stderr $be, hand-off $bh) $(stamp)" >> "$L"
  awk '/^(STAGE-CPU|EARLY-STOP|CAP-STOP|MAJFIX|C-RADV|C-TMONO|C-DEG|C-P0SUB|C-MAJ-SAMPLE N|PLANT-TRADE-POS|C-TRADE-POS)/ {print "  " substr($0, 1, 220)}' "$o" >> "$L"
  if /usr/bin/grep -q -E 'MAFALLBACK|MAFallback' "$o" "$e"; then echo "STOP-MAFALLBACK: $i $(stamp)" >> "$L"; exit 5; fi
  valid "$i" "$o"
  twox "$i" "$c" "$est"
  if [ "$p" = d5 ] || [ "$p" = dwt ] || [ "$p" = dwl ]; then
    if ! /usr/bin/grep -q -E '^C-RADV N=[34]: .* -> PASS; PLANT-RADV .* -> FIRES$' "$o" || ! /usr/bin/grep -q -E '^C-TMONO N=[34] .* -> PASS$' "$o"; then
      echo "STOP-GATES: $i lacks a C-RADV PASS / PLANT-RADV FIRES or a C-TMONO PASS line $(stamp)" >> "$L"; exit 5
    fi
  fi
  k=$(awk '/^HANDOFF / && / sha256 / {j++} END {print j + 0}' "$o")
  hn=$(awk '/^HANDOFF / && / sha256 / {print $5}' "$o")
  hs=$(awk '/^HANDOFF / && / sha256 / {print $7}' "$o")
  if [ "$k" != 1 ] || [ "$hn" != "${h##*/}" ] || [ ! -f "$h" ] || [ "$(sha256sum "$h" < /dev/null | cut -c1-64)" != "$hs" ]; then
    echo "STOP-HANDOFF: $i hand-off missing or not the one the record names (lines $k) $(stamp)" >> "$L"; exit 5
  fi
  chmod 444 "$h"
  echo "$i VALID, hand-off ${h##*/} sha256 $(printf '%s' "$hs" | cut -c1-8) $(stamp); used $(used) s of $CAP" >> "$L"
}
rep_job() {
  local n o e c
  n=$1; o=$D/out/out_m2b_rep_v1_5_n$n.out; e=${o%.out}.err
  for f in "$o" "$e"; do if [ -e "$f" ]; then echo "EXISTS ${f##*/} $(stamp)" >> "$L"; exit 4; fi; done
  guards "rep_v1_5 n$n" 60
  OMP_NUM_THREADS=1 timeout 300 nice -n 10 /usr/bin/time -v prlimit --as=4294967296 -- python3 -I -B "$D/m2b_rep_v1_5.py" "$n" > "$o" 2> "$e"
  chmod 444 "$o" "$e"
  c=$(cpuof "$e")
  echo "rep_v1_5 n$n cpu $c s, bytes written $(($(sz "$o") + $(sz "$e"))) $(stamp)" >> "$L"
  awk '/^(C-REP |C-REP-BOUND|C-REP-READ|C-ANCHOR|PLANT-REP|PLANT-ANCHOR)/ && !/-> PASS$/ {print "  " substr($0, 1, 220)}' "$o" >> "$L"
  awk '/^(C-REP D5|C-REP R0|C-REP ANN_0.6|C-REP D5W)/ {print "  " substr($0, 1, 200)}' "$o" >> "$L"
  valid "rep_v1_5 n$n" "$o"
  echo "rep_v1_5 n$n VALID $(stamp)" >> "$L"
}
echo "start $(stamp); used $(used) s" >> "$L"
float_job 4
float_job 3
for n in 4 3; do
  cert_job "tA.n$n" 15 30 8589934592 300
  cert_job "r0.n$n" 90 180 8589934592 300
  cert_job "d5.n$n" 330 540 17179869184 580
  cert_job "dwt.n$n" 500 560 17179869184 590
  cert_job "dwl.n$n" 500 560 17179869184 590
  echo "N=$n DONE $(stamp); used $(used) s" >> "$L"
done
rep_job 4
rep_job 3
echo "DONE $(stamp); used $(used) s of $CAP" >> "$L"
