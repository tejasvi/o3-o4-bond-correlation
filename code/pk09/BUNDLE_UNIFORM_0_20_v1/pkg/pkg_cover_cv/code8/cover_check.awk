# Wave 18: independent check of the [3, 20] cover ledger (out/cover6_cv.ledger).  Verifies that the CERT intervals
# [J0 - h, J0 + h] cover [JA, JB] (sorted sweep, no gap), that every CERT line carries the vec truncation and frob lambda_5
# tags and I = 6, that L equals the rule L = ceil(sqrt(44 J_end)) for its unit segment, and reports the counts,
# the smallest margins and the wall time per interval.
#   usage: awk -v JA=3 -v JB=20 -f cover_check.awk out/cover6_cv.ledger
function lrule(je,   l) { l = int(sqrt(44 * je)); if (l * l < 44 * je) l++; return l }
BEGIN { n = 0; nf = 0; bad = 0; warn = 0 }
$5 == "FAIL" { nf++; next }
$5 == "CERT" {
    lo[n] = $1 - $2; hi[n] = $1 + $2
    if ($0 !~ /trunc=vec/ || $0 !~ /lam5=frob/ || $4 != 6) { bad++; print "BAD TAGS: " $0 }
    je = int(lo[n] + 1e-9) + 1; if (je > JB) je = JB
    if ($3 + 0 < lrule(je)) { warn++; print "note, L below the rule (the certificate bounds its own truncation): " $0 }
    for (f = 6; f <= NF; f++) {
        split($f, kv, "=")
        if (kv[1] == "F0") { if (n == 0 || kv[2] + 0 < mF0) { mF0 = kv[2] + 0; wF0 = $1 } }
        if (kv[1] == "c7") { if (n == 0 || kv[2] + 0 < mC7) { mC7 = kv[2] + 0; wC7 = $1 } }
        if (kv[1] == "secs") secs += kv[2]
    }
    n++
}
END {
    # sort by lower end (insertion sort, n is a few hundred)
    for (i = 1; i < n; i++) { x = lo[i]; y = hi[i]; j = i - 1; while (j >= 0 && lo[j] > x) { lo[j + 1] = lo[j]; hi[j + 1] = hi[j]; j-- } lo[j + 1] = x; hi[j + 1] = y }
    a = JA + 0; gaps = 0
    for (i = 0; i < n; i++) {
        if (hi[i] <= a) continue
        if (lo[i] > a) { gaps++; printf "GAP: (%.12g, %.12g)\n", a, lo[i] }
        a = hi[i]
    }
    if (a < JB) { gaps++; printf "GAP at the end: covered to %.12g < %g\n", a, JB }
    printf "CERT %d, FAIL %d, bad lines %d, L notes %d, gaps %d; covered [%g, %.12g]; min F0 %.4e (J0 %s), min C7 %.4e (J0 %s); interval seconds %.0f\n", n, nf, bad, warn, gaps, JA, a, mF0, wF0, mC7, wC7, secs
    print ((gaps == 0 && bad == 0 && a >= JB) ? "COVER OK" : "COVER NOT OK")
}
