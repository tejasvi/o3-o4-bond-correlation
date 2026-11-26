# Wave 18: cross-check of the cover ledger against the certificate outputs: for every job tag, the number of CERT and
# FAIL ledger lines must equal the number of CERTIFIED and NOT certified verdict lines in out/certint6_<tag>.txt, every
# CERTIFIED line must carry the frob lambda_5 and vec truncation tags, and no output may contain an early exit.
#   usage: awk -f cert_vs_ledger.awk out/cover6_cv.ledger out/certint6_cv_*.txt
FNR == NR { t = $NF; sub(/^job=/, "", t); if ($5 == "CERT") lc[t]++; else lf[t]++; tags[t] = 1; next }
FNR == 1 { t = FILENAME; sub(/.*certint6_/, "", t); sub(/\.txt$/, "", t); seen[t] = 1 }
/==> interval/ {
    if ($0 ~ /: CERTIFIED \[/) { oc[t]++; if ($0 !~ /lam5=frob\[9\.26,RV11_25\]/ || $0 !~ /trunc=vec\[9\.24,RV21_44;9\.25,RV11_25;9\.27\]/) bad[t]++ }
    else of[t]++
}
/exception|gaps not certified|not above tau|block separation not|truncation too large|not certified positive|a_min <= 0|vacuum rotation too large|Gram deviation too large|too large for the geometric/ { early[t]++ }
END {
    nbad = 0
    for (t in tags) {
        ok = (lc[t] + 0 == oc[t] + 0) && (lf[t] + 0 == of[t] + 0) && !(bad[t] + 0) && !(early[t] + 0) && (t in seen)
        printf "%s: ledger CERT %d FAIL %d | output CERTIFIED %d NOT %d | bad tags %d, early exits %d | %s\n", t, lc[t], lf[t], oc[t], of[t], bad[t], early[t], ok ? "OK" : "MISMATCH"
        nbad += !ok
    }
    print (nbad == 0 ? "LEDGER = CERTIFICATES" : "LEDGER/CERTIFICATE MISMATCH")
}
