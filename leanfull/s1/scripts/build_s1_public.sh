#!/bin/bash
# build_s1.sh MODLIST : compile the modules listed in MODLIST (one module path per line, e.g. G2S1/Alg), in order,
# one lean call per module (the method of s0/scripts/build_tree.sh). Lake is not run.
#   SRC = s1/src ; OUT = s1/build/S1 ; LEAN_PATH = Mathlib deps : s0/build/Lb (package G2Kernel, read-only) : s1/build/S1
# Stops at the first failing module. Prints one line per module and BUILD DONE / BUILD FAIL at the end.
S="${S1_DIR:?set S1_DIR to the leanfull/s1 folder}"
S0="${S0_DIR:?set S0_DIR to a leanfull/s0 folder whose build/Lb holds the build of the package tree G2Kernel_Lb_p13}"
P="${MATHLIB_PACKAGES:?set MATHLIB_PACKAGES to the .lake/packages folder of a Mathlib checkout at the commit of the Lean pin}"
LEAN="${LEAN:?set LEAN to the lean binary of the toolchain leanprover/lean4:v4.35.0-rc3}"
export TMPDIR=$S/tmp
DEPS=$P/mathlib/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean
SRC=$S/src
OUT=$S/build/S1e
export LEAN_PATH=$DEPS:$S0/build/Lb:$OUT
list="$1"
if [ -z "$list" ] || [ ! -f "$list" ]; then echo "BUILD FAIL no module list"; exit 2; fi
echo "lean build start $(date -u +%Y-%m-%dT%H:%M:%SZ) list=$list"
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
