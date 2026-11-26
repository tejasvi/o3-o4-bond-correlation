#!/bin/bash
# job145 (pk25): after the C11 cert run (asm/kt_s9h_crudex_v1.py cert c1, under the approval), checks that the certified record's rows equal the
# dry x1 record's byte for byte and that only the header comment and the two STATUS lines differ, writes the compare file
# asm/out/cmp_crudex_v1_dry_x1_cert_c1.out and the manifest mr/MANIFEST_MR_V4_CRUDEX_CERT_v1.sha256 (both noclobber), and makes the record,
# its out file, the compare file and the manifest read-only. No compute; hashes and counts come from tools here.
set -u
D=/mnt/g2/release/root/code/pk25
cd "$D" || exit 6
C=mr/v4/MR_CRUDEX.kv
X=asm/dry_x1/MR_CRUDEX.kv
O=asm/out/out_kt_s9h_crudex_v1_cert_c1.out
G=guard/crudex_v1_cert_c1.log
E=asm/kt_s9h_crudex_v1.py
P=asm/out/cmp_crudex_v1_dry_x1_cert_c1.out
M=mr/MANIFEST_MR_V4_CRUDEX_CERT_v1.sha256
S=jobs/job145_crudex_cert_post.sh
TD=$D/tmp/job145
for f in "$C" "$X" "$O" "$G" "$E" "$S" MANIFEST_CRUDEX_V1_DRY_x1.sha256; do
  [ -f "$f" ] || { echo "STOP missing $f"; exit 6; }
done
for f in "$P" "$M" "$TD"; do
  [ ! -e "$f" ] || { echo "STOP exists $f"; exit 6; }
done
sha256sum -c --quiet MANIFEST_CRUDEX_V1_DRY_x1.sha256 || { echo "STOP the dry x1 manifest does not check (engine, template, maker, dry record)"; exit 6; }
nv=$(awk '/^VERDICT VALID$/' "$O" | wc -l)
np=$(awk '/^PLANTS: 5 of 5 must-fire plants ran \(not run or repeated: none\); not firing: none$/' "$O" | wc -l)
nm=$(awk -v s="$(sha256sum "$E" | cut -c1-64)" 'index($0, "kt_s9h_crudex_v1 sha256 " s " MODE=cert TAG=c1 ") == 1' "$O" | wc -l)
[ "$nv" = 1 ] && [ "$np" = 1 ] && [ "$nm" = 1 ] || { echo "STOP out file: VERDICT VALID $nv, PLANTS 5 of 5 $np, engine and mode line $nm"; exit 7; }
mkdir "$TD" || exit 6
awk '/^N[34]_P/' "$C" > "$TD/rows_cert.txt"
awk '/^N[34]_P/' "$X" > "$TD/rows_dry.txt"
cmp "$TD/rows_cert.txt" "$TD/rows_dry.txt"
rc=$?
awk '!/^N[34]_P/' "$C" > "$TD/head_cert.txt"
awk '!/^N[34]_P/' "$X" > "$TD/head_dry.txt"
diff "$TD/head_dry.txt" "$TD/head_cert.txt" > "$TD/head_diff.txt"
drc=$?
hl=$(awk 'NR == FNR {a[FNR] = $0; n = FNR; next} {m = FNR; if (a[FNR] != $0) s = s (s == "" ? "" : ",") FNR} END {print (n == m) ? s : "COUNT"}' "$TD/head_dry.txt" "$TD/head_cert.txt")
st=$(awk '/^STATUS = CERTIFIED$/ || /^EXPORT_STATUS = CERTIFIED$/' "$C" | wc -l)
(
  set -o noclobber
  {
    echo "# job145 (pk25): C11 cert c1 against dry x1, written $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "CERT $C sha256 $(sha256sum "$C" | cut -c1-64) lines $(wc -l < "$C")"
    echo "DRY $X sha256 $(sha256sum "$X" | cut -c1-64) lines $(wc -l < "$X")"
    echo "ROWS cert $(wc -l < "$TD/rows_cert.txt") dry $(wc -l < "$TD/rows_dry.txt"); cmp rc $rc (0 = byte-equal)"
    echo "HEADER lines that differ: $hl (expected 1,6,7: the comment line and the two STATUS lines); STATUS lines CERTIFIED: $st of 2; diff rc $drc"
    cat "$TD/head_diff.txt"
    if [ "$rc" = 0 ] && [ "$hl" = "1,6,7" ] && [ "$st" = 2 ]; then echo "COMPARE PASS"; else echo "COMPARE FAIL"; fi
  } > "$P"
) || { echo "STOP could not write $P"; exit 6; }
cat "$P"
awk '/^COMPARE PASS$/' "$P" | wc -l | awk '{exit ($1 == 1) ? 0 : 1}' || { echo "STOP compare failed: no manifest, nothing made read-only"; exit 7; }
( set -o noclobber; sha256sum "$C" "$O" "$P" "$E" "$G" "$S" > "$M" ) || { echo "STOP could not write $M"; exit 6; }
chmod a-w "$C" "$O" "$P" "$M"
sha256sum -c --quiet "$M" && echo "MANIFEST $M sha256 $(sha256sum "$M" | cut -c1-64) rows $(wc -l < "$M") CHECK OK"
