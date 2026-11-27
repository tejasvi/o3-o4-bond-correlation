#!/bin/bash
# build_s3_public.sh MODLIST
# Compile the modules listed in MODLIST (one module path per line, e.g. G2S3/RPCore), in order, one lean call per
# module (the method of leanfull/s0/scripts/build_tree_public.sh). Lake is not run. Dependencies: the Mathlib packages
# and the three build trees of a leanfull/s0 folder (build/Lb = G2Kernel, build/S3 = StripIII, build/S0 = G2S0).
# Output: build/G of this folder. Stops at the first failing module. Prints MOD lines and BUILD DONE / BUILD FAIL.
D="${S3_DIR:?set S3_DIR to the leanfull/s3 folder}"
S0="${S0_DIR:?set S0_DIR to a leanfull/s0 folder whose build/Lb, build/S3 and build/S0 hold the builds of its three trees}"
P="${MATHLIB_PACKAGES:?set MATHLIB_PACKAGES to the .lake/packages folder of a Mathlib checkout at the commit of the Lean pin}"
LEAN="${LEAN:?set LEAN to the lean binary of the toolchain leanprover/lean4:v4.35.0-rc3}"
export TMPDIR=$D/tmp
DEPS=$P/mathlib/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean
SRC=$D/src
OUT=$D/build/G
list="$1"
if [ -z "$list" ] || [ ! -f "$list" ]; then echo "BUILD FAIL no module list"; exit 2; fi
case "$OUT" in
  $D/build/G) ;;
  *) echo "BUILD FAIL output dir"; exit 2 ;;
esac
export LEAN_PATH=$DEPS:$S0/build/Lb:$S0/build/S3:$S0/build/S0:$OUT
echo "lean build start $(date -u +%Y-%m-%dT%H:%M:%SZ) list=$list"
"$LEAN" --version
total0=$(date +%s)
while IFS= read -r m; do
  [ -z "$m" ] && continue
  case "$m" in \#*) continue ;; esac
  d=$(dirname "$OUT/$m")
  mkdir -p "$d"
  t0=$(date +%s)
  "$LEAN" -R "$SRC" -j 8 -s 262144 -o "$OUT/$m.olean" -i "$OUT/$m.ilean" "$SRC/$m.lean"
  rc=$?
  t1=$(date +%s)
  echo "MOD $m rc=$rc wall_s=$((t1 - t0)) total_wall_s=$((t1 - total0))"
  if [ "$rc" -ne 0 ]; then
    echo "BUILD FAIL $(date -u +%Y-%m-%dT%H:%M:%SZ) at $m"
    exit 1
  fi
done < "$list"
echo "BUILD DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) total_wall_s=$(( $(date +%s) - total0 ))"
exit 0
