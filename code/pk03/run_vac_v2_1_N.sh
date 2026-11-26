#!/bin/bash
# run_vac_v2_1_N.sh -- pk03 (code/pk03/). The certified vacuum records of M2(b) on m3_vac_v2_1 for one N: pycheck, then vD.N, OFD.N,
# OF3.N, OF4.N, vGu0.N, vGc0.N, vGk0.N, vGu1.N, vGc1.N, vGk1.N, vGu2.N, vGc2.N, vGk2.N and asm.N, one item at a time (cheap items first).
# Rules as run_batch_v1_7_N.sh (6a7bd160):
# - CPU so far = this shell's reaped children (cutime + cstime of its own /proc stat). Each item runs with LIM = min(540, CAP_S - used - 5)
#   (RLIMIT_CPU in the script, hard limit LIM + 5), so the batch cannot pass CAP_S; if that LIM is below the item's minimum the chain
#   stops for re-pricing.
# - Before each item its .out, its .err and its hand-off must not exist. After it, its VERDICT lines must be exactly ['VERDICT VALID'],
#   else the chain stops. An item whose CPU passes max(2 x estimate, estimate + 30 s) stops the chain for re-pricing.
# - After a VALID asm.N, MANIFEST_m3_vac_v2_1_asm.N.sha256 is written from sha256sum of the asm output and the record its RECORD line names.
# Usage: bash run_vac_v2_1_N.sh N CAP_S   (log: out/chain_vac_v2_1_nN.log)
# REVISION of run_vac_v2_N.sh (0389e277): the m3_vac_v2_1 names; the OF3 and OF4 estimates are 60 s and 120 s (E3 and E4
# have V = 9 and 12). Everything else is the v2 chain.
D=/mnt/g2/release/root/code/pk03
RUN=$D/m3_vac_v2_1.py
N=$1
CAP_S=$2
case "$N" in 3|4) ;; *) echo "usage: bash run_vac_v2_1_N.sh N CAP_S (N = 3 or 4)"; exit 2;; esac
case "$CAP_S" in ''|*[!0-9]*) echo "usage: bash run_vac_v2_1_N.sh N CAP_S"; exit 2;; esac
LOG=$D/out/chain_vac_v2_1_n$N.log
set -o noclobber
HZ=$(getconf CLK_TCK)

stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
say() { echo "$(stamp) $*" >> $LOG; echo "$(stamp) $*"; }
child_cpu() { awk -v hz=$HZ '{ printf "%.1f\n", ($16 + $17) / hz }' /proc/$$/stat; }
verdict_valid() { awk 'index($0, "VERDICT") == 1 { n++; v = $0 } END { exit !(n == 1 && v == "VERDICT VALID") }' "$1"; }
verdict_of() { awk 'index($0, "VERDICT") == 1 { print; n++ } END { if (!n) print "(no VERDICT line)" }' "$1" | tr '\n' ' '; }
over() { awk -v a="$1" -v b="$2" 'BEGIN { exit !(a > b) }'; }

est() {
    case "$1" in
        vD.*) echo 20;; OFD.*) echo 20;; OF3.*) echo 60;; OF4.*) echo 120;; vGu*) echo 120;; vGc*) echo 90;; vGk*) echo 60;; asm.*) echo 30;;
        *) echo 0;;
    esac
}
minlim() {
    case "$1" in
        vD.*) echo 60;; OFD.*) echo 60;; OF3.*) echo 120;; OF4.*) echo 240;; vGu*) echo 240;; vGc*) echo 180;; vGk*) echo 120;;
        asm.*) echo 90;; *) echo 540;;
    esac
}

