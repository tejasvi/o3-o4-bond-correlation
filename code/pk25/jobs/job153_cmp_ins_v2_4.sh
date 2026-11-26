#!/bin/bash
# job153 (pk25; the P0_LOG rows 4525, 4526): compares an MR_INSERT v2_4 record (argument 1) with the certified
# mr/v4/MR_INSERT.kv. Conditions: the same header FIELDS and row keys; on every row every field byte-equal except Pev_hi and vp_hi (Pevw_hi
# included in the byte-equal set: row 4526 withdraws row 4521's allowance); the six h-row columns MR_CRUDEX reads (vx, vy, mxx, mxy as their
# _lo and _hi fields, Pevw_hi, PeBwux_hi) byte-identical on every h row, printed as their own line; no Pev_hi above the old value. Prints
# counts and ranges; writes nothing. Exit 0 only if every condition holds. (job150, frozen, allowed Pevw_hi to move; this is its successor.)
set -u
D=/mnt/g2/release/root/code/pk25
NEW=$1
OLD=$D/mr/v4/MR_INSERT.kv
[ -f "$NEW" ] && [ -f "$OLD" ] || { echo "STOP missing input"; exit 6; }
fo=$(awk '/^FIELDS = /' "$OLD")
fn=$(awk '/^FIELDS = /' "$NEW")
[ "$fo" = "$fn" ] || { echo "STOP FIELDS differ"; exit 7; }
echo "OLD $OLD sha256 $(sha256sum "$OLD" | cut -c1-64)"
echo "NEW $NEW sha256 $(sha256sum "$NEW" | cut -c1-64)"
awk -F' = ' 'FNR == 1 {f++}
  /^FIELDS = / {n = split($2, a, " "); for (i = 1; i <= n; i++) ix[a[i]] = i; next}
  /^N[34]_P[0-9]+_[hta] = / {
    if (f == 1) {old[$1] = $2; no++; next}
    nn++
    if (!($1 in old)) {miss++; next}
    split(old[$1], o, " "); split($2, v, " ")
    for (i = 1; i <= n; i++) {
      if (i == ix["Pev_hi"] || i == ix["vp_hi"]) continue
      if (o[i] != v[i]) {other++; if (other <= 5) print "OTHER-FIELD " $1 " " a[i] ": " o[i] " -> " v[i]}
    }
    if (substr($1, length($1)) == "h") {
      nh++
      split("vx_lo vx_hi vy_lo vy_hi mxx_lo mxx_hi mxy_lo mxy_hi Pevw_hi PeBwux_hi", six, " ")
      d6 = 0
      for (k = 1; k <= 10; k++) if (o[ix[six[k]]] != v[ix[six[k]]]) d6 = 1
      if (d6) {h6++; if (h6 <= 5) print "SIX-COLUMN-DIFF " $1}
    }
    pn = v[ix["Pev_hi"]] + 0; po = o[ix["Pev_hi"]] + 0
    if (pn > po) {up++; if (up <= 5) print "PEV-UP " $1 " " po " -> " pn}
    if (v[ix["Pev_hi"]] != o[ix["Pev_hi"]]) chp++
    if (v[ix["Pevw_hi"]] != o[ix["Pevw_hi"]]) chw++
    if (v[ix["vp_hi"]] != o[ix["vp_hi"]]) chv++
    t = substr($1, length($1)); if (!(t in mn) || pn < mn[t]) mn[t] = pn; if (pn > mx[t]) {mx[t] = pn; km[t] = $1}
  }
  END {
    printf "ROWS old %d new %d, missing in old %d; fields other than Pev_hi and vp_hi differing %d (Pevw_hi changed on %d rows); Pev_hi raised %d; changed Pev_hi %d, vp_hi %d\n", no, nn, miss, other, chw, up, chp, chv
    printf "SIX-COLUMNS (vx, vy, mxx, mxy as _lo and _hi, Pevw_hi, PeBwux_hi; main row 4526): %d h rows compared, %d differing -> %s\n", nh, h6, (h6 == 0 && nh > 0) ? "BYTE-IDENTICAL" : "DIFFERENT"
    for (t in mn) printf "PEV %s: new Pev_hi from %.4g to %.4g (largest on %s)\n", t, mn[t], mx[t], km[t]
    exit (no == nn && miss == 0 && other == 0 && up == 0 && h6 == 0 && nh > 0) ? 0 : 3
  }' "$OLD" "$NEW"
rc=$?
echo "COMPARE rc=$rc (0 = only Pev_hi and vp_hi differ, the six h-row columns are byte-identical, and no Pev_hi rises)"
exit $rc
