#!/bin/bash
# build_tree.sh TREE MODLIST
# Compile the modules listed in MODLIST (one module path per line, e.g. G2Kernel/Defs), in order, one lean call
# per module: the release rebuild method of README_release_N.md section 3.2. Lake is not run, so nothing is
# written into the Mathlib checkout (which has no .lake/lakefile.olean that Lake could reuse).
#   TREE = Lb : pkg/G2Kernel_Lb_p13/src -> build/Lb
#   TREE = S3 : pkg/StripIII_v2/src     -> build/S3   (after Lb; options -s 262144 -DElab.async=false)
#   TREE = S0 : src (new S0 modules)    -> build/S0   (after Lb and S3)
# Stops at the first module that fails. Prints one line per module and BUILD DONE / BUILD FAIL at the end.
S="${S0_DIR:?set S0_DIR to the leanfull/s0 folder}"
P="${MATHLIB_PACKAGES:?set MATHLIB_PACKAGES to the .lake/packages folder of a Mathlib checkout at the commit of the Lean pin}"
LEAN="${LEAN:?set LEAN to the lean binary of the toolchain leanprover/lean4:v4.35.0-rc3}"
export TMPDIR=$S/tmp
DEPS=$P/mathlib/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean
tree="$1"
list="$2"
case "$tree" in
  Lb) SRC=$S/pkg/G2Kernel_Lb_p13/src; OUT=$S/build/Lb; LP=$DEPS:$S/build/Lb; EXTRA="" ;;
  S3) SRC=$S/pkg/StripIII_v2/src; OUT=$S/build/S3; LP=$DEPS:$S/build/Lb:$S/build/S3; EXTRA="-s 262144 -DElab.async=false" ;;
  S0) SRC=$S/src; OUT=$S/build/S0; LP=$DEPS:$S/build/Lb:$S/build/S3:$S/build/S0; EXTRA="-s 262144" ;;
  *) echo "BUILD FAIL bad tree '$tree'"; exit 2 ;;
esac
if [ -z "$list" ] || [ ! -f "$list" ]; then echo "BUILD FAIL no module list"; exit 2; fi
case "$OUT" in
  $S/build/*) ;;
  *) echo "BUILD FAIL output dir outside s0/build"; exit 2 ;;
esac
export LEAN_PATH=$LP
echo "lean build start $(date -u +%Y-%m-%dT%H:%M:%SZ) tree=$tree list=$list"
"$LEAN" --version
total0=$(date +%s)
while IFS= read -r m; do
  [ -z "$m" ] && continue
  case "$m" in \#*) continue ;; esac
  d=$(dirname "$OUT/$m")
  mkdir -p "$d"
  t0=$(date +%s)
  "$LEAN" -R "$SRC" -j 8 $EXTRA -o "$OUT/$m.olean" -i "$OUT/$m.ilean" "$SRC/$m.lean"
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
