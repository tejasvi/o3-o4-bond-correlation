#!/bin/bash
# Frozen review package for RV21_37: copies (no links) of the certifier code, its library inputs, the ledgers, the run
# logs, the union-check output and the notes, plus MANIFEST.txt (sha256 of every file, run commands, versions).
# usage: mkpkg.sh PKGNAME LEDGERPREFIX      (e.g. mkpkg.sh pkg_v2 S)
cd /mnt/g2/release/root/data/e17/unif/scratch || exit 1
P=$1; X=$2
case "$P" in pkg_*) ;; *) echo "package name must start with pkg_"; exit 1 ;; esac
[ -e "$P" ] && { echo "$P exists; refusing to overwrite"; exit 1; }
mkdir "$P" "$P/code" "$P/out" || exit 1
for f in certint4.py certlib3.py certlib2.py certlib.py tm2.py tm.py checkcover.py chain23.sh sumledger.awk test_tm2.py test_bd.py certgrid.py cert2.py scope40.py versions.py mkpkg.sh; do
    cp code4/$f "$P/code/$f" || exit 1
done
cp /mnt/g2/release/root/data/e15/dy4/scratch/code/su2lib.py "$P/code/su2lib.py" || exit 1
cp out/cover4_${X}*.ledger out/certint4_${X}*.txt out/chain23_${X}.log "$P/out/" || exit 1
cp ../UNIF_NOTES.md "$P/UNIF_NOTES.md" || exit 1
env TMPDIR=/mnt/g2/release/root/data/e17/unif/scratch/tmp OMP_NUM_THREADS=1 timeout 120 nice -n 10 prlimit --as=8589934592 -- \
    python3 -I -B code4/checkcover.py 1/100 3 $(ls out/cover4_${X}*.ledger) > "$P/out/checkcover_output.txt" 2>&1 || exit 1
for f in "$P"/out/cover4_${X}*.ledger; do awk -f code4/sumledger.awk "$f"; done > "$P/out/ledger_summaries.txt" || exit 1
find "$P" -type l | awk 'END {if (NR > 0) {print "symlinks present"; exit 1}}' || exit 1
{
    echo "# RV21_37 package $P (UNIF 9.13-9.17), built $(date -u +%FT%TZ)"
    echo "# run: bash code/chain23.sh S \"10 3 0.0099 0.62 0.01 0.04 3\" \"12 4 0.6 1.72 0.03 0.06 3\" \"14 6 1.7 2.75 0.015 0.035 4\" \"16 6 2.7 3.0 0.005 0.01 4\""
    echo "#      (from the scratch directory; code4/ there = code/ here; the L<=14 quadruple tables are rebuilt into tmp/ if absent)"
    echo "# check: python3 code/checkcover.py 1/100 3 out/cover4_S*.ledger  -> out/checkcover_output.txt"
    echo "# $(env OMP_NUM_THREADS=1 timeout 60 nice -n 10 prlimit --as=8589934592 -- python3 -I -B code4/versions.py 2>&1)"
    echo "# sha256 of every file:"
    (cd "$P" && find . -type f ! -name MANIFEST.txt | sort | while read -r f; do sha256sum "$f"; done)
} > "$P/MANIFEST.txt" || exit 1
sha256sum "$P/MANIFEST.txt"
