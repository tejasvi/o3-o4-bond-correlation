#!/bin/bash
# SCRATCH_freeze_asm_reader_v1.sh -- pk02 hand: freezes m2b_reader_v1.py (from SCRATCH_m2b_reader_v1_draft_e2.py: the docstring loses
# '(draft d)' and the 'DRAFT (by hand)' line) and m2b_asm_v1.py (kit c on SCRATCH_m2b_asm_v1_draft_f.py), both 444, after the rerun's records
# and rep_v1_5's outputs are VALID; lints both; writes the dry copy SCRATCH_asmdry/m2b_asm_v1_dry.py (OUTREC in SCRATCH_asmdry only).
# Runs nothing else. Every hash is computed.
D=/mnt/g2/release/root/code/pk02
PY="env OMP_NUM_THREADS=1 timeout 120 nice -n 10 prlimit --as=4294967296 -- python3 -I -B"
R=$D/m2b_reader_v1.py; A=$D/m2b_asm_v1.py; X=$D/SCRATCH_asmdry; Y=$X/m2b_asm_v1_dry.py
for f in "$R" "$A" "$Y"; do [ ! -e "$f" ] || { echo "exists: $f"; exit 2; }; done
for n in 4 3; do
  for f in "$D/out/out_m2b_rep_v1_5_n$n.out" "$D/out/out_m2b_floatref_v2_n$n.out"; do
    [ "$(awk '/^VERDICT/' "$f" 2> /dev/null)" = "VERDICT VALID" ] || { echo "not VALID or missing: $f"; exit 3; }
  done
  for p in d5 dwt dwl r0 tA; do
    f=$D/out_m2b_cert_v1_4_$p.n$n.out
    [ "$(awk '/^VERDICT/' "$f" 2> /dev/null)" = "VERDICT VALID" ] || { echo "not VALID or missing: $f"; exit 3; }
  done
done
awk '$0 == "DRAFT (by hand): frozen before m2b_asm_v1, which pins it." {n1++; next} /^Also checked \(draft d\): / {sub(/^Also checked \(draft d\): /, "Also checked: "); n2++} {print} END {if (n1 != 1 || n2 != 1) exit 9}' \
  "$D/SCRATCH_m2b_reader_v1_draft_e2.py" > "$R" || { echo "reader edit counts wrong"; exit 4; }
chmod 444 "$R"
$PY "$D/SCRATCH_mk_asm_freeze_c.py" "$D/SCRATCH_m2b_asm_v1_draft_f.py" "$A" || { echo "kit c refused"; exit 5; }
chmod 444 "$A"
for f in "$R" "$A"; do echo "lint $(basename "$f"): $($PY "$D/SCRATCH_namecheck_b.py" "$f" 2>&1 | tail -n 1)"; done
mkdir -p "$X" || exit 6
awk -v o="OUTREC = os.path.join(OWN, 'SCRATCH_asmdry', 'M2B_KV_v1_DRY.txt')   # DRY COPY: the record goes to SCRATCH_asmdry only" \
  '$0 == "OUTREC = os.path.join(OWN, '"'"'M2B_KV_v1.txt'"'"')" {print o; n++; next} {print} END {if (n != 1) exit 9}' "$A" > "$Y" || { echo "dry edit count wrong"; exit 7; }
echo "frozen: m2b_reader_v1.py $(sha256sum "$R" | cut -c1-8), m2b_asm_v1.py $(sha256sum "$A" | cut -c1-8); dry copy $(sha256sum "$Y" | cut -c1-8)"
diff "$A" "$Y"
true
