#!/bin/bash
# job173 (pk25; P4 rerun on P2's N1-fixed table, the row 4691): ast of the v2_7 maker; build asm/kt_s9h_ins_v2_7.py from the v2_7 template
# (v2_6 with the cert record to mr/v5b) with pk23's Pev records and P2's new certified table p2/v3f2/MR_LEMMAP_V3F.kv (manifest
# p2/MANIFEST_P2_V2_3_CERT_c1.sha256); make mr/v5b; the certified run TAG c1; the rows against MR_INSERT v5 (mr/v5, 91f80105) and job164's
# compare with v4b saved to asm/out/cmp_ins_v2_7_cert_c1.out.
set -u
W=/mnt/g2/release/root/code
D=$W/pk25
PY=python3
$PY -I -B -c 'import ast, sys
for f in sys.argv[1:]:
    ast.parse(open(f).read(), f)
print("AST OK %d files" % (len(sys.argv) - 1))' $D/asm/make_kt_s9h_ins_v2_7.py || { echo "STOP ast"; exit 6; }
[ ! -e $D/asm/kt_s9h_ins_v2_7.py ] && [ ! -e $D/mr/v5b ] || { echo "STOP the engine or mr/v5b exists"; exit 6; }
$PY -I -B $D/asm/make_kt_s9h_ins_v2_7.py kt_s9h_ins_v2_7.py $D/asm/src/pevb_paths_v1.txt pk25/p2/v3f2/MR_LEMMAP_V3F.kv pk25/p2/MANIFEST_P2_V2_3_CERT_c1.sha256 | awk '!/^PINS_B/' || { echo "STOP maker"; exit 6; }
[ -f $D/asm/kt_s9h_ins_v2_7.py ] || { echo "STOP no engine"; exit 6; }
mkdir $D/mr/v5b || { echo "STOP mkdir"; exit 6; }
$PY -I -B $D/asm/kt_s9h_ins_v2_7.py cert c1
echo "cert c1 rc $?"
if [ -f $D/mr/v5b/MR_INSERT.kv ]; then
  awk -F' = ' 'FNR == 1 {f++} /^N[34]_P[0-9]+_[hta] = / {if (f == 1) {o[$1] = $2; n1++} else {n2++; if (!($1 in o)) miss++; else if (o[$1] != $2) d++}} END {printf "ROWS v5 %d, v5b %d, missing %d, differing %d\n", n1, n2, miss, d}' $D/mr/v5/MR_INSERT.kv $D/mr/v5b/MR_INSERT.kv
  diff <(awk '!/^N[34]_P[0-9]+_[hta] = /' $D/mr/v5/MR_INSERT.kv) <(awk '!/^N[34]_P[0-9]+_[hta] = /' $D/mr/v5b/MR_INSERT.kv) | cut -c1-200
  set -o noclobber
  bash $D/jobs/job164_cmp_ins_v2_5.sh $D/mr/v5b/MR_INSERT.kv > $D/asm/out/cmp_ins_v2_7_cert_c1.out
  echo "compare with v4b rc $?"
fi
exit 0
