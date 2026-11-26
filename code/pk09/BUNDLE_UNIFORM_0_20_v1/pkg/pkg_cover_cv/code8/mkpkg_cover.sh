#!/bin/bash
# Wave 18: freeze the N = 4 [3, 20] cover (certint6, vec truncation, frob lambda_5) for review: code (certint6 and its
# modules, code4 dependencies, cover chain and checker), the ledger, status and job times, every job output and log,
# the union check, and a MANIFEST of sha256 sums.  usage: mkpkg_cover.sh PKGDIR_NAME
S=/mnt/g2/release/root/data/e17/unif/scratch
P=$S/$1
case "$1" in pkg_cover_*) ;; *) echo "package name must start with pkg_cover_"; exit 2 ;; esac
if [ -e "$P" ]; then echo "exists: $P"; exit 3; fi
cd $S || exit 1
mkdir "$P" && mkdir "$P/code8" "$P/code4" "$P/code_dep" "$P/out" "$P/log" || exit 4
cp code8/certint6.py code8/mfops.py code8/mfstruct.py code8/mfstruct2.py code8/lam5frob.py code8/cover_chain.sh code8/cover_check.awk code8/cert_vs_ledger.awk code8/mkpkg_cover.sh "$P/code8/" || exit 5
cp /mnt/g2/release/root/data/e15/dy4/scratch/code/su2lib.py "$P/code_dep/" || exit 51
cp tmp/README_cover_cv.md "$P/README.md" || exit 52
cp tmp/cover_cv_table.txt "$P/out/cover_table.txt" || exit 53
cp code4/certlib3.py code4/tm2.py "$P/code4/" || exit 6
cp out/cover6_cv.ledger out/cover6_cv.status out/cover6_cv.times "$P/out/" || exit 7
for f in $(ls out/ | awk '/^certint6_cv_[0-9]+\.txt$/'); do cp "out/$f" "$P/out/" || exit 8; done
for f in $(ls tmp/ | awk '/^cv_[0-9]+\.log$/'); do cp "tmp/$f" "$P/log/" || exit 9; done
awk -v JA=3 -v JB=20 -f code8/cover_check.awk out/cover6_cv.ledger > "$P/out/cover_check.txt"
awk -f code8/cert_vs_ledger.awk out/cover6_cv.ledger out/certint6_cv_*.txt > "$P/out/cert_vs_ledger.txt"
cp ../UNIF_NOTES.md "$P/UNIF_NOTES_frozen.md" || exit 10
cd "$P" && sha256sum README.md UNIF_NOTES_frozen.md code8/* code4/* code_dep/* out/* log/* > MANIFEST
echo "MANIFEST $(sha256sum MANIFEST | cut -c1-8), $(awk 'END { print NR }' MANIFEST) files; $(tail -n 1 out/cover_check.txt)"
