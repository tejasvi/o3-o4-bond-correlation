#!/bin/bash
# job292 (pk22; item (4), try 3: + C-WAYA-JOIN): make mrx_cert_v1_10.py (make_mrx_v1_10_r2.py, the corrected F form: Way A for h-1 and h0 on the last piece), its static check (ast.parse),
# and a SCRATCH dry copy (parts to out/SCRATCH_dry_v1_10, STATUS DRY) for a test run; nothing is frozen here.
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
C=$S/midrow/g4/mrc
export TMPDIR=$C/tmp
mkdir -p $C/tmp $C/out/SCRATCH_dry_v1_10
python3 -I -B $C/src/make_mrx_v1_10_r2.py || { echo "STOP: maker failed"; exit 3; }
python3 -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('STATIC ast.parse OK', sys.argv[1])" $C/src/mrx_cert_v1_10.py || { echo "STOP: static"; exit 3; }
python3 -I -B - $C/src/mrx_cert_v1_10.py $C/src/SCRATCH_dry_mrx_cert_v1_10.py <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src).read()
o1 = "OUTD = W + '/pk22/midrow/g4/mrc/out/cert'   # mrx_cert_v1_8: the certified parts\n"
o2 = "'STATUS = CERTIFIED', 'EXPORT_STATUS = PART'"
assert t.count(o1) == 1 and t.count(o2) == 1, (t.count(o1), t.count(o2))
t = t.replace(o1, "OUTD = W + '/pk22/midrow/g4/mrc/out/SCRATCH_dry_v1_10'   # SCRATCH dry copy of mrx_cert_v1_10 (never cited)\n")
t = t.replace(o2, "'STATUS = DRY', 'EXPORT_STATUS = PART'")
open(dst, 'x').write(t)
print('SCRATCH copy written', dst)
PY
