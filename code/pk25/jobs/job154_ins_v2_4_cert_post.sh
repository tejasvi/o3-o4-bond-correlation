#!/bin/bash
# job154 (pk25; the P0_LOG rows 4521, 4525, 4526, 4534): after the option (B) MR_INSERT cert run (asm/kt_s9h_ins_v2_4.py cert CTAG), checks:
#  (1) the cert out: the engine and mode line, VERDICT VALID, every plant fired (PLANTS line: not firing none), C-PEVB-READ and C-PEVB-T048 PASS;
#  (2) the record's rows byte-equal to the dry record's (dry tag DTAG), and only the header comment and the two STATUS lines differ;
#  (3) the MU-T and MU lines (OR_t, c_t, c~_h intervals, OR, C) identical to the certified v4 run's (asm/out/out_kt_s9h_ins_v2_2_cert_c1.out),
#      which MR_JOINT reads (the row 4534);
#  (4) job153's compare on the cert record (only Pev_hi and vp_hi differ from mr/v4, the six h-row columns byte-identical, no Pev_hi rises);
#  then writes the compare file asm/out/cmp_ins_v2_4_cert_<CTAG>.out with the INFO PEV MAX lines (the gate report) and the manifest
#  mr/MANIFEST_MR_V4B_CERT_v1.sha256 (noclobber), and makes the record, outs, compare file and manifest read-only. Usage: job154 DTAG CTAG
set -u
D=/mnt/g2/release/root/code/pk25
cd "$D" || exit 6
[ $# -eq 2 ] || { echo "usage: job154 DTAG CTAG"; exit 2; }
DT=$1
CT=$2
E=asm/kt_s9h_ins_v2_4.py
REC=mr/v4b/MR_INSERT.kv
DRY=asm/dry_$DT/MR_INSERT.kv
OC=asm/out/out_kt_s9h_ins_v2_4_cert_$CT.out
OD=asm/out/out_kt_s9h_ins_v2_4_dry_$DT.out
O4=asm/out/out_kt_s9h_ins_v2_2_cert_c1.out
P=asm/out/cmp_ins_v2_4_cert_$CT.out
M=mr/MANIFEST_MR_V4B_CERT_v1.sha256
C153=jobs/job153_cmp_ins_v2_4.sh
TD=$D/tmp/job154_$CT
for f in "$E" "$REC" "$DRY" "$OC" "$OD" "$O4" "$C153" asm/make_kt_s9h_ins_v2_4.py asm/src/kt_s9h_ins_v2_4.py.in asm/src/pevb_paths_v1.txt; do
  [ -f "$f" ] || { echo "STOP missing $f"; exit 6; }
done
for f in "$P" "$M" "$TD"; do
  [ ! -e "$f" ] || { echo "STOP exists $f"; exit 6; }
done
es=$(sha256sum "$E" | cut -c1-64)
n1=$(awk -v s="$es" -v t="$CT" 'index($0, "kt_s9h_ins_v2_4 sha256 " s " MODE=cert TAG=" t " ") == 1' "$OC" | wc -l)
n2=$(awk '/^VERDICT VALID$/' "$OC" | wc -l)
n3=$(awk '/^PLANTS: / && /not firing: none$/ && /not run or repeated: none/' "$OC" | wc -l)
n4=$(awk '/^C-PEVB-READ: / && / -> PASS$/' "$OC" | wc -l)
n5=$(awk '/^C-PEVB-T048: / && / -> PASS$/' "$OC" | wc -l)
[ "$n1$n2$n3$n4$n5" = "11111" ] || { echo "STOP cert out: engine line $n1, VERDICT VALID $n2, PLANTS $n3, C-PEVB-READ $n4, C-PEVB-T048 $n5"; exit 7; }
mkdir "$TD" || exit 6
awk '/^N[34]_P/' "$REC" > "$TD/rows_cert.txt"
awk '/^N[34]_P/' "$DRY" > "$TD/rows_dry.txt"
cmp "$TD/rows_cert.txt" "$TD/rows_dry.txt"
rc=$?
awk '!/^N[34]_P/' "$REC" > "$TD/head_cert.txt"
awk '!/^N[34]_P/' "$DRY" > "$TD/head_dry.txt"
hl=$(awk 'NR == FNR {a[FNR] = $0; n = FNR; next} {m = FNR; if (a[FNR] != $0) s = s (s == "" ? "" : ",") FNR} END {print (n == m) ? s : "COUNT"}' "$TD/head_dry.txt" "$TD/head_cert.txt")
awk '/^MU-T N=|^MU N=/' "$OC" > "$TD/mu_cert.txt"
awk '/^MU-T N=|^MU N=/' "$O4" > "$TD/mu_v4.txt"
cmp "$TD/mu_cert.txt" "$TD/mu_v4.txt"
mrc=$?
nmu=$(wc -l < "$TD/mu_cert.txt")
bash "$C153" "$REC" > "$TD/job153.out"
crc=$?
(
  set -o noclobber
  {
    echo "# job154 (pk25): option (B) MR_INSERT cert $CT against dry $DT, written $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "CERT $REC sha256 $(sha256sum "$REC" | cut -c1-64) lines $(wc -l < "$REC")"
    echo "DRY $DRY sha256 $(sha256sum "$DRY" | cut -c1-64) lines $(wc -l < "$DRY")"
    echo "ROWS cert $(wc -l < "$TD/rows_cert.txt") dry $(wc -l < "$TD/rows_dry.txt"); cmp rc $rc (0 = byte-equal)"
    echo "HEADER lines that differ: $hl (expected 1,6,7: the comment line and the two STATUS lines)"
    echo "MU lines (OR_t, c_t, c~_h intervals, OR, C; main row 4534): $nmu lines, cmp against the v4 cert run $(sha256sum "$O4" | cut -c1-8): rc $mrc (0 = identical)"
    cat "$TD/job153.out"
    echo "JOB153 rc $crc"
    awk '/^INFO PEV MAX /' "$OC"
    if [ "$rc" = 0 ] && [ "$hl" = "1,6,7" ] && [ "$mrc" = 0 ] && [ "$nmu" = 4 ] && [ "$crc" = 0 ]; then echo "POST PASS"; else echo "POST FAIL"; fi
  } > "$P"
) || { echo "STOP could not write $P"; exit 6; }
cat "$P"
awk '/^POST PASS$/' "$P" | wc -l | awk '{exit ($1 == 1) ? 0 : 1}' || { echo "STOP post check failed: no manifest, nothing made read-only"; exit 7; }
( set -o noclobber; sha256sum "$REC" "$OC" "$DRY" "$OD" "$P" "$E" asm/make_kt_s9h_ins_v2_4.py asm/src/kt_s9h_ins_v2_4.py.in asm/src/pevb_paths_v1.txt "$C153" jobs/job154_ins_v2_4_cert_post.sh > "$M" ) || { echo "STOP could not write $M"; exit 6; }
chmod a-w "$REC" "$OC" "$DRY" "$OD" "$P" "$M"
sha256sum -c --quiet "$M" && echo "MANIFEST $M sha256 $(sha256sum "$M" | cut -c1-64) rows $(wc -l < "$M") CHECK OK"
