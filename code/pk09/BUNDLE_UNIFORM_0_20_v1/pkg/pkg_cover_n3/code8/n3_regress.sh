#!/bin/bash
# Wave 18: regression of the path-parameterised N = 3 code (o3cert6 --out/--cache, relative ../code5, ../code_dep, ../tmp)
# against the cover run: re-certify three ledger intervals into a fresh output directory with a fresh 6j cache, and
# compare each interval block with the cover's certificate (timings, J0 text and the file header masked).
#   usage: n3_regress.sh OUTDIR "J0:h:L:coverfile" ...
S=/mnt/g2/release/root/data/e17/unif/scratch
W="env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=$S/tmp timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B"
D=$1; shift
cd $S || exit 1
case "$D" in $S/tmp/n3_regress*) ;; *) echo "OUTDIR must be under $S/tmp/n3_regress"; exit 2 ;; esac
mkdir -p "$D" || exit 3
block() {   # the lines of the interval [lo, hi] (from its lam5 line to its verdict), masked
    awk -v key="$2" '/lam5 over I/ { buf = ""; on = 1 } on { buf = buf $0 "\n" } /==> interval/ && on { if (index(buf, key) > 0) { printf "%s", buf; exit } on = 0 }' "$1" |
    awk '{ gsub(/\(J0=[^,]*, /, "(J0=*, "); gsub(/eigen [0-9.]+s, operators [0-9.]+s, frame [0-9.]+s/, "T"); gsub(/\([0-9.]+s[:)].*$/, "(T)"); gsub(/used frob \([0-9.]+s\)/, "used frob (T)"); print }'
}
k=0; bad=0
for spec in "$@"; do
    k=$((k + 1))
    J0=${spec%%:*}; r=${spec#*:}; h=${r%%:*}; r=${r#*:}; L=${r%%:*}; F=${r#*:}
    $W code8/o3cert6.py --out "$D" --cache "$D/sixj_signed_cache.npz" rg$k "$L" 6 "$J0:$h" vec frob > "$D/rg$k.log" 2>&1
    echo "rg$k rc=$?"
    key=$(awk -v j="$J0" -v hh="$h" 'BEGIN { printf "J in [%.6f, %.6f]", j - hh, j + hh }')
    if diff <(block "out/$F" "$key") <(block "$D/o3cert6_rg$k.txt" "$key") > "$D/rg$k.diff"; then
        echo "rg$k ($key, L=$L): identical to out/$F ($(block "out/$F" "$key" | awk 'END { print NR }') lines)"
    else
        echo "rg$k ($key, L=$L): DIFFERS from out/$F (see $D/rg$k.diff)"; bad=$((bad + 1))
    fi
done
echo "regression: $bad of $k intervals differ"
