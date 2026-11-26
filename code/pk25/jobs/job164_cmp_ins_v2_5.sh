#!/bin/bash
# job164 (pk25; P4, the rows 4640, 4644): compares an MR_INSERT v5 record (argument 1) with the certified v4b record mr/v4b/MR_INSERT.kv.
# Conditions: the same FIELDS, X_POWER, X_DEFINITION, ORIENTATION, TRIAL_SET, LEMMAP_SHA256 and PEV_ROUTE lines; the same row keys in the same
# order; every field of every row byte-equal, except on the two last h rows (N4_P0903_h, N3_P0903_h) the five way A fields vx_lo, vx_hi,
# xc_lo, xc_hi, xf_hi, printed old and new; on those rows xf_hi = 0 and vx_lo = 0. Prints the header keys that differ (CODE, PRODUCER,
# STATUS, SOURCE and the comment line are expected to); writes nothing. Exit 0 only if every condition holds.
set -u
D=/mnt/g2/release/root/code/pk25
NEW=$1
OLD=$D/mr/v4b/MR_INSERT.kv
[ -f "$NEW" ] && [ -f "$OLD" ] || { echo "STOP missing input"; exit 6; }
echo "OLD $OLD sha256 $(sha256sum "$OLD" | cut -c1-64)"
echo "NEW $NEW sha256 $(sha256sum "$NEW" | cut -c1-64)"
awk 'FNR == 1 {f++}
  /^#/ {next}
  /^N[34]_P[0-9]+_[hta] = / {
    val = substr($0, index($0, " = ") + 3); key = substr($0, 1, index($0, " = ") - 1)
    if (f == 1) {old[key] = val; ko[++no] = key; next}
    kn[++nn] = key; new[key] = val; next
  }
  index($0, " = ") > 0 {
    val = substr($0, index($0, " = ") + 3); key = substr($0, 1, index($0, " = ") - 1)
    if (key == "FIELDS") {if (f == 1) fo = val; else fn = val; n = split(val, a, " "); for (i = 1; i <= n; i++) ix[a[i]] = i; next}
    if (f == 1) ho[key] = val; else hn[key] = val
  }
  END {
    bad = 0
    if (fo != fn) {print "FIELDS differ"; bad++}
    split("X_POWER X_DEFINITION ORIENTATION TRIAL_SET LEMMAP_SHA256 PEV_ROUTE", must, " ")
    for (j = 1; j <= 6; j++) if (ho[must[j]] != hn[must[j]]) {print "HEADER-MUST-EQUAL differs: " must[j]; bad++}
    for (k in ho) if (!(k in hn) || ho[k] != hn[k]) print "HEADER differs (expected for CODE PRODUCER STATUS SOURCE): " k
    for (k in hn) if (!(k in ho)) {print "HEADER new key: " k; bad++}
    if (no != nn) {print "ROW COUNT old " no " new " nn; bad++}
    for (i = 1; i <= no && i <= nn; i++) if (ko[i] != kn[i]) {print "ROW ORDER differs at " i ": " ko[i] " vs " kn[i]; bad++; break}
    split("vx_lo vx_hi xc_lo xc_hi xf_hi", wa, " ")
    for (j = 1; j <= 5; j++) allow[ix[wa[j]]] = 1
    same = 0; last = 0
    for (i = 1; i <= no; i++) {
      k = ko[i]
      if (!(k in new)) {print "MISSING " k; bad++; continue}
      no_ = split(old[k], o, " "); nn_ = split(new[k], v, " ")
      if (no_ != nn_) {print "ROW LENGTH " k; bad++; continue}
      islast = (k == "N4_P0903_h" || k == "N3_P0903_h")
      d = 0
      for (m = 1; m <= no_; m++) {
        if (o[m] == v[m]) continue
        if (islast && (m in allow)) continue
        d++
        if (d <= 3) print "FIELD-DIFF " k " " a[m] ": " o[m] " -> " v[m]
      }
      if (d) bad++
      else if (!islast) same++
      if (islast) {
        last++
        printf "WAYA-ROW %s:", k
        for (j = 1; j <= 5; j++) printf " %s %s -> %s;", wa[j], o[ix[wa[j]]], v[ix[wa[j]]]
        print ""
        if (v[ix["xf_hi"]] != "0") {print "WAYA-ROW " k " xf_hi is not 0"; bad++}
        if (v[ix["vx_lo"]] + 0 != 0) {print "WAYA-ROW " k " vx_lo is not 0"; bad++}
      }
    }
    printf "ROWS %d; byte-identical rows %d; way A rows %d; conditions failing %d\n", no, same, last, bad
    exit (bad == 0 && last == 2 && same == no - 2) ? 0 : 3
  }' "$OLD" "$NEW"
rc=$?
echo "COMPARE rc=$rc (0 = all rows byte-identical to v4b except the five way A fields of the two last h rows, with xf_hi = 0 and vx_lo = 0)"
exit $rc
