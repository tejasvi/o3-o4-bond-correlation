#!/bin/bash
# Wave 18: freeze the N = 3 [3, 20] cover (o3cert6, vec truncation, frob lambda_5) for review: code (certint6 and its
# modules, code4 dependencies, cover chain and checker), the ledger, status and job times, every job output and log,
# the union check, and a MANIFEST of sha256 sums.  usage: mkpkg_cover3.sh PKGDIR_NAME
S=/mnt/g2/release/root/data/e17/unif/scratch
P=$S/$1
case "$1" in pkg_cover_*) ;; *) echo "package name must start with pkg_cover_"; exit 2 ;; esac
if [ -e "$P" ]; then echo "exists: $P"; exit 3; fi
cd $S || exit 1
mkdir "$P" && mkdir "$P/code8" "$P/code4" "$P/code5" "$P/code_dep" "$P/out" "$P/log" || exit 4
cp code8/o3cert6.py code8/mfops.py code8/o3mfstruct.py code8/mfstruct.py code8/mfstruct2.py code8/lam5frob.py code8/cover_chain3.sh code8/cover_check.awk code8/o3cert_vs_ledger.awk code8/mkpkg_cover3.sh "$P/code8/" || exit 5
cp code5/o3struct.py code5/o3lib3.py "$P/code5/" || exit 54
cp code8/n3_regress.sh "$P/code8/" || exit 55
mkdir "$P/code_ran" && cp -r tmp/n3_code_ran/code8 tmp/n3_code_ran/code4 tmp/n3_code_ran/code5 "$P/code_ran/" || exit 56
( cd "$P" && for f in o3cert6 mfops o3mfstruct mfstruct2 mfstruct lam5frob; do diff -u "code_ran/code8/$f.py" "code8/$f.py"; done > code_diff.txt )
mkdir "$P/out/n3_regress" && cp tmp/n3_regress/rg*.log tmp/n3_regress/rg*.diff tmp/n3_regress/o3cert6_rg*.txt tmp/n3_regress/regress_summary.txt "$P/out/n3_regress/" || exit 57
cp /mnt/g2/release/root/data/e15/dy4/scratch/code/su2lib.py "$P/code_dep/" || exit 51
cp tmp/README_cover_n3.md "$P/README.md" || exit 52
cp tmp/cover_n3_table.txt "$P/out/cover_table.txt" || exit 53
cp code4/certlib3.py code4/tm2.py "$P/code4/" || exit 6
cp out/o3cover6_n3.ledger out/o3cover6_n3.status out/o3cover6_n3.times "$P/out/" || exit 7
for f in $(ls out/ | awk '/^o3cert6_n3_[0-9]+\.txt$/'); do cp "out/$f" "$P/out/" || exit 8; done
for f in $(ls tmp/ | awk '/^n3_[0-9]+\.log$/'); do cp "tmp/$f" "$P/log/" || exit 9; done
awk -v JA=3 -v JB=20 -f code8/cover_check.awk out/o3cover6_n3.ledger > "$P/out/cover_check.txt"
awk -f code8/o3cert_vs_ledger.awk out/o3cover6_n3.ledger out/o3cert6_n3_*.txt > "$P/out/cert_vs_ledger.txt"
cp ../UNIF_NOTES.md "$P/UNIF_NOTES_frozen.md" || exit 10
cd "$P" && sha256sum README.md UNIF_NOTES_frozen.md code_diff.txt code8/* code4/* code5/* code_dep/* code_ran/code8/* code_ran/code4/* code_ran/code5/* out/*.* out/n3_regress/* log/* > MANIFEST
echo "MANIFEST $(sha256sum MANIFEST | cut -c1-8), $(awk 'END { print NR }' MANIFEST) files; $(tail -n 1 out/cover_check.txt)"
