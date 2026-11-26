#!/bin/bash
# w2m_chain_v1.sh (run-time tool of the spot regeneration, shipped as a record): the N chain of m3_run_r0m_v1_2.py, run in the package
# overlay from code/pk03, by the item rules of the archived run_chain_m3_run_r0m_v1_2.sh in MODE all (that script and its MANIFEST are
# not shipped): VDu, VDc; the entry pieces W2Mk1, W2Mk2, ... with LIM 540, where a clean CAP-STOP of a piece makes the next piece a long
# piece with LIM 1500 and a long piece that ends in a clean CAP-STOP stops the chain, until a C-PIECE line reads 'next X of X;'; W2Mr1,
# W2Mr2; asm. Each item runs with one thread, timeout LIM + 40 s and address space AS bytes; its output out/m3_run_r0m_v1_2_<ITEM>.out
# and .err are never overwritten (set -C); the chain stops at the first item that is neither VERDICT VALID nor a clean CAP-STOP of an
# entry piece. Left out from the archived script: its CPU cap arithmetic (CAP_S; the core-hour guard bounds the run), its MANIFEST check
# and its pycheck. Log: out/w2m_chain_N<N>.log (a run-time file). usage: bash w2m_chain_v1.sh N AS_BYTES
set -u
N=$1; AS=$2
[[ "$N" =~ ^(4|3)$ && "$AS" =~ ^[0-9]{10,12}$ ]] || { echo "usage: w2m_chain_v1.sh 4|3 AS_BYTES"; exit 2; }
PYB=python3
NICE="nice -n 10"
LOG=out/w2m_chain_N$N.log
CAPPED='VERDICT INCOMPLETE (CAP-STOP)'
set -C
stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
say() { echo "$(stamp) $*" >> $LOG; }
verdict_is() { awk -v w="$2" 'index($0, "VERDICT") == 1 { n++; v = $0 } END { exit !(n == 1 && v == w) }' "$1"; }
clean_cap() { verdict_is "$1" "$CAPPED" && awk 'index($0, "CAP-STOP SIGXCPU") == 1 { n++ } END { exit !(n == 1) }' "$1"; }
run_item() {
    local item=$1 lim=$2 o=out/m3_run_r0m_v1_2_$1.out e=out/m3_run_r0m_v1_2_$1.err rc
    say "START $item LIM $lim"
    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 timeout $((lim + 40)) $NICE prlimit --as=$AS -- $PYB -I -B m3_run_r0m_v1_2.py \
        $item $lim > "$o" 2> "$e"
    rc=$?
    say "END $item rc $rc $(awk 'index($0, "VERDICT") == 1' "$o" | tr '\n' ' ')out $(sha256sum "$o" | cut -c1-8) err $(wc -c < "$e") bytes"
    verdict_is "$o" "VERDICT VALID" && return 0
    if [[ "$item" =~ ^W2Mk ]] && clean_cap "$o"; then return 3; fi
    say "STOP after $item: neither VERDICT VALID nor a clean CAP-STOP of an entry piece"
    exit 1
}
say "CHAIN m3_run_r0m_v1_2 $(sha256sum m3_run_r0m_v1_2.py | cut -c1-8); w2m_chain_v1.sh; N $N; address space $AS"
run_item VDu.$N 540
run_item VDc.$N 540
q=1; long=0
while :; do
    [ $q -le 40 ] || { say "STOP: the W2M entries did not finish by piece 40"; exit 1; }
    lim=540; [ $long = 1 ] && lim=1500
    run_item W2Mk$q.$N $lim; rc=$?
    o=out/m3_run_r0m_v1_2_W2Mk$q.$N.out
    if [ $rc = 3 ]; then
        [ $long = 1 ] && { say "STOP after W2Mk$q.$N: a long piece ended in a clean CAP-STOP"; exit 5; }
        long=1
        say "LONG-NEXT after W2Mk$q.$N"
    else
        long=0
        if awk 'index($0, "C-PIECE ") == 1 && match($0, /next [0-9]+ of [0-9]+;/) { split(substr($0, RSTART + 5, RLENGTH - 6), a, " of "); if (a[1] == a[2]) g = 1 } END { exit !g }' "$o"; then
            say "ENTRIES DONE in piece $q"
            break
        fi
    fi
    q=$((q + 1))
done
run_item W2Mr1.$N 540
run_item W2Mr2.$N 540
run_item asm.$N 540
say "CHAIN end"
