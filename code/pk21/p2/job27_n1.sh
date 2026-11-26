#!/bin/bash
W=/mnt/g2/release/root/code
H=$W/pk15/out
O=$W/pk21/p2/a/out
R=$O/n1_export_pair_compare_v1.txt
{
for k in t 14_joint 14_means; do
  a=$H/export_p2_${k}_cert_kt_p2_assembly_v1_37.kv
  b=$H/export_p2_${k}_cert_kt_p2_assembly_v1_37_1.kv
  echo "== $k"
  sha256sum $a $b
  awk '/^N[34]_/' $a > $O/.rows_${k}_v1_37.txt
  awk '/^N[34]_/' $b > $O/.rows_${k}_v1_37_1.txt
  wc -l $O/.rows_${k}_v1_37.txt $O/.rows_${k}_v1_37_1.txt
  if cmp -s $O/.rows_${k}_v1_37.txt $O/.rows_${k}_v1_37_1.txt; then echo "ROWS IDENTICAL ($k)"; else echo "ROWS DIFFER ($k)"; fi
  echo "non-row lines that differ:"
  diff <(awk '!/^N[34]_/' $a) <(awk '!/^N[34]_/' $b) | cut -c1-200
done
} > $R 2>&1
