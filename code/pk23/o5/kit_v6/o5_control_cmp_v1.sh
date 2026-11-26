#!/bin/bash
# o5_control_cmp_v1.sh (pk23 O5 box kit v4): the control gate's comparison. It compares the box's n = 4 control output with pk06's
# certified run pk06/runs/full_n4_G02_s14_v1.out (a copy ships in the kit, sha256 checked by the kit manifest) after masking only timing,
# memory, run-cap and identity fields: cpu/wall seconds (also "CPU <orbit>: N s"), RSS and predicted-peak megabytes, the LIM and MEMSTOP
# arguments, the script's sha256 and name, and the python and python-flint versions. Every other byte must agree. Prints the count of
# differing lines; exit 0 only if it is 0. Usage: o5_control_cmp_v1.sh BOX_OUTPUT REFERENCE
mask() {
  awk '{
    gsub(/cpu so far [0-9.]+ s/, "cpu so far X s"); gsub(/cpu [0-9.]+ s/, "cpu X s"); gsub(/wall [0-9.]+ s/, "wall X s")
    gsub(/: [0-9.]+ s; peak RSS/, ": X s; peak RSS"); gsub(/peak RSS [0-9]+ MB/, "peak RSS X MB"); gsub(/predicted peak [0-9]+ MB/, "predicted peak X MB")
    gsub(/peak [0-9]+ MB/, "peak X MB"); gsub(/LIM [0-9]+/, "LIM X"); gsub(/MEMSTOP [0-9]+ MB/, "MEMSTOP X MB")
    gsub(/sha256 [0-9a-f]+/, "sha256 X"); gsub(/python [0-9.]+/, "python X"); gsub(/python-flint [0-9.]+/, "python-flint X")
    gsub(/^kt_lbu_g3[0-9]_[a-z0-9_]+ /, "ENGINE ")
    print }' "$1"
}
n=$(diff <(mask "$1") <(mask "$2") | awk '/^[<>]/' | wc -l)
echo "control compare: $n differing lines after masking (box $(basename "$1"), reference $(basename "$2"))"
[ "$n" -eq 0 ]
