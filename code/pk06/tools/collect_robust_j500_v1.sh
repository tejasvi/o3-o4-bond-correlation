#!/bin/bash
# collect_robust_j500_v1.sh -- pk06: the two supporting runs at N = 4, J1 = 500 (G03, G18; the suggestion) into
# ROBUST_PK06_K3_J500_v1.tsv, and MANIFEST_PK06_K3_v2.txt = MANIFEST_PK06_K3_v1.txt (all its lines, unchanged) plus the sha256 of the
# two outputs, their guard logs, the new table, this script and v1 itself (run as one guarded job). The J1 = 350 runs remain the certificate.
P=/mnt/g2/release/root/code/pk06
R=$P/runs
T=$P/ROBUST_PK06_K3_J500_v1.tsv
M1=$P/MANIFEST_PK06_K3_v1.txt
M=$P/MANIFEST_PK06_K3_v2.txt
set -C
printf 'N\tJ1\torbit\te\tf\trun\tsigma\tcertified\tverdict\tchecks\tplants\tL\tc2\tL_over_c2\tmin_cell_ratio\tcpu_s\tpeak_rss_mb\tsha8\n' > "$T" || exit 3
for o in G03 G18; do
  f=$R/robust_n4_${o}_j500_v1.out
  [ -e "$f" ] || { echo "missing $f"; exit 4; }
  s8=$(sha256sum "$f" | cut -c1-8)
  awk -v F="$(basename "$f" .out)" -v S8="$s8" '
    $1 == "R-CERT" { orb = $2; e = $3; ff = $4; gsub(/[(,]/, "", e); gsub(/[)]/, "", ff); n = $5; sub(/N=/, "", n); j = $8; sub(/:/, "", j)
      if (match($0, /certified [A-Za-z]+/)) cert = substr($0, RSTART + 10, RLENGTH - 10)
      if (match($0, /sigma [0-9]+\/[0-9]+/)) sg = substr($0, RSTART + 6, RLENGTH - 6)
      if (match($0, /; L [-+0-9.e]+/)) L = substr($0, RSTART + 4, RLENGTH - 4)
      if (match($0, /; c2 [-+0-9.e]+/)) c2 = substr($0, RSTART + 5, RLENGTH - 5)
      if (match($0, /L \/ c2 [-+0-9.e]+/)) r = substr($0, RSTART + 7, RLENGTH - 7) }
    $1 == "CELL" && match($0, /Phi_lo \/ c2 [-+0-9.e]+/) { x = substr($0, RSTART + 12, RLENGTH - 12) + 0; if (mc == "" || x < mc) mc = x }
    $1 == "SUMMARY" { if (match($0, /VERDICT [A-Z]+/)) v = substr($0, RSTART + 8, RLENGTH - 8)
      if (match($0, /checks [0-9]+\/[0-9]+/)) ck = substr($0, RSTART + 7, RLENGTH - 7)
      if (match($0, /plants [0-9]+\/[0-9]+/)) pl = substr($0, RSTART + 7, RLENGTH - 7)
      if (match($0, /cpu [0-9.]+ s/)) cp = substr($0, RSTART + 4, RLENGTH - 6)
      if (match($0, /peak RSS [0-9]+ MB/)) rs = substr($0, RSTART + 9, RLENGTH - 12) }
    END { printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.6e\t%s\t%s\t%s\n", n, j, orb, e, ff, F, sg, cert, v, ck, pl, L, c2, r, mc, cp, rs, S8 }' "$f" >> "$T"
done
{ echo "# MANIFEST_PK06_K3_v2 -- pk06, P2-13 at K = 3. Supersedes MANIFEST_PK06_K3_v1.txt ($(sha256sum "$M1" | cut -c1-8)), whose lines follow unchanged; then the two supporting runs at N = 4, J1 = 500 (G03, G18), which are not part of the certificate (the J1 = 350 runs are)"
  cat "$M1"
  echo "# supporting runs: N = 4, J1 = 500, sigma 1/4, engine 8b7aff00; lines: sha256 path"
  sha256sum $R/robust_n4_G03_j500_v1.out $R/robust_n4_G18_j500_v1.out $R/robust_n4_G03_j500_v1.guard.log $R/robust_n4_G18_j500_v1.guard.log "$T" $P/tools/collect_robust_j500_v1.sh "$M1"
  for o in G03 G18; do echo "# robust_n4_${o}_j500_v1.guard.log: $(awk '/guard exits/' $R/robust_n4_${o}_j500_v1.guard.log)"; done; } > "$M"
cat "$T"
sha256sum "$T" "$M" | awk '{n = split($2, a, "/"); print "sha8", substr($1, 1, 8), a[n]}'
wc -l "$M" | awk '{print "lines", $1, $2}'
