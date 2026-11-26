#!/bin/bash
# Frozen review package for the N = 3 cover (RV21_43): copies (no links) of the O(3) certifier code (o3cert2.py = v2.1,
# which produced the ledgers V1-V4; its base o3cert.py and certint4/5.py for the diffs), its library inputs, the
# validation scripts and logs, the ledgers, run logs, the union check, the v2 tail comparison, the old-code cross-check
# runs T/U, and the notes, plus MANIFEST.txt (sha256 of every file, run commands, versions).
# usage: mkpkg_o3.sh PKGNAME
cd /mnt/g2/release/root/data/e17/unif/scratch || exit 1
P=$1
case "$P" in pkg_*) ;; *) echo "package name must start with pkg_"; exit 1 ;; esac
[ -e "$P" ] && { echo "$P exists; refusing to overwrite"; exit 1; }
mkdir "$P" "$P/code5" "$P/code4" "$P/out" "$P/out/crosscheck_old_code" || exit 1
for f in o3cert2.py o3cert.py o3lib3.py o3struct.py o3sparse.py o3brute.py o3check.py o3check2.py o3check3.py chain_o3v2.sh chain_o3.sh val_o3.sh test_o3c.sh mkpkg_o3.sh; do
    cp code5/$f "$P/code5/$f" || exit 1
done
for f in tm.py tm2.py checkcover.py sumledger.awk versions.py cmp_tails.py certint4.py certint5.py; do
    cp code4/$f "$P/code4/$f" || exit 1
done
LEDG=$(ls out/o3cover2_V*.ledger)
cp $LEDG out/o3cover2_V*_*.log out/chain_o3v2_V.log out/val_o3.log out/o3check3.log out/test_o3c.log out/o3cert_o3t*.txt out/cmp_tails.txt out/smoke_v21.log out/smoke_v21a.stdout out/smoke_o3v21a.stdout "$P/out/" || exit 1
cp out/o3cover_T1.ledger out/o3cover_T2.ledger out/o3cover_T3.ledger out/o3cover_U1.ledger out/chain_o3_T.log out/chain_o3_U.log "$P/out/crosscheck_old_code/" || exit 1
cp ../UNIF_NOTES.md "$P/UNIF_NOTES.md" || exit 1
env TMPDIR=/mnt/g2/release/root/data/e17/unif/scratch/tmp OMP_NUM_THREADS=1 timeout 120 nice -n 10 prlimit --as=8589934592 -- \
    python3 -I -B code4/checkcover.py 1/100 3 $LEDG > "$P/out/checkcover_output.txt" 2>&1 || exit 1
for f in $LEDG; do awk -f code4/sumledger.awk "$f"; done > "$P/out/ledger_summaries.txt" || exit 1
find "$P" -type l | awk 'END {if (NR > 0) {print "symlinks present"; exit 1}}' || exit 1
{
    echo "# RV21_43 N = 3 package $P (UNIF 9.20, 9.21), built $(date -u +%FT%TZ)"
    echo "# run: bash code5/chain_o3v2.sh V \"10 3 0.0099 0.62 0.01 0.04 3\" \"12 4 0.6 1.66 0.03 0.06 3\" \"14 6 1.65 2.66 0.015 0.035 4\" \"16 6 2.65 3.0 0.005 0.01 4\""
    echo "#      (from the scratch directory, with code5/ and code4/ as here; the O(3) tables are rebuilt in every job, no cache)"
    echo "# validation: bash code5/val_o3.sh -> out/val_o3.log; code5/o3check3.py 10 3000 1 and 14 400 2 -> out/o3check3.log; code5/test_o3c.sh -> out/test_o3c.log"
    echo "# v2 tails (MINOR-2 for N = 4): code4/cmp_tails.py o4 out/cover4_S*.ledger -> out/cmp_tails.txt"
    echo "# check: python3 code4/checkcover.py 1/100 3 out/o3cover2_V*.ledger  -> out/checkcover_output.txt"
    echo "# out/crosscheck_old_code: the same cover with o3cert.py (before v2.1): chain T stopped in segment 3 at J = 2.7057, chain U (L = 16) stopped at J = 2.758; see the chain logs"
    echo "# $(env OMP_NUM_THREADS=1 timeout 60 nice -n 10 prlimit --as=8589934592 -- python3 -I -B code4/versions.py 2>&1)"
    echo "# sha256 of every file:"
    (cd "$P" && find . -type f ! -name MANIFEST.txt | sort | while read -r f; do sha256sum "$f"; done)
} > "$P/MANIFEST.txt" || exit 1
sha256sum "$P/MANIFEST.txt"
