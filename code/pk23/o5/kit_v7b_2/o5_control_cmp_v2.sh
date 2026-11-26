#!/bin/bash
# o5_control_cmp_v2.sh (pk23 O5 box kit v7; = kit v4-v6's o5_control_cmp_v1.sh 68e8a827 with the sha256 mask on the first line only, so that
# a CELLS line's digest of its CELL lines (g37fs with NCELL > 64) is compared too; the first line's sha256 is the engine's identity): the
# control comparison of kit v7. It compares a box output with a reference output after masking only timing,
# memory, run-cap and identity fields: cpu/wall seconds (also "CPU <orbit>: N s"), RSS and predicted-peak megabytes, the LIM and MEMSTOP
# arguments, the script's sha256 and name, and the python and python-flint versions. Every other byte must agree. Prints the count of
# differing lines; exit 0 only if it is 0. Usage: o5_control_cmp_v1.sh BOX_OUTPUT REFERENCE
mask() {
  awk '{
    gsub(/cpu so far [0-9.]+ s/, "cpu so far X s"); gsub(/cpu [0-9.]+ s/, "cpu X s"); gsub(/wall [0-9.]+ s/, "wall X s")
    gsub(/: [0-9.]+ s; peak RSS/, ": X s; peak RSS"); gsub(/peak RSS [0-9]+ MB/, "peak RSS X MB"); gsub(/predicted peak [0-9]+ MB/, "predicted peak X MB")
    gsub(/peak [0-9]+ MB/, "peak X MB"); gsub(/LIM [0-9]+/, "LIM X"); gsub(/MEMSTOP [0-9]+ MB/, "MEMSTOP X MB")
    if (FNR == 1) gsub(/sha256 [0-9a-f]+/, "sha256 X"); gsub(/python [0-9.]+/, "python X"); gsub(/python-flint [0-9.]+/, "python-flint X")
    gsub(/^kt_lbu_g3[0-9]_[a-z0-9_]+ /, "ENGINE ")
    print }' "$1"
}
n=$(diff <(mask "$1") <(mask "$2") | awk '/^[<>]/' | wc -l)
echo "control compare: $n differing lines after masking (box $(basename "$1"), reference $(basename "$2"))"
[ "$n" -eq 0 ]
