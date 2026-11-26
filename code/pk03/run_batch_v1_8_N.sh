#!/bin/bash
# run_batch_v1_8_N.sh -- pk03 (code/pk03/). One certified batch of S8_ENTRY_LIST_v3's 219 entries on m3_run_v1_8 for one N:
# pycheck, then D.N, E2.N, FF.N (prep and entries), E3u.N, E3c.N and the E3 pieces E3k1.N.., Nu.N, Nc.N and the N pieces Nk1.N.. (a piece
# may stop inside an entry and the next resume it), and asm.N, one item at a time. Rules as run_batch_v1_7_N.sh (6a7bd160):
# - CPU so far = this shell's reaped children (cutime + cstime of its own /proc stat). Each item runs with LIM = min(540, CAP_S - used - 5)
#   (RLIMIT_CPU in the script, hard limit LIM + 5), so the batch cannot pass CAP_S; if that LIM is below the item's minimum the chain
#   stops for re-pricing.
# - Before each item its .out and .err must not exist. After it, its VERDICT lines must be exactly ['VERDICT VALID'], else the chain
#   stops (a capped piece too: its rerun is a decision). Items with an estimate stop the chain when their CPU passes
#   max(2 x estimate, estimate + 30 s). Estimates: m3ref_v1_10's float times x 3.5 for entries, S7's certified preps.
# - The pieces of a family run until its C-PIECE line reports next == total. After a VALID asm.N, MANIFEST_m3_run_v1_8_asm.N.sha256
#   is written from sha256sum of the asm output and the five records its RECORD lines name.
# Usage: bash run_batch_v1_8_N.sh N CAP_S   (log: out/chain_v1_8_nN.log)
D=/mnt/g2/release/root/code/pk03
RUN=$D/m3_run_v1_8.py
N=$1
CAP_S=$2
case "$N" in 3|4) ;; *) echo "usage: bash run_batch_v1_8_N.sh N CAP_S (N = 3 or 4)"; exit 2;; esac
case "$CAP_S" in ''|*[!0-9]*) echo "usage: bash run_batch_v1_8_N.sh N CAP_S"; exit 2;; esac
LOG=$D/out/chain_v1_8_n$N.log
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
        D.*) echo 60;; E2.*) echo 20;; FF.*) echo 15;; E3u.*|Nu.*) echo 320;; E3c.*|Nc.*) echo 200;; asm.*) echo 120;; *) echo 0;;
    esac
}
minlim() {
    case "$1" in
        D.*) echo 140;; E2.*|FF.*) echo 60;; E3u.*|Nu.*) echo 400;; E3c.*|Nc.*) echo 260;; E3k*|Nk*) echo 200;; asm.*) echo 200;; *) echo 540;;
    esac
}

run_item() {
    local item=$1 o=$D/out/m3_run_v1_8_$1.out e=$D/out/m3_run_v1_8_$1.err u0 u1 dt es lim2 lim
    if [ -e "$o" ] || [ -e "$e" ]; then say "STOP $item: $o or its .err exists"; exit 1; fi
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

run_pieces() {
    local pfx=$1 maxp=$2 k=1 nt
    while :; do
        [ $k -le $maxp ] || { say "STOP: pieces ${pfx}k1..${pfx}k$maxp of N = $N did not cover the family"; exit 1; }
        run_item ${pfx}k$k.$N
        nt=$(awk 'index($0, "C-PIECE (") == 1 && match($0, /of [0-9]+ done, next [0-9]+/) { s = substr($0, RSTART, RLENGTH); split(s, a, /[^0-9]+/); print a[3], a[2] }' $D/out/m3_run_v1_8_${pfx}k$k.$N.out)
        say "PIECE ${pfx}k$k.$N next/total: $nt"
        set -- $nt
        [ -n "$1" ] && [ -n "$2" ] || { say "STOP: no C-PIECE line in ${pfx}k$k.$N"; exit 1; }
        [ "$1" -lt "$2" ] || break
        k=$((k + 1))
    done
}

say "CHAIN start N $N: m3_run_v1_8.py $(sha256sum $RUN | cut -c1-8); $(basename $0) $(sha256sum $0 | cut -c1-8); cap $CAP_S s"
PO=$D/out/m3_pycheck_v1_run_v1_8_n$N.out
PE=$D/out/m3_pycheck_v1_run_v1_8_n$N.err
if [ -e "$PO" ] || [ -e "$PE" ]; then say "STOP pycheck: its output exists"; exit 1; fi
OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --cpu=120:125 -- python3 -I -B $D/m3_pycheck_v1.py \
    $RUN $D/m3_reader_v4_4.py $D/m3_record_v4.py $D/m3_bar_v10.py $D/m3_scal_v2.py $D/m3_graph_v3.py $D/m3_series_v2.py \
    $D/m3_major_v2.py $D/m3_entries_v3.py $D/m3_handoff_v3.py > "$PO" 2> "$PE"
say "END pycheck rc $? $(verdict_of "$PO"); out sha256 $(sha256sum "$PO" | cut -c1-8)"
verdict_valid "$PO" || { say "STOP after pycheck"; exit 1; }

for f in D E2 FF E3u E3c; do run_item $f.$N; done
run_pieces E3 9
for f in Nu Nc; do run_item $f.$N; done
run_pieces N 19
run_item asm.$N
A=out/m3_run_v1_8_asm.$N.out
RECS=$(awk 'index($0, "RECORD ") == 1 && NF == 3 { print "out/" $2 }' $D/$A)
[ $(echo "$RECS" | awk 'NF' | wc -l) -eq 5 ] || { say "STOP: asm.$N does not name five records"; exit 1; }
M=$D/MANIFEST_m3_run_v1_8_asm.$N.sha256
(cd $D && sha256sum $A $RECS > $M) && chmod 444 $M || { say "STOP: side manifest for asm.$N not written"; exit 1; }
(cd $D && sha256sum -c --quiet $M) || { say "STOP: side manifest check failed for asm.$N"; exit 1; }
say "SIDE-MANIFEST $(basename $M) $(sha256sum $M | cut -c1-8) ($(wc -l < $M) lines)"
say "CHAIN end N $N: CPU $(child_cpu) s of $CAP_S"
