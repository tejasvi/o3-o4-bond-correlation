#!/bin/bash
# run_m2b_asm_v1_v1.sh -- pk02 (code/pk02/). The real m2b_asm_v1 run (6acd83d3) as authorized after the OK:
# checks MANIFEST_M2B_ASM_v1.sha256 (whose own sha256 must start b56f49ee; every entry by sha256sum -c) and m2b_asm_v1.py against it; runs the
# asm once (it writes M2B_KV_v1.txt only after every gate, exclusive create, 444) with stdout in out/out_m2b_asm_v1.out; then requires
# exactly one 'VERDICT VALID' line, the first line naming the asm's own sha256, and exactly one 'RECORD M2B_KV_v1.txt <sha256>' line equal
# to the record's sha256; then reads the record back the consumers' way (m2b_reader_v1.py's script mode: load with the binding and C-PINS,
# and its plants) into out/out_m2b_reader_v1_check.out, which must end 'VERDICT VALID'; then writes the side manifest
# MANIFEST_M2B_KV_v1_RUN.sha256 (444). Stops at the first failed step. One line per step in out/run_m2b_asm_v1_v1.log.
D=/mnt/g2/release/root/code/pk02
L=$D/out/run_m2b_asm_v1_v1.log
M=$D/MANIFEST_M2B_ASM_v1.sha256
A=$D/m2b_asm_v1.py
R=$D/m2b_reader_v1.py
K=$D/M2B_KV_v1.txt
O=$D/out/out_m2b_asm_v1.out; E=${O%.out}.err
C=$D/out/out_m2b_reader_v1_check.out; CE=${C%.out}.err
S=$D/MANIFEST_M2B_KV_v1_RUN.sha256
stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
M8=$(sha256sum "$M" < /dev/null | cut -c1-8)
if [ "$M8" != b56f49ee ]; then echo "SHA MISMATCH manifest $M8 $(stamp)" >> "$L"; exit 3; fi
if ! sha256sum -c --quiet "$M" < /dev/null > /dev/null 2>&1; then echo "SHA MISMATCH: a file in the manifest differs $(stamp)" >> "$L"; exit 3; fi
AS=$(sha256sum "$A" < /dev/null | cut -c1-64)
for s in "$A" "$R"; do
  pin=$(awk -v p="$s" '$2 == p {print $1}' "$M")
  if [ -z "$pin" ] || [ "$pin" != "$(sha256sum "$s" < /dev/null | cut -c1-64)" ]; then echo "SHA MISMATCH ${s##*/} $(stamp)" >> "$L"; exit 3; fi
done
for f in "$K" "$O" "$E" "$C" "$CE" "$S"; do if [ -e "$f" ]; then echo "EXISTS ${f##*/} $(stamp)" >> "$L"; exit 4; fi; done
echo "SHA OK manifest $M8 (every entry; m2b_asm_v1 ${AS:0:8} and m2b_reader_v1 in it) $(stamp)" >> "$L"
echo "launch m2b_asm_v1 $(stamp)" >> "$L"
OMP_NUM_THREADS=1 timeout 580 nice -n 10 /usr/bin/time -v prlimit --as=8589934592 -- python3 -I -B "$A" > "$O" 2> "$E"
rc=$?
chmod 444 "$O" "$E"
cpu=$(awk -F': ' '/User time \(seconds\)|System time \(seconds\)/ {s += $2} END {printf "%.2f", s + 0}' "$E")
rss=$(awk -F': ' '/Maximum resident set size \(kbytes\)/ {printf "%.0f", $2 / 1024}' "$E")
echo "m2b_asm_v1 rc $rc cpu $cpu s peak RSS $rss MiB, bytes: output $(stat -c %s "$O"), stderr $(stat -c %s "$E"), record $( [ -e "$K" ] && stat -c %s "$K" || echo 0) $(stamp)" >> "$L"
awk '/^(C-|PLANT-|REFUSED|RECORD|VERDICT)/ && !/-> (PASS|FIRES)$/ {print "  " substr($0, 1, 230)}' "$O" >> "$L"
v=$(awk '/^VERDICT/' "$O")
if [ "$v" != "VERDICT VALID" ]; then echo "STOP: asm VERDICT lines are not exactly [VERDICT VALID]: $(printf '%s' "$v" | head -c 300) $(stamp)" >> "$L"; exit 5; fi
if [ "$(head -n 1 "$O" | awk '{print $1, $2, $3}')" != "m2b_asm_v1 sha256 $AS" ]; then echo "STOP: the output's first line does not name the asm's sha256 $(stamp)" >> "$L"; exit 5; fi
n=$(awk '/^RECORD M2B_KV_v1.txt [0-9a-f]{64}$/ {j++} END {print j + 0}' "$O")
rs=$(awk '/^RECORD M2B_KV_v1.txt [0-9a-f]{64}$/ {print $3}' "$O")
if [ "$n" != 1 ] || [ ! -f "$K" ] || [ "$(sha256sum "$K" < /dev/null | cut -c1-64)" != "$rs" ] || [ "$(stat -c %a "$K")" != 444 ]; then
  echo "STOP: RECORD line, record sha256 or mode (lines $n) $(stamp)" >> "$L"; exit 5
fi
echo "RECORD M2B_KV_v1.txt sha256 $rs (444); asm output ${O##*/} sha256 $(sha256sum "$O" | cut -c1-64) $(stamp)" >> "$L"
OMP_NUM_THREADS=1 timeout 300 nice -n 10 prlimit --as=4294967296 -- python3 -I -B "$R" "$K" "$O" "$rs" > "$C" 2> "$CE"
chmod 444 "$C" "$CE"
awk '/^(READ|PLANT-|VERDICT)/ {print "  reader: " substr($0, 1, 200)}' "$C" >> "$L"
if [ "$(awk '/^VERDICT/' "$C")" != "VERDICT VALID" ]; then echo "STOP: the reader's script-mode check is not VALID $(stamp)" >> "$L"; exit 5; fi
sha256sum "$K" "$O" "$E" "$C" "$CE" "$A" "$R" "$M" "$D/run_m2b_asm_v1_v1.sh" < /dev/null > "$S" && chmod 444 "$S"
echo "SIDE MANIFEST ${S##*/} sha256 $(sha256sum "$S" | cut -c1-64) ($(awk 'END {print NR}' "$S") files) $(stamp)" >> "$L"
echo "DONE $(stamp)" >> "$L"
