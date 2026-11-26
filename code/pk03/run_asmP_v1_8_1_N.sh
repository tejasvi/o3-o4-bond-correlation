#!/bin/bash
# run_asmP_v1_8_1_N.sh -- pk03 (code/pk03/). The partial assembly (option 5) for one N: pycheck on m3_run_v1_8_1.py and
# its modules (own output name), then m3_run_v1_8_1.py asmP.N, with the batch scripts' rules: its .out and .err must not exist; LIM =
# min(540, CAP_S - used - 5) with CPU so far = this shell's reaped children, and below 150 s the chain stops for re-pricing; VERDICT lines
# exactly ['VERDICT VALID'] or stop; the output must name exactly four records (D, E2, E3, FF) on RECORD lines, none of them an N record.
# Then the four records and the asmP output are chmod 444 and MANIFEST_m3_run_v1_8_1_asmP.N.sha256 is written from sha256sum of the
# output and the four records.
# Usage: bash run_asmP_v1_8_1_N.sh N CAP_S   (log: out/chain_asmP_v1_8_1_nN.log)
D=/mnt/g2/release/root/code/pk03
RUN=$D/m3_run_v1_8_1.py
N=$1
CAP_S=$2
case "$N" in 3|4) ;; *) echo "usage: bash run_asmP_v1_8_1_N.sh N CAP_S (N = 3 or 4)"; exit 2;; esac
case "$CAP_S" in ''|*[!0-9]*) echo "usage: bash run_asmP_v1_8_1_N.sh N CAP_S"; exit 2;; esac
LOG=$D/out/chain_asmP_v1_8_1_n$N.log
set -o noclobber
HZ=$(getconf CLK_TCK)

stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
say() { echo "$(stamp) $*" >> $LOG; echo "$(stamp) $*"; }
child_cpu() { awk -v hz=$HZ '{ printf "%.1f\n", ($16 + $17) / hz }' /proc/$$/stat; }
verdict_valid() { awk 'index($0, "VERDICT") == 1 { n++; v = $0 } END { exit !(n == 1 && v == "VERDICT VALID") }' "$1"; }
verdict_of() { awk 'index($0, "VERDICT") == 1 { print; n++ } END { if (!n) print "(no VERDICT line)" }' "$1" | tr '\n' ' '; }

say "CHAIN start N $N: m3_run_v1_8_1.py $(sha256sum $RUN | cut -c1-8); $(basename $0) $(sha256sum $0 | cut -c1-8); cap $CAP_S s"
O=$D/out/m3_run_v1_8_1_asmP.$N.out
E=$D/out/m3_run_v1_8_1_asmP.$N.err
PO=$D/out/m3_pycheck_v1_run_v1_8_1_n$N.out
PE=$D/out/m3_pycheck_v1_run_v1_8_1_n$N.err
for f in "$O" "$E" "$PO" "$PE"; do [ ! -e "$f" ] || { say "STOP: $f exists"; exit 1; }; done
OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --cpu=120:125 -- python3 -I -B $D/m3_pycheck_v1.py \
    $RUN $D/m3_reader_v4_4.py $D/m3_record_v4.py $D/m3_bar_v10.py $D/m3_scal_v2.py $D/m3_graph_v3.py $D/m3_series_v2.py \
    $D/m3_major_v2.py $D/m3_entries_v3.py $D/m3_handoff_v3.py > "$PO" 2> "$PE"
say "END pycheck rc $? $(verdict_of "$PO"); out sha256 $(sha256sum "$PO" | cut -c1-8)"
verdict_valid "$PO" || { say "STOP after pycheck"; exit 1; }
u0=$(child_cpu)
lim=$(awk -v c="$CAP_S" -v u="$u0" 'BEGIN { l = int(c - u - 5); if (l > 540) l = 540; print l }')
[ "$lim" -ge 150 ] || { say "STOP: LIM $lim s under the cap $CAP_S s is below 150 s; re-price"; exit 1; }
say "START asmP.$N LIM $lim (CPU so far $u0 s of $CAP_S)"
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=$D/tmp timeout 580 nice -n 10 prlimit --as=8589934592 -- \
    python3 -I -B $RUN asmP.$N $lim > "$O" 2> "$E"
rc=$?
say "END asmP.$N rc $rc CPU $(awk -v a="$u0" -v b="$(child_cpu)" 'BEGIN { printf "%.1f", b - a }') s; $(verdict_of "$O"); out sha256 $(sha256sum "$O" | cut -c1-8); err $(wc -c < "$E") bytes"
verdict_valid "$O" || { say "STOP after asmP.$N: VERDICT lines are not exactly [VERDICT VALID]"; exit 1; }
RECS=$(awk 'index($0, "RECORD ") == 1 && NF == 3 { print "out/" $2 }' "$O")
[ "$(echo "$RECS" | awk 'NF' | wc -l)" -eq 4 ] || { say "STOP: asmP.$N does not name four records"; exit 1; }
echo "$RECS" | awk -v n=$N '{ f = $0; sub(/^out\//, "", f); ok += (f == "m3_s8v3_D_N" n "_J300_v1_8_1.json" || f == "m3_s8v3_E2_N" n "_J300_v1_8_1.json" || f == "m3_s8v3_E3_N" n "_J300_v1_8_1.json" || f == "m3_s8v3_FF_N" n "_J300_v1_8_1.json") } END { exit !(ok == 4) }' \
    || { say "STOP: asmP.$N names a record other than the D, E2, E3 and FF ones"; exit 1; }
(cd $D && chmod 444 $RECS && chmod 444 out/$(basename $O)) || { say "STOP: chmod 444 failed"; exit 1; }
M=$D/MANIFEST_m3_run_v1_8_1_asmP.$N.sha256
(cd $D && sha256sum out/$(basename $O) $RECS > $M) && chmod 444 $M || { say "STOP: side manifest for asmP.$N not written"; exit 1; }
(cd $D && sha256sum -c --quiet $M) || { say "STOP: side manifest check failed for asmP.$N"; exit 1; }
say "SIDE-MANIFEST $(basename $M) $(sha256sum $M | cut -c1-8) ($(wc -l < $M) lines)"
say "CHAIN end N $N: CPU $(child_cpu) s of $CAP_S"