run_item() {
    local item=$1 o=$D/out/m3_vac_v2_1_$1.out e=$D/out/m3_vac_v2_1_$1.err h=$D/hand/m3_vac_v2_1_$1.json u0 u1 dt es lim2 lim
    if [ -e "$o" ] || [ -e "$e" ] || [ -e "$h" ]; then say "STOP $item: $o, its .err or its hand-off exists"; exit 1; fi
    u0=$(child_cpu)
    lim=$(awk -v c="$CAP_S" -v u="$u0" 'BEGIN { l = int(c - u - 5); if (l > 540) l = 540; print l }')
    if [ "$lim" -lt "$(minlim $item)" ]; then say "STOP before $item: CPU so far $u0 s leaves LIM $lim s under the cap $CAP_S s, below its minimum $(minlim $item) s; re-price"; exit 1; fi
    say "START $item LIM $lim (CPU so far $u0 s of $CAP_S)"
    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=$D/tmp timeout 580 nice -n 10 prlimit --as=8589934592 -- \
        python3 -I -B $RUN $item $lim > "$o" 2> "$e"
    local rc=$?
    u1=$(child_cpu)
    dt=$(awk -v a="$u0" -v b="$u1" 'BEGIN { printf "%.1f", b - a }')
    say "END $item rc $rc CPU $dt s (total $u1 s); $(verdict_of "$o"); out sha256 $(sha256sum "$o" | cut -c1-8); err $(wc -c < "$e") bytes"
    if ! verdict_valid "$o"; then say "STOP after $item: VERDICT lines are not exactly [VERDICT VALID]"; exit 1; fi
    es=$(est "$item")
    if [ "$es" != 0 ]; then
        lim2=$(awk -v s="$es" 'BEGIN { m = 2 * s; if (s + 30 > m) m = s + 30; print m }')
        if over "$dt" "$lim2"; then say "STOP after $item: CPU $dt s passes $lim2 s (2 x estimate $es s); re-price"; exit 1; fi
    fi
}

say "CHAIN start N $N: m3_vac_v2_1.py $(sha256sum $RUN | cut -c1-8); $(basename $0) $(sha256sum $0 | cut -c1-8); cap $CAP_S s"
PO=$D/out/m3_pycheck_v1_vac_v2_1_n$N.out
PE=$D/out/m3_pycheck_v1_vac_v2_1_n$N.err
if [ -e "$PO" ] || [ -e "$PE" ]; then say "STOP pycheck: its output exists"; exit 1; fi
OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --cpu=120:125 -- python3 -I -B $D/m3_pycheck_v1.py \
    $RUN $D/m3_scal_v2.py $D/m3_graph_v3.py $D/m3_series_v2.py $D/m3_major_v2.py $D/m3_bar_v10.py $D/m3_entries_v3.py \
    $D/m3_record_v5.py $D/m3_reader_v5.py $D/m3_handoff_v3.py > "$PO" 2> "$PE"
say "END pycheck rc $? $(verdict_of "$PO"); out sha256 $(sha256sum "$PO" | cut -c1-8)"
verdict_valid "$PO" || { say "STOP after pycheck"; exit 1; }

for f in vD OFD OF3 OF4 vGu0 vGc0 vGk0 vGu1 vGc1 vGk1 vGu2 vGc2 vGk2 asm; do run_item $f.$N; done
A=out/m3_vac_v2_1_asm.$N.out
RECS=$(awk 'index($0, "RECORD ") == 1 && NF == 3 { print "out/" $2 }' $D/$A)
[ "$(echo "$RECS" | awk 'NF' | wc -l)" -eq 1 ] || { say "STOP: asm.$N does not name exactly one record"; exit 1; }
M=$D/MANIFEST_m3_vac_v2_1_asm.$N.sha256
(cd $D && sha256sum $A $RECS > $M) && chmod 444 $M || { say "STOP: side manifest for asm.$N not written"; exit 1; }
(cd $D && sha256sum -c --quiet $M) || { say "STOP: side manifest check failed for asm.$N"; exit 1; }
say "SIDE-MANIFEST $(basename $M) $(sha256sum $M | cut -c1-8) ($(wc -l < $M) lines)"
say "CHAIN end N $N: CPU $(child_cpu) s of $CAP_S"
