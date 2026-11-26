#!/bin/bash
# job72 (pk25): freeze C5's first cert run outputs, then the v1_1 maker (PLANT-SWAP on M0; names to v1_1), ast.parse of both new files,
# and the freeze of v1_1 with its maker and diffs: manifest pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 (paths relative to code), chmod a-w.
W=/mnt/g2/release/root/code
PY=python3
cd $W || exit 2
set -o noclobber
O=pk25/out/job72_make.out
M=pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256
for f in $O $M; do [ ! -e "$f" ] || { echo "STOP exists $f"; exit 6; }; done
TMPDIR=$W/pk25/tmp $PY -I -B pk25/m4h/make_m4h_v1_1.py > $O 2>&1
rc=$?; cat $O; [ $rc = 0 ] || { echo "STOP maker rc $rc"; exit 3; }
$PY -I -B -c "import ast,sys; [ast.parse(open(f).read()) for f in sys.argv[1:]]; print('ast.parse ok', len(sys.argv) - 1, 'files')" pk25/m4h/m4h_reader_v1_1.py pk25/m4h/m4h_asm_v1_1.py || exit 3
L=(pk25/m4h/m4h_reader_v1_1.py pk25/m4h/m4h_asm_v1_1.py pk25/m4h/make_m4h_v1_1.py pk25/m4h/diff_m4h_reader_v1_to_v1_1.txt
   pk25/m4h/diff_m4h_asm_v1_to_v1_1.txt $O pk25/jobs/job72_m4h_v1_1.sh pk25/m4h/out/out_m4h_asm_v1.out pk25/m4h/out/out_m4h_asm_v1.err
   pk25/jobs/c5_run_v1.sh pk25/guard/c5_run_v1.log pk25/guard/job71_bashn.log pk25/jobs/job70_freeze_m4h.sh pk25/guard/job70_freeze_m4h.log)
for f in "${L[@]}"; do [ -f "$f" ] || { echo "STOP missing $f"; exit 4; }; done
sha256sum "${L[@]}" > $M || exit 3
sha256sum -c --quiet $M || { echo "STOP check"; exit 5; }
chmod a-w "${L[@]}" $M
echo "FROZE $M $(wc -l < $M) files sha256 $(sha256sum $M | cut -d' ' -f1); still writable among them: $(find "${L[@]}" $M -perm /222 | wc -l)"
for f in pk25/m4h/m4h_asm_v1_1.py pk25/m4h/m4h_reader_v1_1.py pk25/m4h/make_m4h_v1_1.py pk25/m4h/out/out_m4h_asm_v1.out; do echo "$f $(sha256sum $f | cut -c1-8)"; done
