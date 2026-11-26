#!/bin/bash
# job295 (pk22; item (4)): make mrx_combine_v1_10.py (make_mrx_combine_v1_10.py on the frozen mrx_combine_v1_9.py), its static check
# (ast.parse), a SCRATCH copy that joins the SCRATCH dry parts of job294 (CERTF the SCRATCH dry cert copy, OUTD out/SCRATCH_dry_v1_10, RUNS the
# job294 outputs, STATUS DRY), and its run; nothing is frozen here.
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
C=$S/midrow/g4/mrc
PY=python3
export TMPDIR=$C/tmp
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('STATIC ast.parse OK', sys.argv[1])" $C/src/make_mrx_combine_v1_10.py || { echo "STOP: maker static"; exit 3; }
$PY -I -B $C/src/make_mrx_combine_v1_10.py || { echo "STOP: maker failed"; exit 3; }
$PY -I -B -c "import ast, sys; ast.parse(open(sys.argv[1]).read()); print('STATIC ast.parse OK', sys.argv[1])" $C/src/mrx_combine_v1_10.py || { echo "STOP: static"; exit 3; }
$PY -I -B - $C/src/mrx_combine_v1_10.py $C/src/SCRATCH_dry_mrx_combine_v1_10.py <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src).read()
reps = [("OUTD = E + '/out/cert'   # mrx_combine_v1_8\n", "OUTD = E + '/out/SCRATCH_dry_v1_10'   # SCRATCH dry copy of mrx_combine_v1_10 (never cited)\n"),
        ("CERTF = E + '/src/mrx_cert_v1_10.py'\n", "CERTF = E + '/src/SCRATCH_dry_mrx_cert_v1_10.py'\n"),
        ("RUNS = {4: E + '/out/mrx_cert_v1_10_cert_n4.out', 3: E + '/out/mrx_cert_v1_10_cert_n3.out'}\n",
         "RUNS = {4: E + '/out/SCRATCH_dry_mrx_cert_v1_10_n4.out', 3: E + '/out/SCRATCH_dry_mrx_cert_v1_10_n3.out'}\n"),
        ("            or h.get('STATUS') != 'CERTIFIED' or h.get('RUN_VERDICT') != 'VALID':\n", "            or h.get('STATUS') != 'DRY' or h.get('RUN_VERDICT') != 'VALID':\n"),
        ("'STATUS = CERTIFIED', 'EXPORT_STATUS = CERTIFIED'", "'STATUS = DRY', 'EXPORT_STATUS = DRY'")]
for a, b in reps:
    assert t.count(a) == 1, (t.count(a), a[:60])
    t = t.replace(a, b)
open(dst, 'x').write(t)
print('SCRATCH copy written', dst)
PY
[ $? -eq 0 ] || { echo "STOP: scratch copy"; exit 3; }
O=$C/out/SCRATCH_dry_mrx_combine_v1_10.out
if [ -e $O ]; then echo "STOP: $O exists"; exit 3; fi
$PY -I -B $C/src/SCRATCH_dry_mrx_combine_v1_10.py > $O 2> ${O%.out}.err
echo "COMBINE rc=$?"
/usr/bin/cut -c1-900 $O
/usr/bin/tail -n 12 ${O%.out}.err
