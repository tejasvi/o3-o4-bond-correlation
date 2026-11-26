# cmp_cw_x11_v1.awk (pk23, C_w): FILE 1 = MR_LEMMAP v3, FILE 2 = the new CW_X11 record, FILES 3.. = older CW_X11 records. The token check
# compares each record row's jlo and jhi with MR_LEMMAP v3's row of the same key as exact strings; the row compares give x1t_hi, chp_lo
# and chp_hi of the new record against each older one (INFO, in floating point). Usage: awk -f cmp_cw_x11_v1.awk LEMMAP NEW OLD [OLD ...]
FNR == 1 { f++ }
$0 !~ /^N[34]_P[0-9]+ = / { next }
{
  key = $1
  if (f == 1) { lo[key] = $3; hi[key] = $4; next }
  if (f == 2) {
    n2++; J1[key] = $3; J2[key] = $4; X[key] = $5; A[key] = $6; B[key] = $7
    if (!(key in lo)) miss++
    else if (lo[key] != $3 || hi[key] != $4) bad++
    next
  }
  c[f]++
  if (!(key in X)) { gone[f]++; next }
  d = X[key] - $5
  r = (d < 0 ? -d : d) / ($5 < 0 ? -$5 : $5)
  if (d > 0) up[f]++
  else if (d < 0) dn[f]++
  else eq[f]++
  if (r > mr[f]) mr[f] = r
  da = A[key] - $6; if (da < 0) da = -da
  if (da > ma[f]) ma[f] = da
  db = B[key] - $7; if (db < 0) db = -db
  if (db > mb[f]) mb[f] = db
  if (J1[key] != $3 || J2[key] != $4) tok[f]++
}
END {
  printf "TOKENS: %d record rows; %d keys missing in MR_LEMMAP v3; %d jlo/jhi token mismatches\n", n2, miss + 0, bad + 0
  for (i = 3; i <= f; i++)
    printf "VS FILE %d (%s): %d rows, %d not in the new record, jlo/jhi token differences %d; x1t_hi up %d, down %d, equal %d, largest relative difference %.3e; chp_lo largest |difference| %.3e, chp_hi %.3e\n", i, ARGV[i], c[i], gone[i] + 0, tok[i] + 0, up[i] + 0, dn[i] + 0, eq[i] + 0, mr[i], ma[i], mb[i]
}
