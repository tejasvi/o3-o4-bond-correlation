#!/bin/bash
# job70 (pk25): freeze the C5 forks m4h_reader_v1 and m4h_asm_v1 with their maker, diffs and maker job: manifest
# pk25/m4h/MANIFEST_C5_M4H_v1.sha256 (paths relative to code), chmod a-w (files only).
W=/mnt/g2/release/root/code
cd $W || exit 2
set -o noclobber
M=pk25/m4h/MANIFEST_C5_M4H_v1.sha256
[ ! -e $M ] || { echo "STOP exists $M"; exit 6; }
L=(pk25/m4h/m4h_reader_v1.py pk25/m4h/m4h_asm_v1.py pk25/m4h/make_m4h_v1.py pk25/m4h/diff_m4_reader_v1_to_m4h_reader_v1.txt
   pk25/m4h/diff_m4_asm_v1_to_m4h_asm_v1.txt pk25/out/job69_make.out pk25/jobs/job69_m4h_make.sh pk25/guard/job69_m4h_make.log
   pk25/jobs/job68_freeze_c4s2.sh pk25/guard/job68_freeze_c4s2.log)
for f in "${L[@]}"; do [ -f "$f" ] || { echo "STOP missing $f"; exit 4; }; done
sha256sum "${L[@]}" > $M || exit 3
sha256sum -c --quiet $M || { echo "STOP check"; exit 5; }
chmod a-w "${L[@]}" $M
echo "FROZE $M $(wc -l < $M) files sha256 $(sha256sum $M | cut -d' ' -f1); still writable among them: $(find "${L[@]}" $M -perm /222 | wc -l)"
for f in pk25/m4h/m4h_asm_v1.py pk25/m4h/m4h_reader_v1.py pk25/m4h/make_m4h_v1.py pk25/m4h/diff_m4_asm_v1_to_m4h_asm_v1.txt pk25/m4h/diff_m4_reader_v1_to_m4h_reader_v1.txt; do echo "$f $(sha256sum $f | cut -c1-8)"; done
