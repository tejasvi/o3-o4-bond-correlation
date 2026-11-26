#!/bin/bash
# SCRATCH (pk02, hand): writes the manifest of the m2b_asm_v1 package from the frozen asm's own pin tables (every quoted path under code/
# in its lines before 'def sha_file') plus the package's code, specs, drafts and kit; sha256sum computes every hash. argv: manifest name
# (a new file in the own folder).
CODEDIR=/mnt/g2/release/root/code
D=$CODEDIR/pk02
M=$D/$1
[ -n "$1" ] && [ "$(dirname "$(realpath -m "$M")")" = "$(realpath "$D")" ] && [ ! -e "$M" ] || { echo "manifest must be a new file in the own folder"; exit 2; }
A=$D/m2b_asm_v1.py
[ -f "$A" ] && [ -f "$D/m2b_reader_v1.py" ] || { echo "asm or reader not frozen"; exit 2; }
L=$D/SCRATCH_asm_manifest_list.txt
[ ! -e "$L" ] || { echo "list file exists: $L"; exit 2; }
{
  for f in m2b_asm_v1.py m2b_reader_v1.py SCRATCH_m2b_asm_v1_draft_f.py SCRATCH_m2b_reader_v1_draft_e2.py SCRATCH_mk_asm_freeze_c.py \
           SCRATCH_freeze_asm_reader_v1.sh SCRATCH_mk_asm_manifest_v1.sh SPEC_M2B_CERT_v1.md SPEC_M2B_CERT_v1_ADD1.md SPEC_M2B_CERT_v1_ADD2.md \
           SPEC_M2B_CERT_v1_ADD3.md arbeng_ma_v1_1.py arbeng_ma_v1_2.py RECORD_INDEX_F2_pk02_v2.md \
           SCRATCH_asmdry/m2b_asm_v1_dry.py SCRATCH_asmdry/out_m2b_asm_v1_dry.out SCRATCH_asmdry/out_m2b_asm_v1_dry.err \
           SCRATCH_asmdry/M2B_KV_v1_DRY.txt; do
    echo "$D/$f"
  done
  awk '/^def sha_file/ {exit} {print}' "$A" | /usr/bin/grep -o "'\(pk02\|pk03\|rv01\|pk11\|pk10\|pk08\)/[^']*'" | \
    awk -v w="$CODEDIR" '{gsub("\047", ""); print w "/" $0}'
} | awk '!seen[$0]++' > "$L" || exit 3
n=0; miss=0
while read -r p; do
  if [ -f "$p" ]; then n=$((n + 1)); else echo "MISSING $p"; miss=$((miss + 1)); fi
done < "$L"
[ "$miss" -eq 0 ] || { echo "$miss missing; no manifest written"; exit 4; }
xargs -d '\n' sha256sum < "$L" > "$M" || exit 5
chmod 444 "$M"
echo "wrote $(basename "$M"): $(awk 'END{print NR}' "$M") files ($n listed), sha256 $(sha256sum "$M" | awk '{print $1}')"
