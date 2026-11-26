#!/bin/bash
W=/mnt/g2/release/root/code
O=$W/pk07/out
M=$W/pk21/p2/s4c/out
R=$M/cmp_vs_original_v1.txt
{
echo "piece rows (lines starting N3_P or N4_P followed by a digit) of the two vsweep exports:"
awk '/^N[34]_P[0-9]/' $O/export_kt_s9h_v1_2_vsweep.kv > $M/.rows_orig_v1.txt
awk '/^N[34]_P[0-9]/' $M/export_kt_s9h_tau4_pk21_v1_vsweep.kv > $M/.rows_copy_v1.txt
wc -l $M/.rows_orig_v1.txt $M/.rows_copy_v1.txt
if cmp -s $M/.rows_orig_v1.txt $M/.rows_copy_v1.txt; then echo "PIECE ROWS IDENTICAL"; else echo "PIECE ROWS DIFFER"; fi
echo "header lines that differ (excluding piece rows):"
diff <(awk '!/^N[34]_P[0-9]/' $O/export_kt_s9h_v1_2_vsweep.kv) <(awk '!/^N[34]_P[0-9]/' $M/export_kt_s9h_tau4_pk21_v1_vsweep.kv) | head -20
echo "run output lines S5/S6/S7/INFO-HARM/C-MV/VERDICT: original vs copy"
diff <(awk '/^S5 N=|^S6 N=|^S7 N=|^INFO-HARM|^C-MV N=|^VERDICT/' $O/out_kt_s9h_v1_2_vsweep.out) <(awk '/^S5 N=|^S6 N=|^S7 N=|^INFO-HARM|^C-MV N=|^VERDICT/' $M/out_kt_s9h_tau4_pk21_v1_vsweep.out) && echo "THOSE LINES IDENTICAL"
} > $R 2>&1
